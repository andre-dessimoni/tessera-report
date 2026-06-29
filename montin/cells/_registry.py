"""
montin.cells._registry
========================
Maps a serialised ``cell_type`` (the cell class name) back to its class, so
:meth:`Cell.from_dict` can reconstruct the right subtype. Imported lazily by
``from_dict`` to avoid an import cycle with the cell modules.
"""

from __future__ import annotations

from montin.cells.base import Cell
from montin.cells.image import ImageCell
from montin.cells.image_slider import ImageSliderCell
from montin.cells.matplotlib import MatplotlibCell
from montin.cells.misc import (
    CodeCell,
    EmptyCell,
    HtmlCell,
    IframeCell,
    ListCell,
    MermaidCell,
    MetricCell,
)
from montin.cells.plotly import PlotlyCell
from montin.cells.table import TableCell
from montin.cells.tabulator import TabulatorCell
from montin.cells.text import TextCell

CELL_REGISTRY: dict[str, type[Cell]] = {
    cls.__name__: cls
    for cls in (
        TextCell,
        ImageCell,
        ImageSliderCell,
        MatplotlibCell,
        TableCell,
        TabulatorCell,
        ListCell,
        PlotlyCell,
        CodeCell,
        MetricCell,
        MermaidCell,
        HtmlCell,
        IframeCell,
        EmptyCell,
    )
}
