"""Sphinx configuration for the Coriolis documentation."""

import html

project = "Coriolis"
author = "Cloudbase Solutions"
copyright = "Cloudbase Solutions"
release = ""

extensions = ["myst_parser"]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_image",
    "replacements",
    "smartquotes",
]
myst_heading_anchors = 4
# Scraped WordPress pages often jump from H1 to H3.
suppress_warnings = ["myst.header"]

source_suffix = {".md": "markdown"}
root_doc = "index"
exclude_patterns = [
    "deprecated/**",
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/._*",
]

html_theme = "shibuya"
html_static_path = ["_static"]
html_css_files = ["overview-logos.css", "lightbox.css"]
html_js_files = ["lightbox.js"]
html_title = "Coriolis Documentation"
html_logo = "_static/images/coriolis-logo.svg"
html_favicon = "_static/images/coriolis-logo.svg"


def _rewrite_source(app, docname, source):
    text = html.unescape(source[0])
    if "/" in docname:
        text = text.replace("](_static/", "](../_static/")
        text = text.replace("(_static/", "(../_static/")
    source[0] = text


def setup(app):
    app.connect("source-read", _rewrite_source)
