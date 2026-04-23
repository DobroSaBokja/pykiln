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

   .. method:: get_property(key) -> value

      Returns the current value of a GObject property. Enum values are returned
      as their nick string (e.g. ``"horizontal"``).

   .. method:: connect(signal, function)

      Connects a GTK signal to a Python callable.

      .. code-block:: python

         btn = get("my-button")
         btn.connect("clicked", lambda _: print("clicked"))

   .. method:: destroy()

      Removes the widget from its parent and unregisters it from the widget
      dictionary.

Events
------

.. function:: bind(event, func, *args, **kwargs) -> Event

   Registers a recurring or background callback. Supported event types:

   ``"repeat"``
      Calls ``func()`` on a ``GLib`` timer. The third argument is the interval
      in seconds (``int``). Pass ``miliseconds=True`` to treat the interval as
      milliseconds instead. Returns an :class:`Event` that can be used to
      cancel the timer. If ``func()`` returns ``False`` the timer is removed
      automatically.

      .. code-block:: python

         e = bind("repeat", my_func, 1)       # every second
         e = bind("repeat", my_func, 500, miliseconds=True)  # every 500 ms
         e.kill()  # cancel

   ``"idle"``
      Runs ``func(*args)`` in a background daemon thread via
      ``threading.Thread``. Any callable arguments in ``*args`` are
      automatically wrapped so that calling them dispatches back to the GTK
      main thread via ``GLib.idle_add``. Useful for blocking I/O that should
      not freeze the UI.

.. class:: Event

   Returned by :func:`bind`. Represents an active timer.

   .. method:: kill()

      Cancels the timer and removes it from the active event list.

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
