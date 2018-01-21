import os.path
from typing import Optional
import tempfile
import time

from popupdict.config import Configuration, ConfigError
from popupdict.util import cache_dir, logger
from .client import *


class SpeechAdapter:
    def __init__(self, config: Configuration):
        for client_class in valid_speech_clients:
            if client_class.id == config.speech.client_id:
                config_section = config.speech_clients.get(client_class.id, config.speech_clients['default'])
                client_config = client_class.config_class(config_section)
                self.client = client_class(client_config)
                break
        if not self.client:
            raise ConfigError("Unknown speech client: {}".format(repr(config.speech.client_id)))

        self.cache_enabled = config.cache
        self.max_cache_items = config.max_cache_items
        if self.cache_enabled:
            self.cache_dir = os.path.join(cache_dir, 'speech', self.client.id)  # type: str
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir, 0o755)
        else:
            self.tmp_dir = tempfile.mkdtemp(prefix='popup-dict-speech-' + self.client.id + '.')  # type: str

    def get(self, text: str) -> Optional[str]:
        start_time = time.time()
        logger.debug('[speech %s] Get speech started for text=%s', self.client.id, repr(text))

        # noinspection PyBroadException
        try:
            # 检查缓存
            if self.cache_enabled:
                path = os.path.join(self.cache_dir, text)
                if os.path.exists(path) and os.path.getsize(path) > 0:
                    logger.debug('[speech %s] Cache hit for text=%s', self.client.id, repr(text))
                    return path
            else:
                path = os.path.join(self.tmp_dir, text)
                if os.path.exists(path):
                    return path

            path = self.client.get(text, path)
            logger.debug('[speech %s] Get speech finished for text=%s, path=%s', self.client.id, repr(text), repr(path))
            return path

        except Exception:
            logger.exception('[speech %s] Get speech failed for text=%s', self.client.id, repr(text))
        finally:
            time_spent = (time.time() - start_time) * 1000
            logger.debug('[speech %s] Time spent: %fms', self.client.id, time_spent)

    # 缓存条目数超出数量时，删除旧缓存。使用 LRU 原则
    def remove_old_cache(self):
        start_time = time.time()
        files = os.listdir(self.cache_dir)
        if len(files) <= self.max_cache_items:
            return
        files = [os.path.join(self.cache_dir, f) for f in files]
        pairs = [(os.path.getatime(f), f) for f in files]
        pairs.sort()
        for pair in pairs[1000:]:
            os.remove(pair[1])
        time_spent = (time.time() - start_time) * 1000
        logger.debug('Time spent for clearing old speech cache: %fms', time_spent)
