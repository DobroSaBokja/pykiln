import gi

from gi.repository import Gtk, GObject, Gdk
from dataclasses import dataclass

import typing
from pathlib import Path
import copy
import re

import xml.etree.ElementTree as ET

@dataclass
class Context:
    app: Gtk.Application
    base_path: Path
    parent_tag: str = ""
    parent: typing.Optional[Gtk.Widget] = None

class Blueprint:
    element: ET.Element
    context: Context
    id: str

    def __init__(self, element, context, id):
        self.element = element
        self.context = context
        self.id = id

    def create(self, parent_id=None, **kwargs):
        import scripts
        import widget_builder

        context = copy.copy(self.context)

        if parent_id is not None:
            if parent_id not in scripts.widget_dictionary:
                throw_error("No widget with id " + parent_id)
            context.parent = scripts.widget_dictionary[parent_id]._widget

        element = copy.deepcopy(self.element)

        def replace_templates(el: ET.Element):
            for attrib in el.attrib:
                if m := re.search(r'\{([^}]+)\}', el.attrib[attrib]):
                    key = m.group(1)
                    if key in kwargs:
                        el.attrib[attrib] = kwargs[key]
            for child in el:
                replace_templates(child)

        replace_templates(element)
        for child in element:
            widget_builder.build(child, context)

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
    elif vtype.pytype is Gdk.RGBA:
        color = Gdk.RGBA()
        color.parse(string_value)
        return color
    elif vtype.is_a(GObject.GEnum):
        enum_class = vtype.pytype
        if enum_class is None:
            enum_class = getattr(Gtk, vtype.name.removeprefix("Gtk"), None)
        if enum_class is None:
            throw_error("cannot resolve enum type for " + prop_name)
        for val in enum_class.__enum_values__.values():
            if val.value_nick == string_value:
                return val
        throw_error("no enum value '" + string_value + "' for " + prop_name)
    else:
        return string_value