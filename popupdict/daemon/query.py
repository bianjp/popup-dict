import time
import threading
from typing import Optional
from concurrent.futures import Future, ThreadPoolExecutor

from popupdict.gtk import *
from popupdict.ui import Popup
from popupdict.query import QueryAdapter, QueryResult
from popupdict.util import Selection


# 监视选中文本，如果变化，发起翻译请求，翻译完成后通知主线程渲染 UI
class QueryDaemon(threading.Thread):
    # 查询延时（选中文本多长时间不再变化时查询）。单位：秒
    QUERY_DELAY = 0.1

    def __init__(self, popup: Popup, query_adapter: QueryAdapter):
        super().__init__(daemon=True)
        self.popup = popup
        self.query_adapter = query_adapter
        self.executor = ThreadPoolExecutor(10)

    def run(self):
        query_task = None  # type: Optional[Future]
        last_selection = None  # type: Optional[Selection]
        while True:
            # 翻译完成，通知主线程渲染
            if query_task and query_task.done():
                query_result = query_task.result()  # type: QueryResult
                query_task = None
                if query_result:
                    # 只在主线程中渲染 UI
                    GLib.idle_add(self.popup.redraw, last_selection, query_result)

            # 选中内容不再变化时，发起翻译请求。避免选中文本过程中频繁请求
            selection = Selection.current
            if selection and not selection.queried and (
                    selection.time + __class__.QUERY_DELAY <= time.time() <=
                    selection.time + self.popup.popup_timeout):
                # 取消未完成的查询请求
                # TODO 如果请求已经在执行，Future.cancel 并不能真正取消
                if query_task:
                    query_task.cancel()

                last_selection = selection
                query_task = self.executor.submit(self.query_adapter.query, selection.text)
                selection.queried = True

            time.sleep(0.05)
