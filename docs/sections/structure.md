# Deck structure

Beyond content slides, téssera provides three structural slide types for
organising long presentations: **title**, **section**, and **TOC**.

## Title slide

`add_title()` creates the cover slide shown at the start of a deck. It is
centred, displays a large heading, and automatically shows author, date, and
version metadata from the `HTMLSlides` constructor.

```python
slides = HTMLSlides(
    title="Annual Engineering Report",
    author="A. Dessimoni",
    date="2025-06-01",
    version="2.1",
    theme="default",
)

slides.add_title(
    "Annual Engineering Report",
    subtitle="Platform Performance · H1 2025",
)
```

The `subtitle` appears below the title in a smaller muted style. A decorative
accent bar is drawn under the title block on the default theme.

---

## Section slides

`add_section()` inserts a centred divider slide between groups of content
slides. By default it also shows an inline table of contents that highlights
the current section.

```python
slides.add_section("Data Ingestion")

# sub-section — indented in the sidebar
slides.add_section("Raw pipeline",   level=2)
slides.add_section("Validation",     level=2)

slides.add_section("Model Training")
slides.add_section("Feature store",  level=2)
```

### Section levels

The `level` parameter controls how the section is displayed in the sidebar:

| `level` | Sidebar appearance |
|---|---|
| `1` (default) | Bold, full opacity |
| `2` | Indented, muted colour |
| `3` | Further indented, dimmed |

### Excluding a section from the TOC

Pass `add_to_toc=False` to create a section divider that does not appear in
TOC slides or inline TOC lists — useful for appendices or internal breaks.

```python
slides.add_section("Appendix", add_to_toc=False)
```

### Inline TOC on section slides

By default (`show_toc=True`) each section slide shows a compact list of all
TOC-registered sections with the current one highlighted. Disable it for a
clean divider with only the title:

```python
slides.add_section("Data Ingestion", show_toc=False)
```

---

## TOC slide

`add_toc()` inserts a clickable table of contents. The entries are populated at
`write()` time, so the TOC always reflects every section in the deck regardless
of the order you called `add_toc()`.

```python
slides.add_title("Annual Engineering Report")
slides.add_toc()                              # placed early, but populated at write()

slides.add_section("Data Ingestion")
slides.add_slide("Ingestion pipeline", ...)

slides.add_section("Model Training")
slides.add_slide("Training results", ...)

slides.write("report")                        # TOC now lists both sections
```

### Custom title

```python
slides.add_toc("Contents")
```

### Disabling auto-population

Pass `auto=False` to render an empty TOC placeholder (useful as a manual
override or debugging aid):

```python
slides.add_toc(auto=False)
```

---

## Putting it together

```python
from tessera import HTMLSlides, Plugin

slides = HTMLSlides(
    title="Q3 Platform Report",
    author="A. Dessimoni",
    date="2025-06-01",
    version="3.0",
    plugins=[Plugin("plotly", "cdn"), Plugin("mermaid", "cdn")],
)

slides.add_title("Q3 Platform Report", subtitle="Platform Engineering")
slides.add_toc()

# — Section 1 ——————————————————————————————
slides.add_section("Infrastructure")
slides.add_section("Networking", level=2)

slide = slides.add_slide("Network overview", nrows=1, ncols=2)
slide.add_metric(value="12 ms", label="Avg latency")
slide.add_metric(value="99.98 %", label="Uptime")

slides.add_section("Storage", level=2)

slide = slides.add_slide("Storage capacity", nrows=1, ncols=2)
slide.add_metric(value="4.2 TB", label="Used")
slide.add_metric(value="12 TB",  label="Total")

# — Section 2 ——————————————————————————————
slides.add_section("Model Performance")

slide = slides.add_slide("Latency benchmarks", nrows=1, ncols=2)
# ... add cells ...

# — Appendix (no TOC entry) ————————————————
slides.add_section("Appendix", add_to_toc=False, show_toc=False)

slides.write("q3-report")
```

For a better view, click the &#x26F6; `Fullscreen (F)` button on the bottom toolbar.

```{raw} html
<div style="
  width: 65vw;
  position: relative;
  padding: 0 1rem;
  box-sizing: border-box;
">
  <iframe
    src="../_static/title-sections-example.html"
    style="
      display: block;
      width: 100%;
      height: 600px;
      border: 1px solid var(--color-background-border, #ccc);
      border-radius: 8px;
    "
    loading="lazy"
    allowfullscreen
  ></iframe>
</div>
```