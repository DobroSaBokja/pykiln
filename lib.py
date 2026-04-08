import gi

from gi.repository import Gtk, GObject
from dataclasses import dataclass

import typing

@dataclass
class Context:
    app: Gtk.Application
    parent_tag: str = ""
    parent: typing.Optional[Gtk.Widget] = None

def throw_error(message):
    print("ERROR:", message)
    exit(1)

def convert_value(widget: Gtk.Widget, prop_name, string_value):
    pspec = widget.__class__.find_property(prop_name)
    if pspec is None:
        throw_error("no property called " + prop_name)

    vtype = pspec.value_type

    if vtype == GObject.TYPE_STRING:
        return string_value
    elif vtype == GObject.TYPE_INT or vtype == GObject.TYPE_LONG:
        return int(string_value)
    elif vtype == GObject.TYPE_FLOAT or vtype == GObject.TYPE_DOUBLE:
        return float(string_value)
    elif vtype == GObject.TYPE_BOOLEAN:
        return string_value.lower() in ("true", "1", "yes")
    elif vtype.is_a(GObject.GEnum):
        enum_class = vtype.pytype
        for val in enum_class.__enum_values__.values():
            if val.value_nick == string_value:
                return val
        throw_error("no enum called " + prop_name)
    else:
        return string_value