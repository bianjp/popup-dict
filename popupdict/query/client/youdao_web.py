from typing import Optional

from popupdict.config import *
from popupdict.query.result import QueryResult
from .abstract import AbstractQueryClient


# 有道词典网页版
class YoudaoWebQueryClient(AbstractQueryClient):
    id = 'youdao-web'

    def __init__(self, config: YoudaoWebConfiguration):
        super().__init__(config)
        self.config = config

    def query(self, word: str) -> Optional[QueryResult]:
        raise Exception('Client not implemented!')
