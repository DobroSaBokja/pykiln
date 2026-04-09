.. _widgets:

Widgets
=======

.. _standard-widgets:

Standard GTK widgets
--------------------

Any ``Gtk.*`` class name can be used directly as a tag. Attributes map to
GObject properties. Refer to the `GTK4 widget gallery
<https://docs.gtk.org/gtk4/visual_index.html>`_ for the full list of available
widgets and their properties.

.. code-block:: xml

   <Box orientation="horizontal" spacing="8">
       <Label label="Hello"/>
       <Button label="Click me"/>
   </Box>

.. _custom-widgets:

Custom widgets
--------------

Bar
~~~

A layer-shell window for creating panels, docks, and overlays. Extends
``Gtk.Window``.

.. code-block:: xml

   <Bar anchored-top="True" anchored-left="True" anchored-right="True">
       <!-- children -->
   </Bar>

.. literalinclude:: ../examples/bar.kiln
   :language: xml

Properties:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Property
     - Type
     - Description
   * - ``anchored-top``
     - bool
     - Anchor the bar to the top edge
   * - ``anchored-bottom``
     - bool
     - Anchor the bar to the bottom edge
   * - ``anchored-left``
     - bool
     - Anchor the bar to the left edge
   * - ``anchored-right``
     - bool
     - Anchor the bar to the right edge
   * - ``exclusive-zone``
     - bool
     - Reserve space so other windows don't overlap
   * - ``margin-top``
     - int
     - Top margin in pixels
   * - ``margin-bottom``
     - int
     - Bottom margin in pixels
   * - ``margin-left``
     - int
     - Left margin in pixels
   * - ``margin-right``
     - int
     - Right margin in pixels
   * - ``layer``
     - str
     - Layer-shell layer: ``background``, ``bottom``, ``top``, ``overlay``

Rectangle
~~~~~~~~~

A custom drawing widget that renders a filled rectangle.

.. code-block:: xml

   <Rectangle width-request="100" height-request="100" color="green"/>

Properties: ``color`` (CSS color string), ``width-request`` (int),
``height-request`` (int).

Circle
~~~~~~

A custom drawing widget that renders a filled circle.

.. code-block:: xml

   <Circle radius="50" color="yellow"/>

Properties: ``color`` (CSS color string), ``radius`` (float).

Anchor
~~~~~~

A layout widget that positions a single child at one of nine anchor points.
Expands to fill all available space.

.. code-block:: xml

   <Anchor anchor="top-left">
       <Rectangle width-request="50" height-request="50" color="red"/>
   </Anchor>

``anchor`` values: ``top-left``, ``top-center``, ``top-right``,
``center-left``, ``center``, ``center-right``, ``bottom-left``,
``bottom-center``, ``bottom-right``.

.. literalinclude:: ../examples/primitives.kiln
   :language: xml

Multiple children
-----------------

``Window``, ``ApplicationWindow``, and ``Bar`` all support multiple children
via an implicit ``Gtk.Overlay`` wrapper — the first child is the base layer,
and subsequent children are overlaid on top.
