import time
from typing import Optional

from popupdict.gtk import *
from popupdict.query import QueryResult
from popupdict.util import Selection, logger
from .widgets import Widgets


# 弹窗
class Popup(Gtk.Window):
    WINDOW_WIDTH = 400  # type: int

    def __init__(self, popup_timeout: float = None, auto_play: bool = True):
        super().__init__(type=Gtk.WindowType.POPUP)

        # 弹窗显示时间。单位：秒
        self.popup_timeout = popup_timeout or 3  # type: float
        # 是否自动发音
        self.auto_play = auto_play

        self.set_border_width(10)
        self.set_default_size(__class__.WINDOW_WIDTH, -1)
        self.set_size_request(__class__.WINDOW_WIDTH, -1)

        # Initialize container, widgets
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.START)
        self.widgets = Widgets(self.box, self.pronounce)
        self.add(self.box)

        # Time to hide to window. Timestamp with float point got by time.time()
        self.time_to_hide = 0  # type: float

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        clipboard.connect("owner-change", __class__.selection_changed)

        self.current_query_result = None  # type: Optional[QueryResult]
        self.player = Gst.ElementFactory.make('playbin', 'player')  # type: Gst.Element
        if not self.player:
            raise Exception('Unable to create audio player')

        # 鼠标设备
        self.pointer_device = Gdk.Display.get_default().get_default_seat().get_pointer()  # type: Gdk.Device
        # 弹窗显示一段时间后，自动隐藏
        GLib.timeout_add(300, self.hide_window_if_timeout)

    # 渲染翻译结果
    def redraw(self, selection: Selection, query_result: QueryResult):
        if not query_result:
            logger.debug('Redraw canceled, since query_result is invalid: %s', repr(query_result))
            return
        # 若选中文本已经变化，不再显示旧的查询结果
        if selection.text != Selection.current.text:
            logger.debug('Redraw canceled, since selection has changed: original=%s, current=%s',
                         repr(selection.text), repr(Selection.current.text))
            return
        logger.debug('Redraw started for query=%s', repr(selection.text))
        self.current_query_result = query_result
        self.widgets.draw(query_result)
        minimum_height, natural_height = self.box.get_preferred_height()
        # Avoid warning: Allocating size to window without calling gtk_widget_get_preferred_width/height()
        # self.get_preferred_width()
        # self.get_preferred_height()
        self.resize(self.WINDOW_WIDTH, minimum_height)
        self.move_window(selection)
        self.show()
        self.time_to_hide = time.time() + self.popup_timeout
        if self.auto_play and query_result.speech_path:
            self.pronounce(query_result.speech_path)

    # 发音下载完成后，决定是否发音
    def on_speech_downloaded(self, query: str, path: str):
        logger.debug('on_speech_downloaded: query=%s, path=%s', repr(query), repr(path))
        if not self.auto_play:
            return
        # 若窗口未显示，或查询内容已改变，不发音
        if not self.is_visible() or not self.current_query_result or self.current_query_result.query != query:
            return
        # 避免重复发音
        if not self.current_query_result.speech_path:
            self.pronounce(path)
            self.current_query_result.speech_path = path

    # 发音
    def pronounce(self, path: Optional[str] = None):
        path = path or (self.current_query_result and self.current_query_result.speech_path)
        if not path:
            logger.error("Cannot pronounce: path=%s, current_query_result.speech_path=%s",
                         repr(path), repr(self.current_query_result and self.current_query_result.speech_path))
            return
        self.player.set_state(Gst.State.READY)
        self.player.set_property('uri', Gst.filename_to_uri(path))
        self.player.set_state(Gst.State.PLAYING)

    # 根据选中文本位置、弹窗大小、屏幕大小确定弹窗位置，保证弹窗显示完整
    def move_window(self, selection: Selection):
        target_x, target_y = selection.position
        monitor_size = selection.monitor.get_geometry()
        width, height = self.get_size()

        def try_move(x, y):
            if x >= 0 and y >= 0 and x + width <= monitor_size.width and y + height <= monitor_size.height:
                self.move(x, y)
                return True
            return False

        # 下
        if try_move(target_x, target_y + 30):
            return
        # 上
        if try_move(target_x, target_y - height - 30):
            return
        # 左
        if try_move(target_x - width - 40, target_y - height / 2):
            return
        # 右
        if try_move(target_x + 40, target_y - height / 2):
            return
        self.move(10, 10)

    # 检查鼠标是否在窗口
    def is_pointer_in_window(self) -> bool:
        _, pointer_x, pointer_y = self.pointer_device.get_position()
        x, y = self.get_position()
        width, height = self.get_size()
        return x < pointer_x < x + width and y < pointer_y < y + height

    # 弹窗显示一段时间后，自动隐藏
    def hide_window_if_timeout(self) -> bool:
        if self.is_visible() and time.time() >= self.time_to_hide:
            # 若鼠标在窗口中，延迟隐藏窗口
            if not self.is_pointer_in_window():
                self.hide()
        return True

    # 选中文本变化事件处理
    @staticmethod
    def selection_changed(clipboard: Gtk.Clipboard, event: Gdk.EventOwnerChange):
        text = clipboard.wait_for_text()
        Selection.update(text, event)
