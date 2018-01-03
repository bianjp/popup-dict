import signal
import os.path
import sys
import psutil
import argparse
from typing import Optional, Dict

from .gtk import *
from .config import Configuration, ConfigError
from .query import QueryAdapter
from .ui import Popup
from .daemon import QueryDaemon

PID_FILE = os.path.join(GLib.get_user_cache_dir(), 'popup-dict', 'popup-dict.pid')


def read_pid() -> Optional[int]:
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            try:
                return int(f.read().strip())
            except ValueError:
                pass
    return None


def write_pid(pid: int):
    os.makedirs(os.path.dirname(PID_FILE), 0o755, True)
    with open(PID_FILE, 'w') as f:
        f.write(str(pid))


def delete_pid():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def is_running():
    pid = read_pid()
    if pid and psutil.pid_exists(pid):
        process = psutil.Process(pid)
        if 'dict' in process.name():
            return True
    return False


def start(config_file: str = None, cmd_config: Optional[Dict] = None):
    config = Configuration(config_file, cmd_config)
    query_adapter = QueryAdapter(config)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window = Popup()
    window.show_all()
    window.hide()

    QueryDaemon(window, query_adapter).start()

    Gtk.main()


def main():
    parser = argparse.ArgumentParser(description='划词翻译')
    parser.add_argument('--client', metavar='CLIENT_ID', help='查询客户端')
    parser.add_argument('--debug', default=None, action='store_true', help='开启调试模式')
    parser.add_argument('--no-debug', default=None, action='store_false', help='关闭调试模式', dest='debug')
    parser.add_argument('-c', '--config', metavar='CONFIG_FILE',
                        help='配置文件，默认 ~/.config/popup-dict/config.ini, 或 /etc/popup-dict/config.ini')
    args = parser.parse_args()

    if args.config and not os.path.exists(args.config):
        print("Config file {} does not exist!".format(repr(args.config)), file=sys.stderr)
        sys.exit(1)

    # 命令行配置项，用于覆盖配置文件中的配置
    cmd_config = {
        'global': {
            'query_client': args.client,
            'debug': args.debug,
        }
    }

    # 未指定命令行参数时避免覆盖配置文件
    cmd_config['global'] = {k: v for k, v in cmd_config['global'].items() if v is not None}

    if is_running():
        print('An instance is already running!', file=sys.stderr)
        sys.exit(2)
    else:
        write_pid(os.getpid())
        try:
            start(args.config, cmd_config)
        except ConfigError as e:
            print(e.args[0], file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
