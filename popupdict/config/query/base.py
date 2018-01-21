from configparser import SectionProxy

from ..exception import ConfigError


# 查询配置
class QueryConfiguration:
    def __init__(self, section: SectionProxy):
        self.client_id = section.get('client')

        if not self.client_id:
            raise ConfigError('No query client specified')


# 查询客户端基本配置
class QueryClientConfiguration:
    def __init__(self, section: SectionProxy):
        # noinspection PyUnresolvedReferences
        self.request_timeout = section.getint('request_timeout')

    # Validate configuration, raise exception if invalid
    def validate(self):
        if not self.request_timeout or self.request_timeout <= 0:
            raise ConfigError('Invalid request_timeout value: {}'.format(repr(self.request_timeout)))

    def __repr__(self):
        result = self.__class__.__name__ + "("
        for k, v in self.__dict__.items():
            result += str(k) + '=' + str(v) + ', '
        result = result[:-2]
        result += ')'
        return result
