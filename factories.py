import gi
from gi.repository import Gtk, Gdk
from gi.repository import Gtk4LayerShell as LayerShell

import lib

def _parse_bool(value):
    return value.lower() in ("true", "1", "yes")


def _set_all_margins(widget, margin):
    widget.set_margin_start(margin)
    widget.set_margin_end(margin)
    widget.set_margin_top(margin)
    widget.set_margin_bottom(margin)


def _construct_bar(context):
    window = Gtk.Window(application=context.app)

    provider = Gtk.CssProvider()
    provider.load_from_string("* { margin: 0; padding: 0; }")
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    window.set_decorated(False)

    LayerShell.init_for_window(window)
    LayerShell.set_layer(window, LayerShell.Layer.TOP)

    return window

def _toggle_exclusive_zone(w, v):
    if v.lower() in ("true", "1", "yes"):
        LayerShell.auto_exclusive_zone_enable(w)
    else:
        LayerShell.set_exclusive_zone(w, 0)

widget_mapping = {
    "Window": lambda context: Gtk.Window(application=context.app),
    "ApplicationWindow": lambda context: Gtk.ApplicationWindow(application=context.app),
    "Bar": _construct_bar
}

attribute_handlers = {
    "Bar": {
        "exclusive-zone": _toggle_exclusive_zone,
        "anchored-top": lambda w, v: LayerShell.set_anchor(w, LayerShell.Edge.TOP, v.lower() in ("true", "1", "yes")),
        "anchored-bottom": lambda w, v: LayerShell.set_anchor(w, LayerShell.Edge.BOTTOM, v.lower() in ("true", "1", "yes")),
        "anchored-left": lambda w, v: LayerShell.set_anchor(w, LayerShell.Edge.LEFT, v.lower() in ("true", "1", "yes")),
        "anchored-right": lambda w, v: LayerShell.set_anchor(w, LayerShell.Edge.RIGHT, v.lower() in ("true", "1", "yes")),

        "margin-top": lambda w, v: LayerShell.set_margin(w, LayerShell.Edge.TOP, int(v)),
        "margin-bottom": lambda w, v: LayerShell.set_margin(w, LayerShell.Edge.BOTTOM, int(v)),
        "margin-left": lambda w, v: LayerShell.set_margin(w, LayerShell.Edge.LEFT, int(v)),
        "margin-right": lambda w, v: LayerShell.set_margin(w, LayerShell.Edge.RIGHT, int(v)),
    },
}

def _paned_add(parent, child):
    if parent.get_start_child() is None:
        parent.set_start_child(child)
    else:
        parent.set_end_child(child)


def _centerbox_add(parent, child):
    if parent.get_start_widget() is None:
        parent.set_start_widget(child)
    elif parent.get_center_widget() is None:
        parent.set_center_widget(child)
    else:
        parent.set_end_widget(child)


def _overlay_add(parent, child):
    if parent.get_child() is None:
        parent.set_child(child)
    else:
        parent.add_overlay(child)


child_adders = {
    "Paned": _paned_add,
    "CenterBox": _centerbox_add,
    "Overlay": _overlay_add,
    "Stack": lambda parent, child: parent.add_child(child),
    "Notebook": lambda parent, child: parent.append_page(child, None),
    "HeaderBar": lambda parent, child: parent.pack_start(child),
    "ActionBar": lambda parent, child: parent.pack_start(child),
}
