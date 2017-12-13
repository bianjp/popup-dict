import requests
import random
import hashlib
import json
from typing import Optional

from popupdict.config import *
from popupdict.query.result import QueryResult
from .abstract import AbstractQueryClient


# 使用有道智云的自然语言翻译服务进行查词翻译
class YoudaoZhiyunQueryClient(AbstractQueryClient):
    API = 'https://openapi.youdao.com/api'
    DICT_LINK = 'https://dict.youdao.com/w/{}/{}/'

    def __init__(self, config: YoudaoZhiyunConfiguration):
        super().__init__(config)
        self.config = config

    def query(self, text: str) -> Optional[QueryResult]:
        try:
            res = requests.get(self.API, params=self._params(text), timeout=self.config.request_timeout)
            if not res.ok:
                print("Request failed for text={}: status_code={}, reason={}, content={}".format(
                    repr(text), res.status_code, res.reason, res.text))
                return None

            try:
                result = res.json()
            except json.decoder.JSONDecodeError as e:
                print("Invalid JSON response for text={}: ".format(repr(text), res.text))
                return

            if result['errorCode'] != '0':
                print("Query failed for word={}: errorCode={}".format(
                    repr(text), str(result['errorCode'])))
                return None

            language = result['l'].replace('2zh-CHS', '').lower()

            basic = result.get('basic')
            phrases = result.get('web')
            if phrases is not None:
                for phrase in phrases:
                    phrase['value'] = '; '.join(phrase['value'])
                    phrase['dict_link'] = __class__.dict_link(language, phrase['key'])

            # 小语种查询结果没有 'query'
            query_result = QueryResult(result.get('query', text), '; '.join(result['translation']),
                                       dict_link=__class__.dict_link(language, result.get('query', text)),
                                       phonetic=basic and (
                                           basic.get('us-phonetic') or
                                           basic.get('uk-phonetic') or
                                           basic.get('phonetic')),
                                       explanations=basic and basic.get('explains'),
                                       phrases=phrases
                                       )
            return query_result
        except requests.exceptions.RequestException as e:
            print("Request failed for text={}: {}".format(repr(text), repr(e)))

    @staticmethod
    def dict_link(lang, query):
        return __class__.DICT_LINK.format(lang, __class__.escape_url_path(query))

    # 构造请求参数
    def _params(self, text):
        # http://ai.youdao.com/docs/doc-trans-api.s#p02
        params = {
            'q': text,
            'from': 'auto',
            'to': 'zh-CHS',
            'appKey': self.config.app_id,
            'salt': random.randint(1, 10000),
        }
        s = self.config.app_id + text + str(params['salt']) + self.config.app_secret
        params['sign'] = hashlib.md5(s.encode()).hexdigest()
        return params
