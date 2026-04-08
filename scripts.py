import lib
import textwrap

from gi.repository import Gtk, GLib

import lib
import factories

class Widget:
    def __init__(self, id: str, widget: Gtk.Widget):
        self.id: str = id
        self._widget: Gtk.Widget = widget

        if id in widget_dictionary:
            lib.throw_error("two widgets cant have the same id")
        else:
            widget_dictionary[id] = self
    
    def set_property(self, key: str, value):
        if key in factories.attribute_handlers and key in factories.attribute_handlers[key]:
            factories.attribute_handlers[key][key](self._widget, value)
        elif key in factories.attribute_handlers["common"]:
            factories.attribute_handlers["common"][key](self._widget, value)
        else:
            self._widget.set_property(key, lib.convert_value(self._widget, key, value))

    def connect(self, signal: str, function):
        self._widget.connect(signal, function)

scripts: list = []

widget_dictionary: dict = {}

def get(id):
    if id not in widget_dictionary:
        lib.throw_error("PYTHON: id doesnt exist")
    
    return widget_dictionary[id]

binded = []

def bind(event, func, *args):
    match event:
        case "repeat":
            time = args[0]
            def tick():
                func()
                return GLib.SOURCE_CONTINUE
            
            binded.append(GLib.timeout_add_seconds(time, tick))

def killall():
    for source in binded:
        GLib.source_remove(source)

def shell():
    import subprocess
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def run_scripts():
    globals: dict = {
        "get": get,
        "bind": bind,
    }

    for script in scripts:
        script = textwrap.dedent(script)
        exec(script, globals)