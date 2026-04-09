Advanced
========

.. _libraries:

Library files and ``<Import>``
-------------------------------

A library file is a ``.kiln`` file whose root tag is ``<Library>``. It can
contain any widget definitions and ``<Script>`` blocks.

.. literalinclude:: ../examples/library.kiln
   :language: xml

Import it into another file with ``<Import path="...">``  The path is resolved
relative to the importing file's directory (or as an absolute path).

.. literalinclude:: ../examples/import.kiln
   :language: xml

Key points:

- Scripts inside a library have full access to the importing file's widget
  registry — ``get("blue-rect")`` in the library example resolves a widget
  defined in ``import.kiln``.
- Scripts in the importing file can access widgets defined inside the library
  (e.g. ``get("red-rect")``).
- The library root tag **must** be ``<Library>``; any other root tag is an
  error.

.. _blueprints:

Blueprints
----------

A ``<Blueprint>`` defines a reusable widget template. It is not rendered
immediately; instead it is retrieved in a script and instantiated one or more
times.

.. literalinclude:: ../examples/blueprint.kiln
   :language: xml

Template placeholders
~~~~~~~~~~~~~~~~~~~~~

Attribute values in a blueprint may contain ``{key}`` placeholders. When
:meth:`Blueprint.create` is called with keyword arguments, every occurrence of
``{key}`` in the element tree is replaced before building.

.. code-block:: python

   blueprint = get_blueprint("rect-blueprint")
   blueprint.create(anchor="top-left", color="red")

``parent_id``
~~~~~~~~~~~~~

By default ``create()`` attaches new widgets to the blueprint's original
parent context. Pass ``parent_id="some-id"`` to attach them to a different
widget instead.
