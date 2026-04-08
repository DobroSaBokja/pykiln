from ctypes import CDLL
CDLL('libgtk4-layer-shell.so')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')

from gi.repository import Gtk
from gi.repository import Gtk4LayerShell as LayerShell

import sys

import xml_parser
import widget_builder
import lib
import scripts

import os
kiln_path = os.path.abspath(os.path.expanduser(sys.argv[1]))
root = xml_parser.parse(kiln_path)

def on_activate(app):
    context = lib.Context(app)

    window: Gtk.Window = widget_builder.build(root, context)
    scripts.run_scripts()
    window.present()

app = Gtk.Application(application_id='com.dobrosabokja.pykiln')
app.connect('activate', on_activate)
app.run(None)