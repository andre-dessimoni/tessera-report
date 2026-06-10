# Cell types

## TextCell — `add_text()`

Text with Markdown and LaTeX support (via MathJax).

```python
slide.add_text(
    "### Title\n\nText with **bold**, *italic*, and LaTeX: $E = mc^2$",
    markdown=True,   # default — False delivers raw HTML
    caption="Source: internal report",
)
```

---

## MetricCell — `add_metric()`

KPI card with a large value, a label, and an optional delta.

```python
slide.add_metric(
    value=98.7,
    label="Efficiency (%)",
    delta=+2.3,             # positive → green, negative → red
    delta_label="vs previous month",
)
```

---

## TableCell — `add_table()`

Accepts CSV, dict, `list[list]`, or `pd.DataFrame`.

```python
# CSV (separator auto-detected)
slide.add_table("""Component,Jan,Feb,Mar
Motor A,98.1,97.8,98.7
Motor B,94.3,95.1,96.2""")

# dict
slide.add_table({"Name": ["Motor A", "Motor B"], "Status": ["OK", "OK"]})

# DataFrame
import pandas as pd
slide.add_table(pd.read_csv("data.csv"))
```

---

## ImageCell — `add_image()`

Image with lightbox (zoom/pan). Accepts a local path, URL, or base64 string.

```python
slide.add_image(
    "results/chart.png",
    lightbox=True,           # default
    caption="Fig. 1 — Failure distribution",
)
```

In `self_contained=True` mode, local images are embedded as base64.

---

## ImageSliderCell — `add_image_slider()`

Image carousel with prev/next buttons and lightbox.

```python
slide.add_image_slider(
    ["img1.png", "img2.png", "img3.png"],
    captions=["Front view", "Side view", "Detail"],
    caption="Visual inspection — 3 samples",
)
```

---

## ListCell — `add_list()`

Bullet or numbered list, with support for nested sub-levels.

```python
slide.add_list(
    ["Analysis", "Design", "Implementation", "Testing"],
    ordered=True,
    caption="Project phases",
)

# With sub-levels
slide.add_list([
    "Analysis",
    {"Design": ["UX", "Backend", "Database"]},
    "Implementation",
])
```

---

## CodeCell — `add_code()`

Code block with syntax highlighting via Highlight.js.
Requires `Plugin("highlight", "cdn")`.

```python
slide.add_code(
    "def hello():\n    return 'world'",
    language="python",     # python, sql, javascript, bash, ...
    copy_button=True,
)
```

---

## PlotlyCell — `add_plotly()`

Interactive Plotly figure embedded as JSON.
Requires `Plugin("plotly", "cdn")`.

```python
import plotly.express as px

fig = px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", color="species")
slide.add_plotly(fig, caption="Iris Dataset")
```

---

## MermaidCell — `add_mermaid()`

Declarative diagram (flowchart, sequenceDiagram, gantt, etc.).
Requires `Plugin("mermaid", "cdn")`.

```python
slide.add_mermaid("""
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No|  D[Process B]
    C & D --> E[End]
""")
```

---

## HtmlCell — `add_html()`

Raw HTML injected without escaping — full styling freedom.

```python
slide.add_html("""
<div style="padding:1rem; background:#f0f4ff; border-radius:8px">
    <h3>Custom content</h3>
    <p>Any valid <strong>HTML</strong>.</p>
</div>
""")
```

---

## IframeCell — `add_iframe()`

Embed external content via `<iframe>`. Requires an internet connection.

```python
slide.add_iframe(
    "https://www.openstreetmap.org/export/embed.html?bbox=...",
    caption="Location map",
)
```

---

## EmptyCell — `add_empty()`

Reserves grid space without rendering any content. Useful for asymmetric layouts.

```python
slide = slides.add_slide("Example", nrows=2, ncols=2)
slide.add_metric(value=42, label="KPI", rowspan=2)  # col 1, rows 1 and 2
slide.add_text("Text")                               # col 2, row 1
slide.add_empty()                                    # col 2, row 2 — empty space
```
