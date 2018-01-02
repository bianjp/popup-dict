from popupdict.gtk import *
from popupdict.query import QueryResult


# UI 元素
class Widgets:
    # 查询内容模板
    QUERY_TEMPLATE = '<a href="{}"><span size="xx-large" underline="none" color="#2980B9">{}</span></a>'
    QUERY_TEMPLATE_WITHOUT_LINK = '<span size="xx-large">{}</span>'
    # 词组短语列表项模板
    PHRASE_ITEM_TEMPLATE = '<a href="{}"><span underline="none" color="#2980B9">{}</span></a>: <span>{}</span>'
    PHRASE_ITEM_TEMPLATE_WITHOUT_LINK = '<span>{}</span>: <span>{}</span>'

    def __init__(self, container: Gtk.Box):
        # 查询内容
        self.query = __class__.single_line_label()  # type: Gtk.Label
        container.pack_start(self.query, False, False, 0)

        # 音标
        self.phonetic = __class__.auto_wrap_label()  # type: Gtk.Label
        container.pack_start(self.phonetic, False, False, 0)

        # 简略释义
        self.translation = __class__.auto_wrap_label()  # type: Gtk.Label
        container.pack_start(self.translation, False, False, 20)

        # 基本翻译标题
        self.explanations_label = __class__.label(
            '<span size="large" weight="bold" alpha="95%">基本释义：</span>')  # type: Gtk.Label
        container.add(self.explanations_label)

        # 基本翻译列表
        self.explanations = __class__.list_container()
        container.pack_start(self.explanations, False, False, 10)

        # 词组短语标题
        self.phrases_label = __class__.label(
            '<span size="large" weight="bold" alpha="95%">词组短语：</span>')  # type: Gtk.Label
        container.pack_start(self.phrases_label, False, False, 10)

        # 词组短语列表
        self.phrases = __class__.list_container()
        container.pack_start(self.phrases, False, False, 0)

    def draw(self, query_result: QueryResult):
        # 查询内容
        if query_result.dict_link:
            self.query.set_markup(__class__.QUERY_TEMPLATE.format(query_result.dict_link, query_result.query))
        else:
            self.query.set_markup(__class__.QUERY_TEMPLATE_WITHOUT_LINK.format(query_result.query))

        # 基本释义
        self.translation.set_text(query_result.translation)

        # 音标
        if query_result.phonetic:
            self.phonetic.set_markup('[{}]'.format(query_result.phonetic))
            self.phonetic.show()
        else:
            self.phonetic.set_markup('')
            self.phonetic.hide()

        # 基本翻译
        __class__.clear_list_container(self.explanations)
        if query_result.explanations:
            for item in query_result.explanations:
                label = __class__.auto_wrap_label(item)
                self.explanations.add(label)
            self.explanations_label.show()
            self.explanations.show_all()
        else:
            self.explanations_label.hide()
            self.explanations.hide()

        # 词组短语
        __class__.clear_list_container(self.phrases)
        if query_result.phrases:
            for item in query_result.phrases:
                if item['dict_link']:
                    markup = __class__.PHRASE_ITEM_TEMPLATE.format(item['dict_link'], item['key'], item['value'])
                else:
                    markup = __class__.PHRASE_ITEM_TEMPLATE_WITHOUT_LINK.format(item['key'], item['value'])
                label = __class__.auto_wrap_label(markup)
                self.phrases.add(label)
            self.phrases_label.show()
            self.phrases.show_all()
        else:
            self.phrases_label.hide()
            self.phrases.hide()

    # 基本 Label
    @staticmethod
    def label(markup: str = None) -> Gtk.Label:
        label = Gtk.Label(halign=Gtk.Align.START)
        if markup:
            label.set_markup(markup)
        return label

    # 单行 Label，空间不足以显示完整时，在末尾显示省略号
    @staticmethod
    def single_line_label() -> Gtk.Label:
        label = Gtk.Label(halign=Gtk.Align.START)
        label.set_single_line_mode(True)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        return label

    # 自动换行的 Label
    @staticmethod
    def auto_wrap_label(markup: str = None) -> Gtk.Label:
        label = Gtk.Label(halign=Gtk.Align.START)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        # 若不设置，换行时整个 Label 会左缩进
        label.set_xalign(0)
        if markup:
            label.set_markup(markup)
        label.show()
        return label

    # 列表容器
    @staticmethod
    def list_container() -> Gtk.Container:
        # Gtk.ListBox 样式有点问题（背景色不知如何取消），因此使用 Gtk.Box
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                            halign=Gtk.Align.START,
                            spacing=3)
        return container

    # 清空列表容器的内容
    @staticmethod
    def clear_list_container(container: Gtk.Container):
        for widget in container.get_children():
            widget.destroy()
