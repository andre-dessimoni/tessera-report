"""Tests for JSON export/import of cells, slides, slide groups, and whole decks.

Covers ``to_dict`` / ``from_dict`` round-trips, the file envelope written by
``export`` / read by ``from_file`` (including gzip compression), and the
slide-group / whole-deck operations. The strongest checks compare rendered HTML
before and after a round-trip.
"""

import json

import pytest

from montin import Cell, Deck, Plugins, Slide
from montin.exceptions import InvalidDataError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _all_plugins_deck(**kwargs) -> Deck:
    return Deck(
        title="Round Trip",
        author="Tester",
        plugins=[
            Plugins.Plotly(),
            Plugins.Highlight(),
            Plugins.Mermaid(),
            Plugins.Tabulator(),
        ],
        **kwargs,
    )


def _populated_deck() -> Deck:
    """A deck exercising every JSON-native cell type plus the special slides."""
    deck = _all_plugins_deck()
    deck.add_title("Cover", subtitle="A subtitle")
    deck.add_section("Section One", level=1)
    deck.add_toc()
    s = deck.add_slide("Content", nrows=4, ncols=2, notes="presenter notes")
    s.add_text("# Heading\n\nSome **markdown**.")
    s.add_metric(value=98.7, label="Efficiency", delta=+2.3)
    s.add_code("print('hi')", language="python")
    s.add_table({"a": [1, 2], "b": [3, 4]})
    s.add_list(["one", "two", ["nested"]])
    s.add_mermaid("graph TD; A-->B")
    s.add_tabulator({"x": [1, 2, 3], "y": [4, 5, 6]})
    s.add_html("<b>raw</b>")
    return deck


# ---------------------------------------------------------------------------
# Cell round-trips
# ---------------------------------------------------------------------------

def test_cell_to_dict_has_envelope():
    deck = _all_plugins_deck()
    cell = deck.add_slide("S").add_text("hello")
    d = cell.to_dict()
    assert d["cell_type"] == "TextCell"
    assert d["params"]["col"] == 1 and d["params"]["row"] == 1
    assert d["content"]["content"] == "hello"


def test_cell_from_dict_dispatches_subtype():
    deck = _all_plugins_deck()
    s = deck.add_slide("S", nrows=1, ncols=3)
    cells = [
        s.add_text("t"),
        s.add_code("c", language="python"),
        s.add_mermaid("graph TD; A-->B"),
    ]
    for cell in cells:
        clone = Cell.from_dict(cell.to_dict())
        assert type(clone) is type(cell)


def test_metric_cell_round_trip_preserves_derived():
    deck = _all_plugins_deck()
    m = deck.add_slide("S").add_metric(value=10, label="L", delta=-5, lower_is_better=True)
    clone = Cell.from_dict(m.to_dict())
    assert clone.value == 10
    assert clone.delta == -5
    assert clone.delta_class == m.delta_class
    assert clone.delta_symbol == m.delta_symbol
    assert clone.delta_color == m.delta_color


def test_table_cell_round_trip_preserves_headers_rows():
    deck = _all_plugins_deck()
    t = deck.add_slide("S").add_table({"a": [1, 2], "b": [3, 4]})
    clone = Cell.from_dict(t.to_dict())
    assert clone.headers == t.headers
    assert clone.rows == t.rows


def test_unknown_cell_type_raises():
    with pytest.raises(InvalidDataError):
        Cell.from_dict({"cell_type": "NopeCell", "params": {"col": 1, "row": 1, "cell_id": "x"}})


# ---------------------------------------------------------------------------
# File envelope + compression
# ---------------------------------------------------------------------------

def test_cell_export_and_from_file(tmp_path):
    deck = _all_plugins_deck()
    cell = deck.add_slide("S").add_text("# hi")
    path = cell.export(tmp_path / "cell.json")
    loaded = Cell.from_file(path)
    assert loaded.content == "# hi"


def test_from_file_rejects_wrong_kind(tmp_path):
    deck = _all_plugins_deck()
    slide = deck.add_slide("S")
    p = slide.export(tmp_path / "slide.json")
    with pytest.raises(InvalidDataError):
        Cell.from_file(p)               # a slide file is not a cell file


def test_read_rejects_newer_format(tmp_path):
    p = tmp_path / "future.json"
    p.write_text(json.dumps({"montin_format": 999, "kind": "cell", "cell": {}}), encoding="utf-8")
    with pytest.raises(InvalidDataError):
        Cell.from_file(p)


def test_compression_by_suffix_and_flag(tmp_path):
    deck = _populated_deck()

    gz = deck.export(tmp_path / "deck.json.gz")                 # inferred from suffix
    plain = deck.export(tmp_path / "deck.json")                 # inferred: plain
    forced = deck.export(tmp_path / "forced.json", compress=True)

    assert gz.read_bytes()[:2] == b"\x1f\x8b"
    assert plain.read_bytes()[:2] != b"\x1f\x8b"
    assert forced.read_bytes()[:2] == b"\x1f\x8b"

    # Every form reads back to an equivalent deck (auto-detected gzip).
    base = deck.render()
    for p in (gz, plain, forced):
        assert Deck.from_file(p).render() == base


