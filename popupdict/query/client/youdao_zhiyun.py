import requests
import random
import hashlib
import json
from typing import Optional

from popupdict.config import *
from popupdict.util import logger
from .abstract import AbstractQueryClient
from ..result import QueryResult


# 有道智云的自然语言翻译服务
class YoudaoZhiyunQueryClient(AbstractQueryClient):
    id = 'youdao-zhiyun'
    config_class = YoudaoZhiyunConfiguration

    API = 'https://openapi.youdao.com/api'
    DICT_LINK = 'https://dict.youdao.com/w/{}/{}/'

    def __init__(self, config: YoudaoZhiyunConfiguration):
        super().__init__(config)
        self.config = config

    def query(self, text: str) -> Optional[QueryResult]:
        try:
            res = requests.get(self.API, params=self._params(text), timeout=self.config.request_timeout)
            if not res.ok:
                logger.error('[%s] Request failed for query=%s: status_code=%s, reason=%s, content=%s',
                             self.id, repr(text), res.status_code, res.reason, repr(res.text))
                return

            try:
                result = res.json()
            except json.decoder.JSONDecodeError:
                logger.error('[%s] Invalid JSON response for query=%s: ', self.id, repr(text), repr(res.text))
                return

            if result['errorCode'] != '0':
                logger.error('[%s] Query failed for query=%s: errorCode=%s',
                             self.id, repr(text), str(result['errorCode']))
                return

            # 没有有效翻译结果
            if not result['translation'] or (len(result['translation']) == 1 and
                                             result['translation'][0] == result['query']):
                logger.debug('[%s] No translation for query=%s: %s', self.id, repr(text), result)
                return

            logger.debug('[%s] Request success for query=%s: %s', self.id, repr(text), result)

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
        except requests.exceptions.RequestException:
            logger.exception('[%s] Request failed for query=%s', self.id, repr(text))

    @staticmethod
    def dict_link(lang, query):
        return __class__.DICT_LINK.format(lang, __class__.escape_url_path(query))

    # 构造请求参数
    def _params(self, text: str):
        # http://ai.youdao.com/docs/doc-trans-api.s#p02
        params = {
            'q': text,
            # 设置为 auto 会导致有时识别错误
            'from': 'EN',
            'to': 'zh-CHS',
            'appKey': self.config.app_id,
            'salt': random.randint(1, 10000),
        }
        s = self.config.app_id + text + str(params['salt']) + self.config.app_secret
        params['sign'] = hashlib.md5(s.encode()).hexdigest()
        return params
