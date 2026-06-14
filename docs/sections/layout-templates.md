# Layout templates

`SlideDefaults` and `CellDefaults` can be instantiated independently and passed
per-slide via `slide_defaults` and `cell_defaults`. This lets you define reusable
layout templates and apply them selectively, without changing the global defaults
set on `HTMLSlides`.

```python
from tessera import HTMLSlides, SlideDefaults, CellDefaults

slides = HTMLSlides(title="Template Report")

# Define reusable templates
slide_2x2     = SlideDefaults(ncols=2, nrows=2)
slide_2x1     = SlideDefaults(ncols=2, nrows=1)
centered_cell = CellDefaults(halign="center", valign="middle")

# Apply a layout template and a cell template together
s = slides.add_slide("Results", slide_defaults=slide_2x2, cell_defaults=centered_cell)
for i in range(s.nrows * s.ncols):
    s.add_text(f"Cell {i}")

# Apply only a layout template; cell defaults fall back to the global ones
s = slides.add_slide("Summary", slide_defaults=slide_2x1)
for i in range(s.nrows * s.ncols):
    s.add_text(f"Cell {i}")

slides.write("template_report", open_browser=True)
```

The priority order for each parameter is:

1. **Explicit argument** — value passed directly to `add_slide()` or `add_*()`.
2. **Per-call default** — `slide_defaults` / `cell_defaults` argument on `add_slide()`.
3. **Global default** — `slide_defaults` / `cell_defaults` set on `HTMLSlides`.

<!-- SCREENSHOT ─ layout-templates.png
Show the tessera presentation in a browser (two slides visible via the slide
navigator):
  • Slide 1 "Results": 2×2 grid, four text cells with "Cell 0" … "Cell 3",
    text centred both horizontally and vertically in each card.
  • Slide 2 "Summary": 2×1 grid, two text cells "Cell 0" and "Cell 1",
    left-aligned (global default).
Save as: docs/_static/img/slide-management/layout-templates.png
-->

```{figure} _static/img/slide-management/layout-templates.png
:alt: Two slides using different layout templates
:width: 90%

Two slides built from different `SlideDefaults` templates. Slide 1 uses a 2×2
grid with centred content; slide 2 uses a 2×1 grid with the global cell defaults.
```
