from typing import Optional
import requests

from .abstract import AbstractSpeechClient
from popupdict.util import logger


class YoudaoSpeechClient(AbstractSpeechClient):
    id = 'youdao'

    def get(self, text: str, save_path: str) -> Optional[str]:
        params = {'le': 'en', 'audio': text}
        # noinspection PyBroadException
        try:
            res = requests.get('http://dict.youdao.com/dictvoice', params=params, timeout=self.config.request_timeout)
            if res.status_code != 200 or len(res.content) < 1000:
                return
            with open(save_path, 'wb') as f:
                f.write(res.content)

            return save_path

        except Exception:
            logger.exception('[speech %s] Request failed for text=%s', self.id, repr(text))
            return
