.. _kiln-format:

.kiln File Format
=================

``.kiln`` files are XML. Tags map to GTK4 widget class names; attributes map to
GObject properties.

Widget tags
-----------

Any ``Gtk.*`` class name works directly as a tag (e.g. ``<Label>``, ``<Box>``,
``<Button>``). A small set of tags have custom constructors — see
:ref:`custom-widgets`.

Attributes
----------

Attribute values are strings in XML and are automatically coerced to the
correct GObject property type (``int``, ``float``, ``bool``, ``Gdk.RGBA``,
enum). Boolean values accept ``true``, ``1``, or ``yes``.

Five common attributes apply to all widgets:

``margin``
   Sets all four margins to the same value (integer pixels).

``align``
   Sets ``halign`` and/or ``valign`` in one attribute.

   Two-axis values (set both): ``top-left``, ``top-center``, ``top-right``,
   ``center-left``, ``center``, ``center-right``, ``bottom-left``,
   ``bottom-center``, ``bottom-right``.

   Single-axis values (set one, leave the other unchanged):
   ``top``, ``bottom``, ``left``, ``right``, ``center-h``, ``center-v``.

``expand``
   Requests extra space from the parent layout. Useful inside ``Box`` and
   similar containers. Values: ``horizontal``, ``vertical``, ``all``.

``class``
   Adds a CSS class to the widget (usable in ``<Style>`` blocks).

``id``
   Registers the widget in the script environment and sets its CSS name.
   Required to access the widget from ``<Script>`` blocks via :func:`get`.

Special tags
------------

``<Script>``
   Embedded Python block. Executed after the full widget tree is built.
   Has access to the :doc:`script-api`.

``<Style>``
   Inline CSS applied globally to the default display via ``Gtk.CssProvider``.

``<Property>``
   Sets a property on the **parent** widget using ``key=value`` syntax.
   Useful for code readabilty.

   .. code-block:: xml

      <Bar>
          <Property>anchored-top=True</Property>
      </Bar>

``<Import path="...">``
   Loads a ``.kiln`` library file. Path is resolved relative to the current
   file. The imported file must have ``<Library>`` as its root tag. See
   :ref:`libraries`.

``<Blueprint id="...">``
   Defines a reusable widget template. Not rendered immediately. Retrieved in
   scripts via :func:`get_blueprint`. See :ref:`blueprints`.

Example with multiple features
-------------------------------

.. literalinclude:: ../examples/features.kiln
   :language: xml