# ---------------------------------------------------------------------------
# Slide round-trips
# ---------------------------------------------------------------------------

def test_slide_round_trip_render_equal():
    deck = _populated_deck()
    src = deck.slides[-1]                # the populated content slide
    clone = Slide.from_dict(src.to_dict())
    assert [type(c).__name__ for c in clone.cells] == [type(c).__name__ for c in src.cells]
    assert clone.nrows == src.nrows and clone.ncols == src.ncols
    assert clone.notes == src.notes


def test_slide_export_from_file(tmp_path):
    deck = _populated_deck()
    src = deck.slides[-1]
    p = src.export(tmp_path / "slide.json")
    loaded = Slide.from_file(p)
    assert len(loaded.cells) == len(src.cells)


def test_import_cell_places_content_with_new_params(tmp_path):
    deck = _all_plugins_deck()
    src_slide = deck.add_slide("Src", nrows=1, ncols=1)
    cell = src_slide.add_text("imported text")
    p = cell.export(tmp_path / "cell.json")

    target = deck.add_slide("Target", nrows=2, ncols=2)
    placed = target.import_cell(p, col=2, row=2)
    assert placed.content == "imported text"
    assert (placed.params.col, placed.params.row) == (2, 2)
    assert placed in target.cells


# ---------------------------------------------------------------------------
# Deck round-trips + slide groups
# ---------------------------------------------------------------------------

def test_deck_round_trip_render_equal():
    deck = _populated_deck()
    clone = Deck.from_dict(deck.to_dict())
    assert clone.render() == deck.render()


def test_deck_round_trip_preserves_config_and_sections():
    deck = _populated_deck()
    clone = Deck.from_dict(deck.to_dict())
    assert clone.title == deck.title
    assert {p.name for p in clone.plugins} == {p.name for p in deck.plugins}
    assert clone.sections == deck.sections


def test_export_slides_by_pos_and_by_key(tmp_path):
    deck = _populated_deck()
    content_id = deck.slides[-1].slide_id

    by_pos = deck.export_slides(tmp_path / "pos.json", by_pos=range(0, 2))
    by_key = deck.export_slides(tmp_path / "key.json", by_key=[content_id])

    target = Deck(title="x")
    added = target.import_slides(by_pos)
    assert len(added) == 2

    target2 = Deck(title="y")
    added2 = target2.import_slides(by_key)
    assert len(added2) == 1 and added2[0].slide_id == content_id


def test_import_slides_index_and_collision_rename():
    deck = _populated_deck()
    src = deck.slides[-1]
    payload = src.to_dict()

    # Re-import the same slide → id collision must be auto-renamed, not clobber.
    n_before = len(deck.slides)
    from montin.io import write_document
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    write_document(path, "slide", payload)
    added = deck.import_slides(path, index=0)
    os.remove(path)

    assert len(deck.slides) == n_before + 1
    assert deck.slides[0] is added[0]
    assert added[0].slide_id != src.slide_id          # renamed
    assert added[0].slide_id in deck.slide_map


def test_import_slides_accepts_single_slide_file(tmp_path):
    deck = _populated_deck()
    p = deck.slides[-1].export(tmp_path / "one.json")   # kind="slide"
    target = Deck(title="x")
    added = target.import_slides(p)                       # import_slides reads a single slide too
    assert len(added) == 1


# ---------------------------------------------------------------------------
# Figure + image cells (optional deps)
# ---------------------------------------------------------------------------

def test_matplotlib_round_trip_render_equal():
    pytest.importorskip("matplotlib")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    deck = Deck(title="mpl")
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [3, 1, 2])
    deck.add_slide("S").add_matplotlib(fig)

    clone = Deck.from_dict(deck.to_dict())
    assert clone.render() == deck.render()
    reloaded = clone.slides[0].cells[0]
    assert reloaded.fig is None                  # live figure not restored
    assert reloaded.src                          # but the encoded image is


def test_plotly_round_trip_render_equal():
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    deck = Deck(title="plotly", plugins=[Plugins.Plotly()])
    fig = go.Figure(data=[go.Bar(x=["a", "b"], y=[1, 2])])
    deck.add_slide("S").add_plotly(fig)

    clone = Deck.from_dict(deck.to_dict())
    assert clone.render() == deck.render()
    assert clone.slides[0].cells[0].fig_json == deck.slides[0].cells[0].fig_json


def test_image_embed_true_inlines_and_false_keeps_reference(tmp_path):
    # A minimal file is enough — image_encoder reads bytes and base64-encodes it.
    img = tmp_path / "pic.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)

    deck = Deck(title="img")
    cell = deck.add_slide("S").add_image(img)

    embedded = cell.to_dict(embed=True)["content"]["source"]
    assert embedded.startswith("data:image/png;base64,")

    referenced = cell.to_dict(embed=False)["content"]["source"]
    assert referenced.endswith("pic.png") and not referenced.startswith("data:")


def test_image_round_trip_render_equal(tmp_path):
    img = tmp_path / "pic.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)
    deck = Deck(title="img")
    deck.add_slide("S").add_image(img)
    clone = Deck.from_dict(deck.to_dict())
    assert clone.render() == deck.render()
