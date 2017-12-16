from typing import Optional

from popupdict.config import *
from .client import *
from .result import QueryResult


# Query client adapter
class QueryAdapter:
    def __init__(self, config: Configuration):
        if config.query_client == 'fake':
            client = FakeQueryClient(config.fake)
        elif config.query_client == 'youdao-web':
            client = YoudaoWebQueryClient(config.youdao_web)
        elif config.query_client == 'youdao-zhiyun':
            client = YoudaoZhiyunQueryClient(config.youdao_zhiyun)
        else:
            raise Exception("Unknown query method: {}".format(repr(config.query_client)))

        self.client = client  # type: AbstractQueryClient

    def query(self, word: str) -> Optional[QueryResult]:
        try:
            result = self.client.query(word)
            return result
        except Exception as e:
            print("Query failed: {}".format(repr(e)))
