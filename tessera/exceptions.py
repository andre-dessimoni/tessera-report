"""
tessera.exceptions
==================
Public exception hierarchy for the package.
"""


class HtmlSlidesError(Exception):
    """Base class for all tessera exceptions."""


class CellPlacementError(HtmlSlidesError):
    """
    Raised when a cell cannot be placed on the canvas.

    Cases:
    - col or row out of range (< 1 or > nrows/ncols)
    - col + colspan - 1 > ncols  or  row + rowspan - 1 > nrows
    - position already occupied by another cell
    """


class PluginNotDeclaredError(HtmlSlidesError):
    """
    Raised when a cell requires a plugin not declared in Deck.

    Example: add_code() without Plugin("highlight") in the plugins list.
    """


class ThemeNotFoundError(HtmlSlidesError):
    """
    Raised when the folder for the specified theme is not found.
    """


class InvalidDataError(HtmlSlidesError):
    """
    Raised when the type or format of data passed to an add_* method
    is invalid or cannot be interpreted.

    Example: add_table() receives an unsupported type, or a malformed CSV string.
    """
