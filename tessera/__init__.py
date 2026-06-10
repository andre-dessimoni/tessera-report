"""
tessera
=======
Python library for generating self-contained HTML slideshows for
technical engineering documents.

Basic usage::

    from tessera import HTMLSlides, Plugin, SlideDefaults, CellDefaults

    slides = HTMLSlides(title="My Report")
    slide = slides.add_slide("Results", nrows=1, ncols=2)
    slide.add_text("Hello, world!")
    slides.write("my-report")
"""

from importlib.metadata import PackageNotFoundError, version

from tessera.core.slides import CellDefaults, HTMLSlides, Plugin, SlideDefaults
from tessera.exceptions import (
    CellPlacementError,
    HtmlSlidesError,
    InvalidDataError,
    PluginNotDeclaredError,
    ThemeNotFoundError,
)

try:
    __version__ = version("py-tessera")
except PackageNotFoundError:  # running from source without installing
    __version__ = "0.0.0.dev"

__all__ = [
    "HTMLSlides",
    "Plugin",
    "SlideDefaults",
    "CellDefaults",
    "HtmlSlidesError",
    "CellPlacementError",
    "PluginNotDeclaredError",
    "ThemeNotFoundError",
    "InvalidDataError",
    "__version__",
]
