import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "PyKiln"
copyright = "PyKiln contributors"
author = "PyKiln contributors"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "myst_parser",
]

html_theme = "sphinx_rtd_theme"  # requires sphinx-rtd-theme package (pip install sphinx-rtd-theme)
# html_theme = "nature"  # fallback if sphinx-rtd-theme is not available
html_static_path = []

autodoc_member_order = "bysource"
