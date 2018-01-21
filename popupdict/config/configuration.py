import os.path
import logging
from configparser import ConfigParser, SectionProxy
from typing import Optional, List, Dict
import pkg_resources

from popupdict.gtk import *
from popupdict.util import logger, config_dir
from .exception import ConfigError
from .query import QueryConfiguration
from .speech import SpeechConfiguration


class Configuration:
    # 默认配置，始终加载
    DEFAULT_CONFIG = pkg_resources.resource_string(__package__, 'default.ini').decode()
    # 候选配置文件，按顺序检查，只加载第一个存在的文件
    CANDIDATE_CONFIG_FILES = [
        os.path.join(config_dir, 'config.ini'),
        '/etc/popup-dict/config.ini',
    ]  # type: List[str]

    def __init__(self, config_file: Optional[str] = None, extra_config: Optional[Dict] = None):
        if config_file:
            if not os.path.exists(config_file):
                raise ConfigError("Config file {} does not exist!".format(repr(config_file)))
        else:
            # 若未指定配置文件，从候选配置文件中加载第一个存在的文件
            for path in __class__.CANDIDATE_CONFIG_FILES:
                if os.path.exists(path):
                    config_file = path
                    break

        parser = self.get_parser(None, config_file, extra_config)

        # 全局配置
        try:
            global_section = parser['global']

            # 调试模式
            self.debug = global_section.get('debug') and global_section.getboolean('debug', False) or False
            logger.setLevel(self.debug and logging.DEBUG or logging.INFO)

            # 是否启用缓存
            self.cache = global_section.getboolean('cache')
            # 最大缓存条目数。仅针对单个查询客户端、发音客户端
            self.max_cache_items = global_section.getint('max_cache_items')

            # 弹窗显示时间
            self.popup_timeout = global_section.getfloat('popup_timeout')

            # Gtk Global Dark Theme
            # 不设置或设为空则使用系统默认设置
            prefer_dark_theme = global_section.get('prefer_dark_theme')
            if prefer_dark_theme is not None and prefer_dark_theme != '':
                self.prefer_dark_theme = global_section.getboolean('prefer_dark_theme')
                Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", self.prefer_dark_theme)
            else:
                self.prefer_dark_theme = None

        except KeyError as e:
            raise ConfigError('Missing global configuration: ' + e.args[0])

        # 查询配置
        self.query = QueryConfiguration(parser['query'])
        # 发音配置
        self.speech = SpeechConfiguration(parser['speech'])

        # 各查询客户端配置
        # 为避免 circular imports, 不能在此处实例化 ClientConfiguration 的子类
        parser = self.get_parser('query-client', config_file, extra_config)
        self.clients = {'default': parser['query-client']}  # type: Dict[str, SectionProxy]
        for section_name in parser.sections():
            if section_name.startswith('query:'):
                self.clients[section_name.replace('query:', '')] = parser[section_name]

        # 各发音客户端配置
        parser = self.get_parser('speech-client', config_file, extra_config)
        self.speech_clients = {'default': parser['speech-client']}  # type: Dict[str, SectionProxy]
        for section_name in parser.sections():
            if section_name.startswith('speech:'):
                self.speech_clients[section_name.replace('speech:', '')] = parser[section_name]

    def __repr__(self):
        return repr(__dict__)

    # 解析配置
    # ConfigParser 的 default_section 不能动态修改，因此需要不同的 default_section 时重新解析配置
    @staticmethod
    def get_parser(default_section: Optional[str],
                   config_file: Optional[str] = None,
                   extra_config: Optional[Dict] = None) -> ConfigParser:
        parser = ConfigParser(default_section=default_section)
        parser.read_string(__class__.DEFAULT_CONFIG)

        if config_file:
            parser.read(config_file)

        if extra_config:
            parser.read_dict(extra_config)

        return parser
