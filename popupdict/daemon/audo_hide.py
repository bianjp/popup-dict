import threading
import time

from popupdict.gtk import *
from popupdict.ui.popup import Popup


# 弹窗显示一段时间后，自动隐藏
# 为何使用单独的线程：
#    1. time.sleep 会阻塞整个线程，因此不宜在主线程中调用（拖慢更新选中文本的速度）
#    2. 若主线程正在阻塞（比如在等待 HTTP 请求完成），会无法隐藏窗口
class AutoHidePopupDaemon(threading.Thread):
    def __init__(self, popup: Popup):
        super().__init__(daemon=True)
        self.popup = popup
        # 鼠标设备
        self.pointer_device = Gdk.Display.get_default().get_default_seat().get_pointer()  # type: Gdk.Device

    # 检查鼠标是否在窗口
    def is_pointer_in_window(self) -> bool:
        _, pointer_x, pointer_y = self.pointer_device.get_position()
        x, y = self.popup.get_position()
        width, height = self.popup.get_size()
        return x < pointer_x < x + width and y < pointer_y < y + height

    def run(self):
        while True:
            if self.popup.is_visible() and time.time() >= self.popup.time_to_hide:
                # 若鼠标在窗口中，延迟隐藏窗口
                if not self.is_pointer_in_window():
                    # self.window.hide()
                    # 只在主线程中操作 UI
                    GLib.idle_add(self.popup.hide)
            time.sleep(0.3)
