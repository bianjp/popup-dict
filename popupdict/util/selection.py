import time
from typing import Optional, Tuple

from popupdict.gtk import Gdk
from .selection_filter import SelectionFilter


# 选中文本状态
class Selection:
    # 当前/最近选中状态
    current = None  # type: Optional[Selection]

    def __init__(self, text: str, event: Gdk.EventOwnerChange):
        # 是否已翻译过
        self.queried = False
        # 选中文本
        self.text = text
        # 选中时间
        # event.selection_time 不知道是怎么计算的时间戳，无法与当前时间比较
        self.time = time.time()

        # 屏幕坐标
        # 获取到的是实时坐标，查询翻译后再获取可能会有较大偏差
        _, x, y, mods = event.window.get_pointer()
        self.position = (x, y)  # type: Tuple[int, int]

        # 显示器，用于获取屏幕大小以决定弹窗位置，保证显示完整

        self.monitor = event.window.get_display().get_monitor_at_window(event.window)  # type: Gdk.Monitor

    # 每次变化时，创建一个新的对象（避免修改原对象），以避免线程同步问题
    @staticmethod
    def update(text: str, event: Gdk.EventOwnerChange):
        text = SelectionFilter.filter(text)
        if text:
            __class__.current = Selection(text, event)
