import time

from popupdict.gtk import *
from popupdict.query import QueryResult
from popupdict.util import Selection
from .widgets import Widgets


# 弹窗
class Popup(Gtk.Window):
    WINDOW_WIDTH = 400  # type: int

    def __init__(self, popup_timeout: float = None):
        super().__init__(type=Gtk.WindowType.POPUP)

        # 弹窗显示时间。单位：秒
        self.popup_timeout = popup_timeout or 3  # type: float

        self.set_border_width(10)
        self.set_default_size(__class__.WINDOW_WIDTH, -1)
        self.set_size_request(__class__.WINDOW_WIDTH, -1)

        # Initialize container, widgets
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.START)
        self.widgets = Widgets(self.box)
        self.add(self.box)

        # Time to hide to window. Timestamp with float point got by time.time()
        self.time_to_hide = 0  # type: float

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        clipboard.connect("owner-change", __class__.selection_changed)

    # 渲染翻译结果
    def redraw(self, selection: Selection, query_result: QueryResult):
        # 若选中文本已经变化，不再显示旧的查询结果
        if not query_result or selection.text != Selection.current.text:
            return
        self.widgets.draw(query_result)
        minimum_height, natural_height = self.box.get_preferred_height()
        # Avoid warning: Allocating size to window without calling gtk_widget_get_preferred_width/height()
        # self.get_preferred_width()
        # self.get_preferred_height()
        self.resize(self.WINDOW_WIDTH, minimum_height)
        self.move_window(selection)
        self.show()
        self.time_to_hide = time.time() + self.popup_timeout

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

    # 选中文本变化事件处理
    @staticmethod
    def selection_changed(clipboard: Gtk.Clipboard, event: Gdk.EventOwnerChange):
        text = clipboard.wait_for_text()
        Selection.update(text, event)
