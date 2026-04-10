from gi.repository import Gtk, GObject, Gdk, Graphene, Gsk
from gi.repository import Gtk4LayerShell as LayerShell

def _set_all_margins(widget, margin):
    widget.set_margin_start(margin)
    widget.set_margin_end(margin)
    widget.set_margin_top(margin)
    widget.set_margin_bottom(margin)

def _apply_css_class(w: Gtk.Widget, v: str):
    w.add_css_class(v)

class Bar(Gtk.Window):
    __gtype_name__ = "Bar"

    @GObject.Property(type=int, default=0)
    def corner_radius(self):
        return self._corner_radius
    
    @corner_radius.setter
    def corner_radius(self, value: int):
        self._corner_radius = value
        if value > 0:
            css = Gtk.CssProvider()
            css.load_from_string("window { background: transparent; }")
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(), css,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

    @GObject.Property(type=bool, default=False)
    def anchored_top(self):
        return self._anchored_top
    
    @anchored_top.setter
    def anchored_top(self, value: bool):
        self._anchored_top = value
        LayerShell.set_anchor(self, LayerShell.Edge.TOP, value)

    @GObject.Property(type=bool, default=False)
    def anchored_bottom(self):
        return self._anchored_bottom
    
    @anchored_bottom.setter
    def anchored_bottom(self, value: bool):
        self._anchored_bottom = value
        LayerShell.set_anchor(self, LayerShell.Edge.BOTTOM, value)

    @GObject.Property(type=bool, default=False)
    def anchored_left(self):
        return self._anchored_left
    
    @anchored_left.setter
    def anchored_left(self, value: bool):
        self._anchored_left = value
        LayerShell.set_anchor(self, LayerShell.Edge.LEFT, value)

    @GObject.Property(type=bool, default=False)
    def anchored_right(self):
        return self._anchored_right
    
    @anchored_right.setter
    def anchored_right(self, value: bool):
        self._anchored_right = value
        LayerShell.set_anchor(self, LayerShell.Edge.RIGHT, value)

    @GObject.Property(type=bool, default=False)
    def exclusive_zone(self):
        return self._exclusive_zone
    
    @exclusive_zone.setter
    def exclusive_zone(self, value: bool):
        self._exclusive_zone = value
        if value:
            LayerShell.auto_exclusive_zone_enable(self)
        else:
            LayerShell.set_exclusive_zone(self, 0)

    @GObject.Property(type=int, default=0)
    def margin_top(self):
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value: int):
        self._margin_top = value
        LayerShell.set_margin(self, LayerShell.Edge.TOP, value)

    @GObject.Property(type=int, default=0)
    def margin_bottom(self):
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, value: int):
        self._margin_bottom = value
        LayerShell.set_margin(self, LayerShell.Edge.BOTTOM, value)

    @GObject.Property(type=int, default=0)
    def margin_left(self):
        return self._margin_left

    @margin_left.setter
    def margin_left(self, value: int):
        self._margin_left = value
        LayerShell.set_margin(self, LayerShell.Edge.LEFT, value)

    @GObject.Property(type=int, default=0)
    def margin_right(self):
        return self._margin_right

    @margin_right.setter
    def margin_right(self, value: int):
        self._margin_right = value
        LayerShell.set_margin(self, LayerShell.Edge.RIGHT, value)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._margin_top = 0
        self._margin_bottom = 0
        self._margin_left = 0
        self._margin_right = 0
        self.set_decorated(False)

        LayerShell.init_for_window(self)
        LayerShell.set_layer(self, LayerShell.Layer.TOP)

class Rectangle(Gtk.Widget):
    __gtype_name__ = "Rectangle"

    @GObject.Property(type=Gdk.RGBA)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.queue_draw()

    def do_measure(self, orientation, _for_size):
        if orientation == Gtk.Orientation.HORIZONTAL:
            size = self.get_property("width-request")
        else:
            size = self.get_property("height-request")
        size = max(size, 0)
        return (size, size, -1, -1)

    def do_snapshot(self, snapshot: Gtk.Snapshot):
        bounds = Graphene.Rect().init(0, 0, self.get_width(), self.get_height())
        snapshot.append_color(self.props.color, bounds)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._color = Gdk.RGBA()
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.START)

class Circle(Gtk.Widget):
    __gtype_name__ = "Circle"

    color = GObject.property(type=Gdk.RGBA)
    radius = GObject.property(type=float)

    def do_measure(self, orientation, _for_size):
        size = int(self.props.radius * 2)
        return (size, size, -1, -1)

    def do_snapshot(self, snapshot):
        r = self.props.radius
        bounds = Graphene.Rect().init(0, 0, r * 2, r * 2)
        rounded = Gsk.RoundedRect()
        rounded.init_from_rect(bounds, r)
        snapshot.push_rounded_clip(rounded)
        snapshot.append_color(self.props.color, bounds)
        snapshot.pop()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.START)

class AnchorPosition(GObject.GEnum):
    __gtype_name__ = "AnchorPosition"
    TOP_LEFT     = 0
    TOP_CENTER   = 1
    TOP_RIGHT    = 2
    CENTER_LEFT  = 3
    CENTER       = 4
    CENTER_RIGHT = 5
    BOTTOM_LEFT  = 6
    BOTTOM_CENTER = 7
    BOTTOM_RIGHT = 8

