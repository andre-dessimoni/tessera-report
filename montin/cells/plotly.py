"""montin.cells.plotly — PlotlyCell"""

from __future__ import annotations

from typing import TYPE_CHECKING

from montin.cells.base import Cell, CellParams

if TYPE_CHECKING:
    import jinja2
    import plotly.graph_objects as go


class PlotlyCell(Cell):
    """
    Interactive Plotly figure embedded as JSON.
    Effective overflow default: False.
    Requires Plugins.Plotly().
    """

    def __init__(self, fig: "go.Figure", params: CellParams,
                 save_source: bool = False) -> None:
        super().__init__(params)
        self.fig      = fig
        self.save_source = save_source
        self.fig_json = self._serialize(fig)

    def _serialize(self, fig: "go.Figure") -> str:
        """Serialize the Figure to JSON for template injection."""
        try:
            return fig.to_json()
        except Exception as exc:
            from montin.exceptions import InvalidDataError
            raise InvalidDataError(f"Failed to serialize Plotly figure: {exc}") from exc

    def render(self, env: "jinja2.Environment") -> str:
        return env.get_template("cell_plotly.html").render(cell=self)

    def _to_content(self, *, embed: bool = True) -> dict:
        # fig_json is already a JSON string and is all the template needs.
        return {"fig_json": self.fig_json, "save_source": self.save_source}

    @classmethod
    def _from_content(cls, content, params):
        # Restore fig_json directly (no plotly import / re-serialisation needed).
        obj = cls._raw_new(params)
        obj.fig = None
        obj.save_source = content.get("save_source", False)
        obj.fig_json = content["fig_json"]
        return obj

    def __repr__(self) -> str:
        return (
            f"PlotlyCell(ID={self.params.cell_id!r})"
            f" at row={self.params.row}, col={self.params.col}"
        )