# Kiln
## A low-level alternative to Quickshell, using Python, XML and Gtk
PyKiln allows you to write quick-and-dirty XML, with `<Script>` and `<Style>` tags similar to HTML, with Python and CSS respectively.
`<Script>` tags can execute any Python code, meaning Kiln has integration with anything that has Python integration. It
also comes with a thin wrapper to simplify interacting with Gtk Widgets.
## Note
This repo has become AI slopified (i have used Claude Code quite a bit recently). I feel bad about this and am against AI and especialy AI "art", but this project is for my personal use only and i don't care about the quality of code. If you are super-against AI, don't use this.
## Installation

**Requirements:** Python 3.14+, PyGObject, GTK 4.0, gtk4-layer-shell

Run the install script as root:
```sh
curl -s https://raw.githubusercontent.com/DobroSaBokja/pykiln/prod/install.sh | sudo bash
```
Then run a `.kiln` file with:

```sh
kiln path/to/file.kiln
```

## Documentation
Full documentation is available at: https://pykiln.readthedocs.io

## Examples
Examples are in the `examples` directory in the repository.
