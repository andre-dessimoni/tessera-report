"""
tessera.cells.misc
==================
Remaining cell types: list, code, metric, mermaid, html, iframe, empty.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tessera.cells.base import Cell, CellParams

if TYPE_CHECKING:
    import jinja2


class ListCell(Cell):
    """Bullet or numbered list, with nested sub-levels."""

    def __init__(self, items: list[Any], ordered: bool, params: CellParams) -> None:
        super().__init__(params)
        self.items   = items
        self.ordered = ordered

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_list.html").render(cell=self)


class CodeCell(Cell):
    """
    Code block with syntax highlighting.
    Effective copy_button default: True.
    Requires Plugin('highlight').
    """

    def __init__(self, code: str, language: str, params: CellParams) -> None:
        super().__init__(params)
        self.code     = code
        self.language = language

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_code.html").render(cell=self)


class MetricCell(Cell):
    """
    KPI card: large value + label + optional delta.
    delta > 0 → green; delta < 0 → red; None → hidden.
    Effective overflow default: False.
    """

    def __init__(
        self,
        value: int | float | str,
        label: str,
        delta: int | float | str | None,
        delta_label: str,
        params: CellParams,
    ) -> None:
        super().__init__(params)
        self.value       = value
        self.label       = label
        self.delta       = delta
        self.delta_label = delta_label

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_metric.html").render(cell=self)


class MermaidCell(Cell):
    """
    Mermaid diagram (flowchart, sequenceDiagram, architecture, etc.).
    Effective overflow default: False.
    Requires Plugin('mermaid').
    """

    def __init__(self, diagram: str, params: CellParams) -> None:
        super().__init__(params)
        self.diagram = diagram

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_mermaid.html").render(cell=self)


class HtmlCell(Cell):
    """Raw HTML injected without escaping."""

    def __init__(self, content: str, params: CellParams) -> None:
        super().__init__(params)
        self.content = content

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_html.html").render(cell=self)


class IframeCell(Cell):
    """
    Embed external content via <iframe>.
    Requires an internet connection.
    Effective overflow default: False.
    """

    def __init__(self, url: str, params: CellParams) -> None:
        super().__init__(params)
        self.url = url

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_iframe.html").render(cell=self)


class EmptyCell(Cell):
    """Empty cell — reserves grid space without rendering any content."""

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_empty.html").render(cell=self)
