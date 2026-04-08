import xml.etree.ElementTree as ET

import gi
from gi.repository import Gtk, Gdk

import factories
import lib
import scripts

def build(element: ET.Element, context: lib.Context):
    if element.tag == "Script":
        return
    if element.tag == "Property":
        _apply_property(element, context)
        return
    
    if element.tag == "Style":
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_string(element.text)
        except:
            lib.throw_error("Invalid CSS")

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        return

    if element.tag in factories.widget_mapping:
        widget: Gtk.Widget = factories.widget_mapping[element.tag](context)
    else:
        temp = getattr(Gtk, element.tag, None)
        if temp == None:
            lib.throw_error("unknown widget " + element.tag)
        widget: Gtk.Widget = temp()

    for key, value in element.attrib.items():
        if key == "id":
            scripts.Widget(value, widget)
            widget.set_name(value)
        elif element.tag in factories.attribute_handlers and key in factories.attribute_handlers[element.tag]:
            factories.attribute_handlers[element.tag][key](widget, value)
        elif key in factories.attribute_handlers["common"]:
            factories.attribute_handlers["common"][key](widget, value)
        else:
            widget.set_property(key, lib.convert_value(widget, key, value))

    if context.parent:
        if context.parent_tag in factories.child_adders:
            factories.child_adders[context.parent_tag](context.parent, widget)
        elif hasattr(context.parent, 'append'):
            context.parent.append(widget)
        elif hasattr(context.parent, 'set_child'):
            context.parent.set_child(widget)
        else:
            lib.throw_error(context.parent_tag, "cannot have children")
    
    new_context = lib.Context(context.app, element.tag, widget)

    for child in element:
        build(child, new_context)

    return widget

def _apply_property(element: ET.Element, context: lib.Context):
    key, value = tuple(element.text.split("="))

    if context.parent_tag in factories.attribute_handlers and key in factories.attribute_handlers[context.parent_tag]:
        factories.attribute_handlers[context.parent_tag][key](context.parent, value)
    else:
        context.parent.set_property(key, lib.convert_value(context.parent, key, value))
