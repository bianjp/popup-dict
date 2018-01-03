from typing import List, Type

from .abstract import AbstractQueryClient
from .fake import FakeQueryClient
from .youdao_web import YoudaoWebQueryClient
from .youdao_zhiyun import YoudaoZhiyunQueryClient

valid_clients: List[Type[AbstractQueryClient]] = [
    FakeQueryClient,
    YoudaoWebQueryClient,
    YoudaoZhiyunQueryClient,
]

__all__ = [
    'valid_clients',
    'AbstractQueryClient',
    'FakeQueryClient',
    'YoudaoWebQueryClient',
    'YoudaoZhiyunQueryClient',
]
