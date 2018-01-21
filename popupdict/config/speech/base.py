from configparser import SectionProxy

from ..exception import ConfigError


# 发音配置
class SpeechConfiguration:
    # noinspection PyUnresolvedReferences
    def __init__(self, section: SectionProxy):
        # 是否启用发音
        self.enabled = section.getboolean('enabled')
        # 是否自动播放发音
        self.auto_play = section.getboolean('auto_play')
        # 发音客户端 id
        self.client_id = section.get('client')

        if self.enabled and not self.client_id:
            raise ConfigError('No speech client specified')


# 各发音客户端配置基类
class SpeechClientConfiguration:
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
