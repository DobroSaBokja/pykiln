Examples
========

All examples are in the ``examples/`` directory and can be run with:

.. code-block:: sh

   python main.py examples/<file>.kiln

Hello World
-----------

Minimal window with a label.

.. literalinclude:: ../examples/hello-world.kiln
   :language: xml

Bar
---

Layer-shell panel anchored to the top edge.

.. literalinclude:: ../examples/bar.kiln
   :language: xml

- ``anchored-top/left/right`` anchors the bar to those screen edges.

Features
--------

Demonstrates ``<Property>``, ``<Style>``, and ``<Script>`` together.

.. literalinclude:: ../examples/features.kiln
   :language: xml

- ``<Property>`` sets ``anchored-top`` on the parent ``<Bar>``.
- ``<Style>`` injects CSS targeting the ``button`` selector globally.
- ``<Script>`` retrieves the button by id and wires up the ``clicked`` signal.

Primitives
----------

Custom ``Rectangle`` and ``Circle`` widgets positioned with ``Anchor``.

.. literalinclude:: ../examples/primitives.kiln
   :language: xml

- ``Anchor`` expands to fill the window; children are placed at the named
  anchor point.
- ``color`` accepts any CSS color string.

Repeat
------

``bind("repeat", ...)`` cycles a rectangle's color every second.

.. literalinclude:: ../examples/repeat.kiln
   :language: xml

- ``bind("repeat", func, interval)`` fires ``func()`` on a GLib timer.
- ``set_property("color", ...)`` updates the widget live.

Import and Library
------------------

``import.kiln`` pulls in ``library.kiln``; both files share the same widget
registry.

Library:

.. literalinclude:: ../examples/library.kiln
   :language: xml

Importer:

.. literalinclude:: ../examples/import.kiln
   :language: xml

- The library's script can call ``get("blue-rect")`` — a widget defined in
  the importing file.
- The importer's script can call ``get("red-rect")`` — a widget defined in
  the library.

Blueprint
---------

A single blueprint instantiated four times with different ``anchor`` and
``color`` values.

.. literalinclude:: ../examples/blueprint.kiln
   :language: xml

- ``{anchor}`` and ``{color}`` are template placeholders replaced by
  ``blueprint.create(anchor=..., color=...)``.
