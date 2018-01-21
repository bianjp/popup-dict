import os.path

from popupdict.gtk import GLib

config_dir = os.path.join(GLib.get_user_config_dir(), 'popup-dict')

cache_dir = os.path.join(GLib.get_user_cache_dir(), 'popup-dict')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir, 0o755)
