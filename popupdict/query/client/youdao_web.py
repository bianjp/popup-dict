from typing import Optional

from popupdict.config import *
from popupdict.query.result import QueryResult
from .abstract import AbstractQueryClient


# 使用有道词典网页版进行查词翻译
class YoudaoWebQueryClient(AbstractQueryClient):
    def __init__(self, config: YoudaoWebConfiguration):
        super().__init__(config)
        self.config = config

    def query(self, word: str) -> Optional[QueryResult]:
        raise Exception('Client not implemented!')
