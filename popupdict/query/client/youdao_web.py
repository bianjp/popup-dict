from typing import Optional

from popupdict.config import *
from .abstract import AbstractQueryClient
from ..result import QueryResult


# 有道词典网页版
class YoudaoWebQueryClient(AbstractQueryClient):
    id = 'youdao-web'
    config_class = QueryClientConfiguration

    def query(self, word: str) -> Optional[QueryResult]:
        raise Exception('Client not implemented!')
