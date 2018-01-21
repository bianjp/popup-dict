from .exception import ConfigError
from .configuration import Configuration
from .query import *
from .speech import *

__all__ = [
    'ConfigError',
    'Configuration',
    'QueryClientConfiguration',
    'YoudaoZhiyunConfiguration',
    'SpeechConfiguration',
    'SpeechClientConfiguration',
]
