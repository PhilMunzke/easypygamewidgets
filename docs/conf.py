import os
import sys

sys.path.insert(0, os.path.abspath(("..")))

project = "EasyPygameWidgets"
author = "Phil Munzke"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "notfound.extension"
]
release = "26.51.1"
html_theme = "furo"
html_title = "EasyPygameWidgets"
autodoc_class_signature = "separated"
autodoc_preserver_defaults = True
add_module_names = False
html_static_path = ["static"]
html_css_files = ["custom.css"]