import lib
import textwrap

from gi.repository import Gtk

import lib
import factories

class Widget:
    def __init__(self, id: str, widget: Gtk.Widget):
        self.id: str = id
        self._widget: Gtk.Widget = widget

        if id in widget_dictionary:
            lib.throw_error("two widgets cant have the same id")
        else:
            widget_dictionary[id] = widget
    
    def set_property(self, key: str, value):
        if key in factories.attribute_handlers and key in factories.attribute_handlers[key]:
            factories.attribute_handlers[key][key](self._widget, value)
        elif key in factories.attribute_handlers["common"]:
            factories.attribute_handlers["common"][key](self._widget, value)
        else:
            widget.set_property(key, lib.convert_value(self._widget, key, value))

    def connect(self, signal: str, function):
        self._widget.connect(signal, function)

scripts: list = []

widget_dictionary: dict = {}

def get(id):
    if id not in widget_dictionary:
        lib.throw_error("PYTHON: id doesnt exist")
    
    return widget_dictionary[id]

def run_scripts():
    globals: dict = {
        "get": get
    }

    for script in scripts:
        script = textwrap.dedent(script)
        exec(script, globals)