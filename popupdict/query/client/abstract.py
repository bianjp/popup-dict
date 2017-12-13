import urllib.parse
from abc import ABC, abstractmethod
from typing import Optional

from popupdict.query.result import QueryResult
from popupdict.config import *


# Base class for query client
class AbstractQueryClient(ABC):
    def __init__(self, config: ClientConfiguration):
        config.validate()
        self.config = config

    @abstractmethod
    def query(self, word: str) -> Optional[QueryResult]:
        pass

    # Escape URL path segment
    @staticmethod
    def escape_url_path(s: str):
        return urllib.parse.quote(s, safe='')
