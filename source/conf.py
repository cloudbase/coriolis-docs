"""Sphinx configuration for the Coriolis documentation."""

import html
import os
import re
from pathlib import Path

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
myst_heading_anchors = 3
# Scraped WordPress pages often jump from H1 to H3.
suppress_warnings = ["myst.header"]

source_suffix = {".md": "markdown"}
root_doc = "index"
exclude_patterns = [
    "coriolis.md",
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["overview-logos.css"]
html_title = "Coriolis Documentation"
html_logo = "_static/images/coriolis-logo.svg"
html_favicon = "_static/images/coriolis-logo.svg"
html_theme_options = {
    # Show section titles only. Pages under a section stay hidden until
    # that section is expanded, matching the Read the Docs navigation.
    "collapse_navigation": True,
    "navigation_depth": 2,
    "sticky_navigation": True,
}

# WordPress slugs that do not match the scraped filename.
_SLUG_ALIASES = {
    "cloudstack-as-a-destination-cloud": "cloudstack-as-a-destination-cloud-2",
    "minion-pools---creation-and-management": "minion-pools-creation-and-management",
}

_DOCS_DIR = Path(__file__).parent
# stem -> docname, for pages that live in a section folder.
_SLUG_TO_DOC = {}
for _path in _DOCS_DIR.rglob("*.md"):
    _rel = _path.relative_to(_DOCS_DIR).as_posix()
    if _path.name == "index.md" or _rel in exclude_patterns:
        continue
    _SLUG_TO_DOC[_path.stem] = _rel[:-3]

# Page URL only: optional trailing slash and a heading anchor. Extra path
# segments (attachment pages, downloads) are left unchanged.
_PAGE_LINK = re.compile(
    r"https?://(?:www\.)?cloudbase\.it/"
    r"([a-z0-9-]+)"
    r"/?"
    r"(#[A-Za-z0-9_\-]+)?"
    r"(?=[\s\)\"<]|$)",
    re.IGNORECASE,
)


def _anchor_to_myst(anchor: str) -> str:
    if not anchor:
        return ""
    return "#" + anchor[1:].replace("_", "-").lower()


def _relative_doc_link(docname: str, target: str, anchor: str) -> str:
    start = os.path.dirname(docname) or "."
    return os.path.relpath(f"{target}.md", start=start) + anchor


def _rewrite_source(app, docname, source):
    text = html.unescape(source[0])
    if "/" in docname:
        text = text.replace("](_static/", "](../_static/")
        text = text.replace("(_static/", "(../_static/")

    def rewrite_link(match: re.Match) -> str:
        slug = _SLUG_ALIASES.get(match.group(1).lower(), match.group(1).lower())
        target = _SLUG_TO_DOC.get(slug)
        if target is None:
            return match.group(0)
        return _relative_doc_link(docname, target, _anchor_to_myst(match.group(2) or ""))

    source[0] = _PAGE_LINK.sub(rewrite_link, text)


def setup(app):
    app.connect("source-read", _rewrite_source)
