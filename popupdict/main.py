import signal
import os.path
import sys
import psutil
import argparse
from typing import Optional

from .gtk import *
from .config import Configuration, ConfigError
from .query import QueryAdapter
from .ui import Popup
from .daemon import QueryDaemon

PID_FILE = os.path.join(GLib.get_user_cache_dir(), 'popup-dict/popup-dict.pid')


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


def start(config_file: str = None, debug: bool = False):
    config = Configuration(config_file)
    query_adapter = QueryAdapter(config)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window = Popup()
    window.show_all()
    window.hide()

    QueryDaemon(window, query_adapter).start()

    Gtk.main()


def main():
    parser = argparse.ArgumentParser(description='划词翻译')
    parser.add_argument('--debug', default=False, action='store_true', help='调试模式')
    parser.add_argument('--config', help='配置文件，默认 ~/.config/popup-dict/config.ini, 或 /etc/popup-dict/config.ini',
                        metavar='CONFIG_FILE')
    args = parser.parse_args()

    if args.config and not os.path.exists(args.config):
        print("Config file {} does not exist!".format(repr(args.config)), file=sys.stderr)
        sys.exit(1)

    if is_running():
        print('An instance is already running!', file=sys.stderr)
        sys.exit(2)
    else:
        write_pid(os.getpid())
        try:
            start(config_file=args.config, debug=args.debug)
        except ConfigError as e:
            print(e.args[0], file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
