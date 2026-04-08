# PyKiln

Declarative GTK4 UI builder — define desktop app interfaces in `.kiln` (XML) files with embedded Python scripting, built with Python + PyGObject. Targets Wayland via gtk4-layer-shell.

## Architecture

- **main.py** — Entry point. Loads `libgtk4-layer-shell.so` via ctypes, initializes GTK4 and layer-shell GI bindings, parses the `.kiln` file, creates a `Gtk.Application`, and on activate builds the widget tree + runs scripts.
- **xml_parser.py** — Thin wrapper around `xml.etree.ElementTree`; `parse(path)` returns the root `Element`.
- **widget_builder.py** — `build(element, context)` recursively walks the XML tree depth-first and constructs GTK4 widgets. Handles:
  - `<Script>` tags — collects their CDATA text into `scripts.scripts` (not a widget).
  - Known tags — instantiated via `factories.widget_mapping`.
  - Unknown tags — falls back to `getattr(Gtk, tag)()`, so any `Gtk.*` class can be used directly as an XML tag (e.g. `<Label>`, `<Box>`).
  - Attributes — resolved in order: `id` (registers widget in `scripts.widget_dictionary`), tag-specific handler in `factories.attribute_handlers[tag]`, common handler in `factories.attribute_handlers["common"]`, then fallback `widget.set_property()` with automatic type coercion via `convert_value()`.
  - Child attachment — uses `parent.append()` if available, else `parent.set_child()`, else errors.
- **factories.py** — Two registries:
  - `widget_mapping`: tag name → `lambda context: Gtk.Widget(...)` for widgets that need special construction (currently just `Window` which requires the `application` kwarg).
  - `attribute_handlers`: nested dict keyed by tag name (or `"common"`), mapping attribute names to `lambda widget, value` setters for attributes that need custom logic beyond `set_property()`.
- **scripts.py** — Embedded scripting engine. Collects `<Script>` CDATA blocks during the build phase, then `run_scripts()` executes each with `exec()`. Scripts have access to:
  - `get(id)` — retrieves a widget by its `id` attribute from `widget_dictionary`.
- **lib.py** — Shared utilities:
  - `Context` dataclass — carries `app` (`Gtk.Application`), `parent_tag` (str), and `parent` (optional `Gtk.Widget`) through the recursive build.
  - `throw_error(message)` — prints `ERROR: <message>` and calls `exit(1)`.

## .kiln file format

XML-based layout files with the `.kiln` extension. Tags map to GTK4 widget class names. Attributes map to widget properties. Inline Python is embedded in `<Script>` tags using CDATA:

```xml
<Window>
    <Label text="Hello" id="label"></Label>
    <Script><![CDATA[
        label = get("label")
        label.set_text("Updated text")
    ]]>
    </Script>
</Window>
```

## Build & execution flow

1. `main.py` parses the `.kiln` file into an ElementTree.
2. On GTK `activate`, `widget_builder.build()` walks the tree depth-first, creating widgets and registering `id`-tagged ones.
3. `<Script>` blocks are collected (not executed) during the build.
4. After the full tree is built, `scripts.run_scripts()` executes all collected scripts in order.
5. The root window is presented.

## Running

```sh
python main.py
```

Currently hardcoded to load `test.kiln`. Requires `libgtk4-layer-shell.so` installed on the system.

## Dependencies

- Python 3.14+
- PyGObject (`pygobject`)
- GTK 4.0
- gtk4-layer-shell
- A `.venv` virtualenv is present in the project root.

## Dev notes

- No package manager config (no pyproject.toml/setup.py) — run directly.
- No tests yet.
- To add a new widget type that needs special construction: add an entry to `widget_mapping` in `factories.py`. Otherwise, any `Gtk.*` class works automatically as an XML tag.
- To add a custom attribute handler: add an entry under the tag name (or `"common"`) in `attribute_handlers` in `factories.py`.
- `convert_value()` in `widget_builder.py` handles automatic coercion of XML string values to the correct GObject property type (int, float, bool, enum).
