.. _script-api:

Script API
==========

``<Script>`` blocks have access to the following globals. GTK/GLib internals
are intentionally not exposed — use these helpers instead.

Widget access
-------------

.. function:: get(id) -> Widget

   Returns the ``Widget`` wrapper for the widget registered with ``id``.
   Raises an error if the id is not found.

.. class:: Widget

   Thin wrapper around a ``Gtk.Widget``.

   .. method:: set_property(key, value)

      Sets a GObject property on the underlying widget. Value is coerced
      automatically (same rules as XML attributes).

   .. method:: connect(signal, function)

      Connects a GTK signal to a Python callable.

      .. code-block:: python

         btn = get("my-button")
         btn.connect("clicked", lambda _: print("clicked"))

Events
------

.. function:: bind(event, func, *args)

   Registers a recurring callback. Currently supports one event type:

   ``"repeat"``
      Calls ``func()`` on a ``GLib`` timer. The third argument is the interval
      in seconds (``float``).

      .. code-block:: python

         bind("repeat", my_func, 0.5)  # every 500 ms

.. function:: killall()

   Cancels all active ``bind`` sources.

Example using ``bind("repeat", ...)``:

.. literalinclude:: ../examples/repeat.kiln
   :language: xml

Shell commands
--------------

.. function:: shell(cmd) -> str

   Runs ``cmd`` in a shell synchronously. Returns stdout as a stripped string.

.. function:: shell_async(cmd, callback=None)

   Runs ``cmd`` in a background daemon thread. When the command finishes,
   ``callback(result)`` is called on the GTK main thread via
   ``GLib.idle_add``. ``result`` is the stdout string (stripped).

Blueprints
----------

.. function:: get_blueprint(id) -> Blueprint

   Returns the :class:`Blueprint` registered with ``id``.
   Raises an error if not found. See :ref:`blueprints`.

.. class:: Blueprint

   .. method:: create(parent_id=None, **kwargs)

      Instantiates the blueprint. ``kwargs`` fill ``{key}`` placeholders in
      the template's attributes. If ``parent_id`` is given, the created
      widgets are attached to that widget instead of the blueprint's original
      parent.
