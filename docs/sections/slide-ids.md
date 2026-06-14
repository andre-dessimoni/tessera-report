# Slide IDs

Every slide has an identifier (`slide_id`). When `slide_id` is omitted, tessera
assigns an automatic one of the form `_slide-<n>` (the leading underscore
distinguishes it from user-supplied IDs). You can supply any hashable value —
integer, string, tuple, etc.

```python
# Auto-generated ID ("_slide-1")
slide = presentation.add_slide("Introduction")
slide.add_text("Automatically managed ID.")

# Explicit integer ID
slide = presentation.add_slide("Results", slide_id=1)
slide.add_text("example 2")

# Explicit string ID
slide = presentation.add_slide("Details", ncols=2, slide_id="details")
slide.add_text("example 3.1")
```

## Overwriting slides

If a slide with the given `slide_id` already exists, it is **replaced in-place**
(same position in the deck). This is particularly useful in Jupyter notebooks:
re-running a cell recreates only that slide without duplicating it.

```python
# Re-running this cell overwrites the slide at id=1, preserving deck order
slide = presentation.add_slide("Results", slide_id=1)
slide.add_text("Updated content.")
```

## Retrieving and editing slides

Use `get_slide()` to fetch a slide by ID and continue adding cells to it from a
different notebook cell.

```python
slide = presentation.get_slide("details")
slide.add_text("example 3.2")
```

Cell IDs work the same way within a slide: if a cell with `cell_id` already
exists, it is replaced.

```python
slide.add_text("first version",  cell_id=1)
slide.add_text("second version", cell_id=1)   # overwrites the first
```

## Removing slides

```python
presentation.remove_slide("_slide-1")   # auto-generated ID
presentation.remove_slide(1)            # explicit integer ID
```

<!-- SCREENSHOT ─ slide-id-overwrite.png
Run the full example below in a Jupyter notebook, then take a screenshot of the
resulting browser tab showing the final presentation.

  from tessera import HTMLSlides
  presentation = HTMLSlides(title="IDs example")
  presentation.add_slide("Introduction", slide_id="_intro")
  presentation.add_slide("Results", slide_id=1).add_text("Original content")
  presentation.add_slide("Details", ncols=2, slide_id="details").add_text("3.1")
  # Overwrite id=1:
  presentation.add_slide("Results", slide_id=1).add_text("Overwritten content")
  # Continue editing 'details':
  presentation.get_slide("details").add_text("3.2", cell_id=1)
  presentation.get_slide("details").add_text("3.2 (overwritten)", cell_id=1)
  presentation.remove_slide("_intro")
  presentation.write("ids_example", open_browser=True)

The final deck has 2 slides:
  • Slide "Results" (id=1): shows "Overwritten content"
  • Slide "Details" (id="details"): shows "3.2 (overwritten)" in a 2-col grid
Capture the browser window showing both slides (use the slide navigator to show
both thumbnails if possible, or two side-by-side screenshots).
Save as: docs/_static/img/slide-management/slide-id-overwrite.png
-->

```{figure} _static/img/slide-management/slide-id-overwrite.png
:alt: Final presentation after slide overwriting and removal
:width: 90%

Final deck after re-running a slide definition (`slide_id=1`) and removing the
auto-ID slide. The "Results" slide shows overwritten content; the "Details" slide
shows the overwritten cell.
```

![VSCode-workflow](../_static/img/live-editing/animation.webp)
