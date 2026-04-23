import lib
import re
import textwrap

import xml.etree.ElementTree as ET

from gi.repository import Gtk, GLib, GObject

import lib
import factories
import widget_builder

class Widget:
    def __init__(self, id: str, widget: Gtk.Widget):
        self.id: str = id
        self._widget: Gtk.Widget = widget

        if id in widget_dictionary:
            lib.throw_error("two widgets cant have the same id")
        else:
            widget_dictionary[id] = self
    
    def set_property(self, key: str, value):
        widget_type = type(self._widget).__gtype_name__
        if widget_type in factories.attribute_handlers and key in factories.attribute_handlers[widget_type]:
            factories.attribute_handlers[widget_type][key](self._widget, str(value))
        elif key in factories.attribute_handlers["common"]:
            factories.attribute_handlers["common"][key](self._widget, str(value))
        else:
            self._widget.set_property(key, lib.convert_value(self._widget, key, str(value)))

    def get_property(self, key: str):
        pspec = self._widget.__class__.find_property(key)
        if pspec is None:
            lib.throw_error("PYTHON: no property called " + key)

        vtype = pspec.value_type
        
        if pspec.value_type.is_a(GObject.GEnum):
            enum_class = vtype.pytype
            if enum_class is None:
                enum_class = getattr(Gtk, vtype.name.removeprefix("Gtk"), None)
            if enum_class is None:
                lib.throw_error("PYTHON: cannot resolve enum type for " + key)
            for val in enum_class.__enum_values__.values():
                if val == self._widget.get_property(key):
                    if val.value_nick:
                        return val.value_nick
        else:
            return self._widget.get_property(key)

    def connect(self, signal: str, function):
        self._widget.connect(signal, function)

    def destroy(self):
        parent = self._widget.get_parent()
        if parent:
            if isinstance(parent, Gtk.Overlay):
                if parent.get_child() == self._widget:
                    parent.set_child(None)
                else:
                    parent.remove_overlay(self._widget)
            else:
                parent.remove(self._widget)
        del widget_dictionary[self.id]

class Event:
    def __init__(self, id: int):
        self.id = id
    
    def kill(self):
        GLib.source_remove(self.id)
        binded.remove(self.id)

library_scripts: list = []

main_scripts: list = []

widget_dictionary: dict = {}

blueprints: dict = {}

def get(id):
    if id not in widget_dictionary:
        lib.throw_error("PYTHON: id doesnt exist")
    
    return widget_dictionary[id]

binded = []

def bind(event, func, *args, **kwargs):
    match event:
        case "repeat":
            time = args[0]
            def tick():
                result = func()
                if result == False:
                    return GLib.SOURCE_REMOVE
                return GLib.SOURCE_CONTINUE
            if "miliseconds" in kwargs and kwargs["miliseconds"]:
                source_id = GLib.timeout_add(time, tick)
            else:
                source_id = GLib.timeout_add_seconds(time, tick)
            binded.append(source_id)
            return Event(source_id)
        case "idle":
            import threading
            wrapped_args = tuple(
                (lambda f: lambda *a: GLib.idle_add(f, *a))(a) if callable(a) else a
                for a in args
            )
            def run():
                func(*wrapped_args)
            threading.Thread(target=run, daemon=True).start()

def killall():
    for source in binded:
        GLib.source_remove(source)

def shell(cmd):
    import subprocess
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def shell_async(cmd, callback=None):
    import subprocess, threading
    def run():
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        if callback:
            GLib.idle_add(lambda: callback(result))
    threading.Thread(target=run, daemon=True).start()

def get_blueprint(id: str):
    if id not in blueprints:
        lib.throw_error("No blueprint with id " + id)

    return blueprints[id]

def run_scripts(base_path: str = None):
    import sys
    if base_path and base_path not in sys.path:
        sys.path.insert(0, base_path)

    globals: dict = {
        "get": get,
        "bind": bind,
        "get_blueprint": get_blueprint,
        "shell": shell,
        "shell_async": shell_async
    }

    for script in library_scripts + main_scripts:
        script = textwrap.dedent(script)
        exec(script, globals)
