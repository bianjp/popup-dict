import os.path
import logging
from configparser import ConfigParser, SectionProxy
from typing import Optional, List, Dict
import pkg_resources

from popupdict.gtk import *
from .client import ConfigError
from popupdict.util import logger, config_dir


class Configuration:
    # 默认配置，始终加载
    DEFAULT_CONFIG = pkg_resources.resource_string(__package__, 'default.ini').decode()
    # 候选配置文件，按顺序检查，只加载第一个存在的文件
    CANDIDATE_CONFIG_FILES = [
        os.path.join(config_dir, 'config.ini'),
        '/etc/popup-dict/config.ini',
    ]  # type: List[str]

    def __init__(self, config_file: Optional[str] = None, extra_config: Optional[Dict] = None):
        parser = ConfigParser(default_section='client')
        parser.read_string(__class__.DEFAULT_CONFIG)

        if config_file:
            if not os.path.exists(config_file):
                raise ConfigError("Config file {} does not exist!".format(repr(config_file)))
            else:
                parser.read(config_file)
        else:
            # 若未指定配置文件，从候选配置文件中加载第一个存在的文件
            for path in __class__.CANDIDATE_CONFIG_FILES:
                if os.path.exists(path):
                    parser.read(path)
                    break

        if extra_config:
            parser.read_dict(extra_config)

        if not parser.has_section('global'):
            raise ConfigError('Missing configuration section: global')

        # 全局配置
        try:
            global_section = parser['global']
            self.query_client = global_section['query_client']

            # 调试模式
            self.debug = global_section.get('debug') and global_section.getboolean('debug', False) or False
            logger.setLevel(self.debug and logging.DEBUG or logging.INFO)

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

        # 各查询客户端配置
        # 为避免 circular imports, 不能在此处实例化 ClientConfiguration 的子类
        self.clients = {'default': parser['client']}  # type: Dict[str, SectionProxy]
        for section_name in parser.sections():
            if section_name != 'global' and section_name != 'client':
                self.clients[section_name] = parser[section_name]

    def __repr__(self):
        return repr(__dict__)
