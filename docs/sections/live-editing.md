# Live editing

## Autosave

Pass `autosave` with a filename to have tessera write the HTML file automatically
after each change, so you can live-preview in a browser while building the deck.


```python
presentation = HTMLSlides(
    title="Live Report",
    autosave="report",        # writes report.html after each trigger
    autosave_level="cell",    # trigger: "slide" (default) or "cell"
)
```

`autosave_level` controls how frequently the file is written:

| Level | Trigger | Recommended when |
|---|---|---|
| `"slide"` | After each `add_slide()` | Large presentations with many cells |
| `"cell"` | After each `add_*()` cell call | Small decks or iterative Jupyter workflows |

:::{note}
For large presentations prefer `autosave_level="slide"` to avoid redundant
writes on every cell addition, or keep autosave disabled, manually saving with `.write()` when needed.
:::

## VSCode workflow

A convenient way to use autosave is alongside the
[Live Preview](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server)
extension in VSCode. Open the generated `.html` file with **Live Preview** (right-click
the file → *Show Preview*) and it will automatically refresh whenever tessera
rewrites it. This gives you an instant side-by-side view — code on the left,
slides on the right — without leaving the editor, as shown below:

![VSCode-workflow](../_static/img/live-editing/animation.webp)
