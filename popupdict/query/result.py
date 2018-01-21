from typing import Optional, List, Dict


# 查询结果
class QueryResult:
    # 类版本。de-serializing 时需要检查当前版本是否与 serializing 时的版本相同，避免反序列化错误
    VERSION = 1

    def __init__(self, query: str, translation: str,
                 dict_link: Optional[str] = None,
                 phonetic: Optional[str] = None,
                 explanations: Optional[List[str]] = None,
                 phrases: Optional[List[Dict[str, str]]] = None):
        # 查询的单词
        self.query = query  # type: str
        # 在线词典链接
        self.dict_link = dict_link  # type: Optional[str]
        # 简略释义（一句话解释）
        self.translation = translation  # type: str
        # 音标
        self.phonetic = phonetic  # type: Optional[str]
        # 基本释义
        self.explanations = explanations  # type: Optional[List[str]]
        # 词组短语 [{"key": "词组/短语", value: ["翻译"], "dict_link": "在线词典链接（可为 None）"}]
        self.phrases = phrases  # type: Optional[List[Dict[str, str]]]

        # 发音文件路径。本地路径或 URL
        self.speech_path = None  # type: Optional[str]

    def __repr__(self):
        return repr(self.__dict__)
