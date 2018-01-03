import random

from .abstract import AbstractQueryClient
from popupdict.query.result import QueryResult


# 随机返回查询结果。开发/测试时使用，避免频繁调用接口
class FakeQueryClient(AbstractQueryClient):
    id = 'fake'
    QUERY_RESULTS = [
        QueryResult('phonetic', '语音',
                    phonetic="fə'nɛtɪk",
                    explanations=['adj. 语音的，语音学的；音形一致的；发音有细微区别的'],
                    phrases=[{'value': '语音的; 语音学的; 语言的', 'key': 'phonetic'},
                             {'value': '语音特征; 语音要素; 语音面貌', 'key': 'phonetic feature'},
                             {'value': '注音; 直音注音; 标音', 'key': 'phonetic notation'}]
                    ),
        QueryResult('resume', '个人简历',
                    phonetic="rezju:'mei, ri'zju:m; -'zu:m",
                    explanations=['n. 摘要；[管理] 履历，简历', 'vi. 重新开始，继续', 'vt. 重新开始，继续；恢复，重新占用'],
                    phrases=[{'value': '重新开始; 简历; 恢复', 'key': 'resume'}, {'value': '简历', 'key': 'Resume'},
                             {'value': '视频简历; 视频简历; 频简历', 'key': 'Video resume'}]
                    ),
        QueryResult('fraught', '令人担忧的',
                    phonetic='frɔt',
                    explanations=['adj. 担心的，忧虑的；充满…的'],
                    phrases=[{'value': '误人子弟; 充满的; 忧虑的', 'key': 'Fraught'},
                             {'value': '伴随的', 'key': 'fraught a'},
                             {'value': '充满; 误人子弟; 带有', 'key': 'fraught with'}]
                    ),
    ]

    DICT_LINK = 'https://dict.youdao.com/w/eng/{}/'
    for query_result in QUERY_RESULTS:
        query_result.dict_link = DICT_LINK.format(AbstractQueryClient.escape_url_path(query_result.query))
        if query_result.phrases:
            for phrase in query_result.phrases:
                phrase['dict_link'] = DICT_LINK.format(AbstractQueryClient.escape_url_path(phrase['key']))

    def query(self, word: str) -> QueryResult:
        return __class__.QUERY_RESULTS[random.randint(0, len(__class__.QUERY_RESULTS) - 1)]
