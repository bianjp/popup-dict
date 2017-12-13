from typing import Optional
from configparser import SectionProxy


class ConfigError(Exception):
    pass


# Base class for configurations of various clients
class ClientConfiguration:
    def __init__(self, request_timeout=None):
        self.request_timeout = request_timeout or 3

    # Validate configuration, raise exception if invalid
    def validate(self):
        if not isinstance(self.request_timeout, int):
            raise ConfigError('Invalid timeout type: {}. Integer required!'.format(type(self.request_timeout)))
        elif self.request_timeout <= 0:
            raise ConfigError('Invalid timeout value: {}. Should be positive!'.format(self.request_timeout))

    def __repr__(self):
        result = self.__class__.__name__ + "("
        for k, v in self.__dict__.items():
            result += str(k) + '=' + str(v) + ', '
        result = result[:-2]
        result += ')'
        return result


class FakeConfiguration(ClientConfiguration):
    pass


class YoudaoWebConfiguration(ClientConfiguration):
    def __init__(self, section: SectionProxy):
        super().__init__(section.getint('request_timeout'))


class YoudaoZhiyunConfiguration(ClientConfiguration):
    def __init__(self, section: SectionProxy):
        super().__init__(section.getint('request_timeout'))
        self.app_id = section.get('app_id')  # type: Optional[str]
        self.app_secret = section.get('app_secret')  # type: Optional[str]

    def validate(self):
        super().validate()
        if self.app_id is None or len(self.app_id) == 0:
            raise ConfigError('app_id is empty!')
        elif self.app_secret is None or len(self.app_secret) == 0:
            raise ConfigError('app_secret is empty!')
