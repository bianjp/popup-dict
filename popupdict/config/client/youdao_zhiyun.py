from typing import Optional
from configparser import SectionProxy

from .base import ConfigError, ClientConfiguration


class YoudaoZhiyunConfiguration(ClientConfiguration):
    def __init__(self, section: SectionProxy):
        super().__init__(section)
        self.app_id = section.get('app_id')  # type: Optional[str]
        self.app_secret = section.get('app_secret')  # type: Optional[str]

    def validate(self):
        super().validate()
        if not self.app_id:
            raise ConfigError('app_id is empty!')
        elif not self.app_secret:
            raise ConfigError('app_secret is empty!')
