"""Tests for plugin declaration and missing-plugin errors."""

import pytest

from tessera import HTMLSlides, Plugin
from tessera.exceptions import PluginNotDeclaredError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def deck_without_plugins():
    return HTMLSlides(title="Test", plugins=[])


def deck_with(*names):
    return HTMLSlides(title="Test", plugins=[Plugin(n, "cdn") for n in names])


# ---------------------------------------------------------------------------
# add_code — requires "highlight"
# ---------------------------------------------------------------------------

def test_add_code_without_highlight_raises():
    deck = deck_without_plugins()
    s = deck.add_slide("S", nrows=1, ncols=1)
    with pytest.raises(PluginNotDeclaredError, match="highlight"):
        s.add_code("print('hi')", language="python")


def test_add_code_with_highlight_succeeds():
    deck = deck_with("highlight")
    s = deck.add_slide("S", nrows=1, ncols=1)
    cell = s.add_code("x = 1", language="python")
    assert cell.language == "python"


# ---------------------------------------------------------------------------
# add_mermaid — requires "mermaid"
# ---------------------------------------------------------------------------

def test_add_mermaid_without_plugin_raises():
    deck = deck_without_plugins()
    s = deck.add_slide("S", nrows=1, ncols=1)
    with pytest.raises(PluginNotDeclaredError, match="mermaid"):
        s.add_mermaid("flowchart LR\n  A --> B")


def test_add_mermaid_with_plugin_succeeds():
    deck = deck_with("mermaid")
    s = deck.add_slide("S", nrows=1, ncols=1)
    cell = s.add_mermaid("flowchart LR\n  A --> B")
    assert "A --> B" in cell.diagram


# ---------------------------------------------------------------------------
# add_plotly — requires "plotly"
# ---------------------------------------------------------------------------

def test_add_plotly_without_plugin_raises():
    px = pytest.importorskip("plotly.express")
    deck = deck_without_plugins()
    s = deck.add_slide("S", nrows=1, ncols=1)
    fig = px.scatter(x=[1], y=[1])
    with pytest.raises(PluginNotDeclaredError, match="plotly"):
        s.add_plotly(fig)


def test_add_plotly_with_plugin_succeeds():
    px = pytest.importorskip("plotly.express")
    deck = deck_with("plotly")
    s = deck.add_slide("S", nrows=1, ncols=1)
    fig = px.scatter(x=[1, 2], y=[3, 4])
    cell = s.add_plotly(fig)
    assert cell is not None


# ---------------------------------------------------------------------------
# Other plugins don't interfere
# ---------------------------------------------------------------------------

def test_having_mermaid_does_not_satisfy_highlight():
    deck = deck_with("mermaid")
    s = deck.add_slide("S", nrows=1, ncols=1)
    with pytest.raises(PluginNotDeclaredError, match="highlight"):
        s.add_code("x = 1")


def test_error_message_mentions_method_name():
    deck = deck_without_plugins()
    s = deck.add_slide("S", nrows=1, ncols=1)
    with pytest.raises(PluginNotDeclaredError, match="add_code"):
        s.add_code("x = 1")
