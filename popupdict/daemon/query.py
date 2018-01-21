import time
import threading
from typing import Optional
from concurrent.futures import Future, ThreadPoolExecutor

from popupdict.gtk import *
from popupdict.ui import Popup
from popupdict.query import QueryAdapter, QueryResult
from popupdict.speech import SpeechAdapter
from popupdict.util import Selection


# 监视选中文本，如果变化，发起翻译请求，翻译完成后通知主线程渲染 UI
# 为何使用单独的线程：
#   1. 避免主线程繁忙/阻塞，影响响应速度
#   2. 为避免选中文本过程中频繁触发查询，需要延时查询（即选中内容不再变化时再查询）。使用线程更易处理
# 有些软件（如 Gnome Terminal）中释放鼠标后才会触发 selection change 事件，而有些软件（如 IntelliJ IDEA）在选中过程中会不停触发
class QueryDaemon(threading.Thread):
    # 查询延时（选中文本多长时间不再变化时查询）。单位：秒
    QUERY_DELAY = 0.1

    def __init__(self, popup: Popup,
                 query_adapter: QueryAdapter,
                 speech_adapter: Optional[SpeechAdapter]):
        super().__init__(daemon=True)
        self.popup = popup
        self.query_adapter = query_adapter
        self.speech_adapter = speech_adapter
        self.executor = ThreadPoolExecutor(20)

    def run(self):
        last_selection = None  # type: Optional[Selection]
        # 查询翻译任务
        query_task = None  # type: Optional[Future]
        # 下载发音任务
        speech_task = None  # type: Optional[Future]
        # 查询翻译、下载发音两个任务的完成顺序是不确定的。后者是次要功能，不应拖慢 UI 响应
        # 如果查询翻译完成时，下载发音还未完成，立即渲染 UI，不必等待。待发音下载完成后，由 UI 组件决定是否发音
        while True:
            # 翻译完成，通知主线程渲染
            if query_task and query_task.done():
                query_result = query_task.result()  # type: QueryResult
                query_task = None
                if query_result:
                    # 若发音已下载完成，优先使用
                    if speech_task:
                        if speech_task.done():
                            query_result.speech_path = speech_task.result()
                            speech_task = None
                        # 若翻译结果中已有发音，取消下载发音任务
                        elif query_result.speech_path:
                            speech_task.cancel()
                            speech_task = None
                    # 只在主线程中渲染 UI
                    GLib.idle_add(self.popup.redraw, last_selection, query_result)

            # 翻译结果渲染后，发音才下载好。
            if not query_task and speech_task and speech_task.done():
                speech_path = speech_task.result()
                speech_task = None
                if speech_path:
                    GLib.idle_add(self.popup.on_speech_downloaded, last_selection.text, speech_path)

            # 选中内容不再变化时，发起翻译请求。避免选中文本过程中频繁请求
            selection = Selection.current
            if selection and not selection.queried and (selection.time + __class__.QUERY_DELAY
                                                        <= time.time() <=
                                                        selection.time + self.popup.popup_timeout):
                # 取消未完成的查询请求
                # TODO 如果请求已经在执行，Future.cancel 并不能真正取消
                if query_task:
                    query_task.cancel()
                if speech_task:
                    speech_task.cancel()

                last_selection = selection
                query_task = self.executor.submit(self.query_adapter.query, selection.text)
                if self.speech_adapter:
                    speech_task = self.executor.submit(self.speech_adapter.get, selection.text)

                selection.queried = True

            time.sleep(0.05)
