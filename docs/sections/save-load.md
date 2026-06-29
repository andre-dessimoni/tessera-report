# Saving & Loading

Montin can serialise a report's **structure and data** to JSON and load it back
into Python. You can save and reload at four granularities:

| Granularity | Save | Load |
|-------------|------|------|
| One cell    | `cell.export("cell.json")` | `slide.import_cell("cell.json")` / `Cell.from_file(...)` |
| One slide   | `slide.export("slide.json")` | `deck.import_slides("slide.json")` / `Slide.from_file(...)` |
| Some slides | `deck.export_slides("slides.json", by_pos=...)` | `deck.import_slides("slides.json")` |
| Whole deck  | `deck.export("deck.json")` | `Deck.from_file("deck.json")` |

A reloaded object renders **identically** to the original — loading does not run
your build code again, so a saved report opens even on a machine that lacks the
libraries that produced it (e.g. matplotlib or Plotly need not be installed to
reload a deck that contains their charts).

## Reusing a cell

Export a cell from one report and drop it into another. The cell's *content*
comes from the file; its *placement* (and styling) are decided at import time,
exactly like an `add_*` call:

```python
# Report A
cell = slide_a.add_plotly(fig)
cell.export("revenue_chart.json")

# Report B
slide = deck_b.add_slide("Overview", ncols=2)
slide.import_cell("revenue_chart.json", col=1, colspan=2)
```

Any span / style / caption argument you omit falls back to the value the cell was
exported with. A fresh `cell_id` is assigned unless you pass one (pass an
existing id to overwrite a cell in place).

## Reusing slides

```python
# Save one slide…
slide.export("methods.json")

# …and insert it into another deck. index says where it lands in the deck
# (-1, the default, appends); colliding slide ids are auto-renamed.
deck.import_slides("methods.json", index=1)
```

Save an arbitrary **group** of slides by position or by id, then import them as a
block (a single-slide file and a multi-slide file are both accepted by
`import_slides`):

```python
deck.export_slides("intro.json", by_pos=range(0, 3))     # first three slides
deck.export_slides("kpis.json",  by_key=["kpi", "trend"]) # by slide_id
deck.import_slides("intro.json")
```

## Saving a whole deck

```python
deck.export("report.json")
again = Deck.from_file("report.json")
again.write("report")          # renders identical HTML
```

The deck file stores every `Deck(...)` setting (theme, plugins, defaults,
security, sidebar/toolbar options, …) plus all slides and the table of contents.

## `to_dict` / `from_dict`

`export` / `from_file` are thin wrappers over the dict (de)serialisers, which you
can use directly to inspect or transform a report in memory:

```python
from montin import Cell, Slide, Deck

d = cell.to_dict()
cell2 = Cell.from_dict(d)
slide2 = Slide.from_dict(slide.to_dict())
deck2  = Deck.from_dict(deck.to_dict())
```

## Embedding media (`embed=`)

Every `export` / `to_dict` accepts `embed` (default `True`):

- `embed=True` — **self-contained**: images are inlined as base64 so the JSON
  carries everything. Most portable; larger files.
- `embed=False` — **references**: image file paths / URLs are kept as text.
  Smaller files, but the import breaks if those files move or are absent.

Matplotlib and Plotly figures are always embedded (there is no external file to
point at). A matplotlib figure is stored as its **rendered image**, so it comes
back as a static picture rather than an editable `Figure`; a Plotly figure
round-trips fully via its JSON.

## Compression (`compress=`)

Every `export` accepts `compress`:

- `None` (default) — infer from the path: a `.gz` suffix compresses, otherwise
  plain JSON.
- `True` / `False` — force gzip on / off.

Compression uses the standard-library `gzip` module (no extra dependency).
Readers auto-detect gzip, so a file loads whether or not its extension advertises
it:

```python
deck.export("report.json.gz")          # gzip (inferred from suffix)
deck.export("report.json", compress=True)   # gzip (forced)
Deck.from_file("report.json.gz")        # decompressed transparently
```
