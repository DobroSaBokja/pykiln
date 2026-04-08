from ctypes import CDLL
CDLL('libgtk4-layer-shell.so')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')

from gi.repository import Gtk, Gio
from gi.repository import Gtk4LayerShell as LayerShell

import sys

import xml_parser
import widget_builder
import lib
import scripts

import os
kiln_path = os.path.abspath(os.path.expanduser(sys.argv[1]))
root = xml_parser.parse(kiln_path)

window: Gtk.Window

def on_activate(app):
    context = lib.Context(app)

    global window

    window = widget_builder.build(root, context)
    scripts.run_scripts()
    window.present()

def on_file_changed(monitor, file, other_file, event_type):
    if event_type != Gio.FileMonitorEvent.CHANGES_DONE_HINT:
        return

    global window

    window.destroy()
    scripts.killall()
    scripts.scripts.clear()
    scripts.widget_dictionary.clear()

    context = lib.Context(app)
    new_root = xml_parser.parse(kiln_path)
    window = widget_builder.build(new_root, context)
    scripts.run_scripts()
    window.present()
        

f = Gio.File.new_for_path(kiln_path)
monitor = f.monitor_file(Gio.FileMonitorFlags.NONE, None)
monitor.connect("changed", on_file_changed)

app = Gtk.Application(application_id='com.dobrosabokja.pykiln')
app.connect('activate', on_activate)
app.run(None)