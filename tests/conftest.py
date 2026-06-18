import pytest

from tessera import CellDefaults, Deck, Plugin, SlideDefaults


@pytest.fixture
def deck():
    """Deck instance with all plugins declared."""
    return Deck(
        title="Test Deck",
        author="Tester",
        plugins=[
            Plugin("plotly", "cdn"),
            Plugin("highlight", "cdn"),
            Plugin("mermaid", "cdn"),
        ],
    )


@pytest.fixture
def slide_2x2(deck):
    return deck.add_slide("Test Slide", nrows=2, ncols=2)


@pytest.fixture
def slide_1x3(deck):
    return deck.add_slide("Wide Slide", nrows=1, ncols=3)
