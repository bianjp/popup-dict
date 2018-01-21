import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gdk, Gst, GLib, GObject, Pango

Gst.init()

__all__ = [
    'Gtk',
    'Gdk',
    'Gst',
    'GLib',
    'GObject',
    'Pango',
]
