"""Tests for ``Slide.add_plotly`` loading a figure from a saved HTML file."""

import json
import sys

import pytest

from montin import Deck, Plugins
from montin.cells.plotly import PlotlyCell, _extract_figure_json
from montin.exceptions import InvalidDataError

pytest.importorskip("plotly")
import plotly.graph_objects as go  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def fig():
    return go.Figure(data=[go.Bar(x=["a", "b", "c"], y=[7, 11, 13])])


@pytest.fixture
def html_file(tmp_path, fig):
    p = tmp_path / "chart.html"
    fig.write_html(str(p))
    return p


def _plotly_deck():
    return Deck(title="P", plugins=[Plugins.Plotly()])


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def test_extract_figure_json_round_trips_trace_data(html_file):
    extracted = json.loads(_extract_figure_json(html_file.read_text(encoding="utf-8")))
    assert extracted["data"][0]["y"] == [7, 11, 13]
    assert "layout" in extracted


def test_extract_raises_on_non_plotly_html():
    with pytest.raises(InvalidDataError):
        _extract_figure_json("<html><body>no figure here</body></html>")


# ---------------------------------------------------------------------------
# add_plotly with a path
# ---------------------------------------------------------------------------

def test_add_plotly_from_html_path(html_file):
    deck = _plotly_deck()
    cell = deck.add_slide("S").add_plotly(str(html_file))
    assert isinstance(cell, PlotlyCell)
    assert json.loads(cell.fig_json)["data"][0]["y"] == [7, 11, 13]


def test_add_plotly_from_pathlib_path(html_file):
    deck = _plotly_deck()
    cell = deck.add_slide("S").add_plotly(html_file)   # pathlib.Path, not str
    assert isinstance(cell, PlotlyCell)


def test_add_plotly_from_html_renders(html_file):
    deck = _plotly_deck()
    deck.add_slide("S").add_plotly(html_file)
    html = deck.render()
    assert "Plotly.newPlot" in html or "plotly-graph-div" in html


def test_add_plotly_figure_still_works(fig):
    """The original Figure path must keep working unchanged."""
    deck = _plotly_deck()
    cell = deck.add_slide("S").add_plotly(fig)
    assert isinstance(cell, PlotlyCell)
    assert cell.fig is not None


def test_add_plotly_missing_file_raises():
    deck = _plotly_deck()
    with pytest.raises(FileNotFoundError):
        deck.add_slide("S").add_plotly("does_not_exist.html")


# ---------------------------------------------------------------------------
# Serialization round-trip of an HTML-loaded cell
# ---------------------------------------------------------------------------

def test_html_loaded_cell_round_trips_through_export(html_file):
    deck = _plotly_deck()
    deck.add_slide("S").add_plotly(html_file)
    clone = Deck.from_dict(deck.to_dict())
    assert clone.render() == deck.render()


# ---------------------------------------------------------------------------
# Fallback when plotly is not importable
# ---------------------------------------------------------------------------

def test_from_html_without_plotly(html_file, monkeypatch):
    # Block `import plotly...` so from_html takes the fig_json-only fallback.
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name.split(".")[0] == "plotly":
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    for mod in [m for m in sys.modules if m.split(".")[0] == "plotly"]:
        monkeypatch.delitem(sys.modules, mod, raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)

    from montin.cells.base import CellParams

    params = CellParams(col=1, row=1, cell_id="_cell-1")
    cell = PlotlyCell.from_html(html_file, params)
    assert cell.fig is None
    assert json.loads(cell.fig_json)["data"][0]["y"] == [7, 11, 13]
