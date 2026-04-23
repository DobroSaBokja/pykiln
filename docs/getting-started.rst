Getting Started
===============

Dependencies
------------

- Python 3.14+
- PyGObject (``pygobject``)
- GTK 4.0
- gtk4-layer-shell (``libgtk4-layer-shell.so`` must be installed on the system)

Running
-------

.. code-block:: sh

   kiln path/to/file.kiln

Pass the path to any ``.kiln`` file. PyKiln monitors the file for changes and
hot-reloads the UI automatically.

Your first .kiln file
---------------------

.. literalinclude:: ../examples/hello-world.kiln
   :language: xml

Tags map to GTK4 widget class names. Attributes map to GObject properties.
See :doc:`kiln-format` for the full reference.
