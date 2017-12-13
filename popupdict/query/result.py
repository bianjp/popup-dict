from typing import Optional, List, Dict


# 查询结果
class QueryResult:
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

    def __repr__(self):
        return repr(self.__dict__)
