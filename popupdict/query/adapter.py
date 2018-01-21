from typing import Optional
import time
import os.path

from popupdict.config import *
from popupdict.util import logger
from .client import *
from .result import QueryResult
from .cache import QueryCache


# Query client adapter
class QueryAdapter:
    def __init__(self, config: Configuration):
        self.cache = QueryCache()
        for client_class in valid_clients:
            if client_class.id == config.query.client_id:
                config_section = config.clients.get(client_class.id, config.clients['default'])
                client_config = client_class.config_class(config_section)
                self.client = client_class(client_config)
                break

        if not self.client:
            raise ConfigError("Unknown query client: {}".format(repr(config.query.client_id)))

    def query(self, text: str) -> Optional[QueryResult]:
        start_time = time.time()
        logger.debug('[%s] Query started for query=%s', self.client.id, repr(text))

        # noinspection PyBroadException
        try:
            result = self.cache.get(self.client.id, text)
            if result:
                # TODO 完善路径的协议检查
                if result.speech_path and result.speech_path.startswith('/') and not os.path.exists(result.speech_path):
                    result.speech_path = None
                logger.debug('[%s] Cache hit for query=%s, result=%s', self.client.id, repr(text), repr(result))
                return result

            result = self.client.query(text)
            logger.debug('[%s] Query finished for query=%s, result=%s', self.client.id, repr(text), repr(result))
            if result:
                self.cache.put(self.client.id, text, result)
            return result
        except Exception:
            logger.exception('[%s] Query failed for query=%s', self.client.id, repr(text))
        finally:
            time_spent = (time.time() - start_time) * 1000
            logger.debug('[%s] Time spent: %fms', self.client.id, time_spent)
