from ctypes import CDLL
CDLL('libgtk4-layer-shell.so')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')

from gi.repository import Gtk
from gi.repository import Gtk4LayerShell as LayerShell

import xml_parser
import widget_builder
import lib
import scripts

root = xml_parser.parse("test.kiln")

def on_activate(app):
    context = lib.Context(app)

    window: Gtk.Window = widget_builder.build(root, context)
    scripts.run_scripts()
    window.present()

app = Gtk.Application(application_id='com.dobrosabokja.pykiln')
app.connect('activate', on_activate)
app.run(None)