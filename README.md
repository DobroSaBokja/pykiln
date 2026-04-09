# Kiln
## A low-level alternative to Quickshell, using Python, XML and Gtk
PyKiln allows you to write quick-and-dirty XML, with `<Script>` and `<Style>` tags similar to HTML, with Python and CSS respectively.
`<Script>` tags can execute any Python code, meaning Kiln has integration with anything that has Python integration. It
also comes with a thin wrapper to simplify interacting with Gtk Widgets.
## Installation

**Requirements:** Python 3.14+, PyGObject, GTK 4.0, gtk4-layer-shell

Run the install script as root:
```sh
sudo bash <(curl -s https://raw.githubusercontent.com/DobroSaBokja/pykiln/prod/install.sh)
```
Then run a `.kiln` file with:

```sh
kiln path/to/file.kiln
```

## Documentation
Full documentation is available at: https://pykiln.readthedocs.io

## Examples
Examples are in the `examples` directory in the repository.
