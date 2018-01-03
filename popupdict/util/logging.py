import logging.handlers
import os.path

from popupdict.gtk import GLib

logger = logging.getLogger('popupdict')

formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

cache_dir = os.path.join(GLib.get_user_cache_dir(), 'popup-dict')
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir, 0o755)
filename = os.path.join(cache_dir, 'popup-dict.log')
file_handler = logging.handlers.RotatingFileHandler(filename,
                                                    mode='a',
                                                    maxBytes=50 * 1024 * 1024,
                                                    backupCount=5,
                                                    encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
