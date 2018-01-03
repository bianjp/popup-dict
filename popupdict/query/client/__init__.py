from .abstract import AbstractQueryClient
from .fake import FakeQueryClient
from .youdao_web import YoudaoWebQueryClient
from .youdao_zhiyun import YoudaoZhiyunQueryClient

valid_clients = [
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
