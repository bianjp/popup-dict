from configparser import SectionProxy


class ConfigError(Exception):
    pass


# Base class for configurations of various clients
class ClientConfiguration:
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
