"""Sphinx configuration for the Coriolis documentation."""

import html
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

html_theme = "furo"
html_static_path = ["_static"]
html_title = "Coriolis Documentation"
html_logo = "_static/images/coriolis-logo.svg"
html_favicon = "_static/images/coriolis-logo.svg"

# WordPress slugs that do not match the scraped filename.
_SLUG_ALIASES = {
    "cloudstack-as-a-destination-cloud": "cloudstack-as-a-destination-cloud-2",
    "minion-pools---creation-and-management": "minion-pools-creation-and-management",
}

_DOCS_DIR = Path(__file__).parent
_DOC_STEMS = {path.stem for path in _DOCS_DIR.glob("*.md")} - set(exclude_patterns)

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


def _rewrite_link(match: re.Match) -> str:
    slug = match.group(1).lower()
    slug = _SLUG_ALIASES.get(slug, slug)
    if slug not in _DOC_STEMS:
        return match.group(0)
    return f"{slug}.md{_anchor_to_myst(match.group(2) or '')}"


def _rewrite_source(app, docname, source):
    text = html.unescape(source[0])
    source[0] = _PAGE_LINK.sub(_rewrite_link, text)


def setup(app):
    app.connect("source-read", _rewrite_source)