_ANCHOR_MAP = {
    AnchorPosition.TOP_LEFT:      (Gtk.Align.START, Gtk.Align.START),
    AnchorPosition.TOP_CENTER:    (Gtk.Align.CENTER, Gtk.Align.START),
    AnchorPosition.TOP_RIGHT:     (Gtk.Align.END,   Gtk.Align.START),
    AnchorPosition.CENTER_LEFT:   (Gtk.Align.START, Gtk.Align.CENTER),
    AnchorPosition.CENTER:        (Gtk.Align.CENTER, Gtk.Align.CENTER),
    AnchorPosition.CENTER_RIGHT:  (Gtk.Align.END,   Gtk.Align.CENTER),
    AnchorPosition.BOTTOM_LEFT:   (Gtk.Align.START, Gtk.Align.END),
    AnchorPosition.BOTTOM_CENTER: (Gtk.Align.CENTER, Gtk.Align.END),
    AnchorPosition.BOTTOM_RIGHT:  (Gtk.Align.END,   Gtk.Align.END),
}

class Anchor(Gtk.Widget):
    __gtype_name__ = "Anchor"

    @GObject.Property(type=AnchorPosition, default=AnchorPosition.TOP_LEFT)
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = value
        self.queue_allocate()

    def do_measure(self, orientation, for_size):
        return (0, 0, -1, -1)

    def do_size_allocate(self, width, height, baseline):
        child = self.get_first_child()
        if not child:
            return
        halign, valign = _ANCHOR_MAP[self._anchor]

        _, nat_w, _, _ = child.measure(Gtk.Orientation.HORIZONTAL, height)
        _, nat_h, _, _ = child.measure(Gtk.Orientation.VERTICAL, width)
        child_w = min(nat_w, width)
        child_h = min(nat_h, height)

        if halign == Gtk.Align.START:
            x = 0
        elif halign == Gtk.Align.CENTER:
            x = (width - child_w) // 2
        elif halign == Gtk.Align.END:
            x = width - child_w
        else:
            x, child_w = 0, width

        if valign == Gtk.Align.START:
            y = 0
        elif valign == Gtk.Align.CENTER:
            y = (height - child_h) // 2
        elif valign == Gtk.Align.END:
            y = height - child_h
        else:
            y, child_h = 0, height

        alloc = Gdk.Rectangle()
        alloc.x = x
        alloc.y = y
        alloc.width = child_w
        alloc.height = child_h
        child.size_allocate(alloc, baseline)

    def do_dispose(self):
        child = self.get_first_child()
        if child:
            child.unparent()
        super().do_dispose()

    def append(self, child):
        child.set_parent(self)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._anchor = AnchorPosition.TOP_LEFT
        self.set_hexpand(True)
        self.set_vexpand(True)

widget_mapping = {
    "Window": lambda context: Gtk.Window(application=context.app),
    "ApplicationWindow": lambda context: Gtk.ApplicationWindow(application=context.app),
    "Bar": lambda context: Bar(application=context.app),
    "Rectangle": lambda _: Rectangle(),
    "Circle": lambda _: Circle(),
    "Anchor": lambda _: Anchor(),
}

_LAYER_MAP = {
    "background": LayerShell.Layer.BACKGROUND,
    "bottom":     LayerShell.Layer.BOTTOM,
    "top":        LayerShell.Layer.TOP,
    "overlay":    LayerShell.Layer.OVERLAY,
}

def _set_bar_layer(widget, value: str):
    if value not in _LAYER_MAP:
        import lib
        lib.throw_error("unknown layer value '" + value + "'; expected one of: " + ", ".join(_LAYER_MAP))
    LayerShell.set_layer(widget, _LAYER_MAP[value])

attribute_handlers = {
    "common": {
        "margin": _set_all_margins,
        "class": _apply_css_class,
    },
    "Bar": {
        "layer": _set_bar_layer,
    },
}

def _window_add(parent, child):
    existing = parent.get_child()
    if existing is None:
        overlay = Gtk.Overlay()
        overlay.set_child(child)
        parent.set_child(overlay)
        if isinstance(parent, Bar) and parent._corner_radius > 0:
            r = parent._corner_radius
            overlay.add_css_class("bar-rounded")
            css = Gtk.CssProvider()
            css.load_from_string(f".bar-rounded {{ border-radius: {r}px; }}")
            overlay.get_style_context().add_provider(
                css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
    elif isinstance(existing, Gtk.Overlay):
        existing.add_overlay(child)



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
    "Window": _window_add,
    "ApplicationWindow": _window_add,
    "Bar": _window_add,
    "Paned": _paned_add,
    "CenterBox": _centerbox_add,
    "Overlay": _overlay_add,
    "Stack": lambda parent, child: parent.add_child(child),
    "Notebook": lambda parent, child: parent.append_page(child, None),
    "HeaderBar": lambda parent, child: parent.pack_start(child),
    "ActionBar": lambda parent, child: parent.pack_start(child),
}
