# TODO: replage px by a simpler plotly example to avoid adding plotly as a dependency for this demo
# Add figures generated with matplotlib to the docs/_static directory and use them in ImageCells instead
import plotly.express as px

from tessera import CellDefaults, HTMLSlides, Plugin, SlideDefaults

# -- Configuration -------------------------------------------------------------
slides = HTMLSlides(
    title="Cell Catalog",
    author="J. Smith",
    date="2024-09-30",
    version="1.0",
    self_contained=True,
    slide_defaults=SlideDefaults(nrows=2, ncols=2),
    cell_defaults=CellDefaults(
        expand_button=True, transparent=False),
    plugins=[
        Plugin("plotly",    "cdn"),
        Plugin("highlight", "cdn"),
        Plugin("mermaid",   "cdn"),
    ],
    theme="dark", # light dark light-blue academic sobrio
)


# -- Cover ---------------------------------------------------------------------
slides.add_title(
    "Cell Catalog",
    subtitle="One example of each type available in tessera",
)

# -- Section 1: MetricCell + TextCell ------------------------------------------
slides.add_section("1 — Metrics and Text", level=1)

slide1 = slides.add_slide(
    "MetricCell and TextCell",
    nrows=2,
    ncols=3,
    row_heights=["35%", "65%"],
    notes="add_metric: KPI card with value, label and delta. add_text: markdown with LaTeX.",
)

# MetricCell — KPI cards in row 1
slide1.add_metric(transparent=False, value=98.7, label="Efficiency (%)", delta=+2.3, delta_label="vs previous month")
slide1.add_metric(transparent=False, value=142,  label="Defects",         delta=-18,  delta_label="vs previous month")
slide1.add_metric(transparent=False, value="4.8", label="NPS")

# TextCell — markdown content in row 2
slide1.add_text(
    "### Summary\n\nQuarterly indicators show consistent improvement "
    "in operational efficiency.",
    colspan=2, 
)
slide1.add_text(
    "**Next steps:**\n- Review QA process\n"
    "- Update documentation\n- Schedule retrospective",
)

# -- Section 2: TableCell + ImageCell ------------------------------------------
slides.add_section("2 — Table and Image", level=1)

slide2 = slides.add_slide(
    "TableCell and ImageCell",
    nrows=1,
    ncols=2,
    col_widths=["55%", "45%"],
)

# TableCell — accepts CSV, dict, list, or DataFrame
slide2.add_table(
    """Component,Jan,Feb,Mar,Trend
Motor A,98.1,97.8,98.7,↑
Motor B,94.3,95.1,96.2,↑
Pump C,88.7,87.2,85.0,↓
Valve D,99.9,99.9,99.8,→""",
    caption="Tab. 1 — Efficiency by component (%)",
)

# ImageCell — lightbox with zoom/pan
slide2.add_image(
    "https://th.bing.com/th/id/R.1605a2f78b69d25167b860fecd52d8c3?rik=PN2LlyaaDMgd4A&pid=ImgRaw&r=0",
    caption="Fig. 1 — Schematic diagram",
    lightbox=True,
)

# -- Section 3: ListCell + CodeCell --------------------------------------------
slides.add_section("3 — List and Code", level=1)

slide3 = slides.add_slide(
    "ListCell and CodeCell",
    nrows=1,
    ncols=2,
)

# ListCell — bullet list (ordered=False) or numbered (ordered=True)
slide3.add_list(
    [
        "Requirements analysis",
        "Solution design",
        "Implementation",
        "Integration testing",
        "Production deploy",
    ],
    ordered=True,
    caption="Project phases",
)

# CodeCell — syntax highlighting via Plugin('highlight')
slide3.add_code(
    'def fibonacci(n: int):\n'
    '    a, b = 0, 1\n'
    '    for _ in range(n):\n'
    '        yield a\n'
    '        a, b = b, a + b\n\n'
    'print(list(fibonacci(10)))',
    language="python",
    caption="Example — CodeCell with highlighting",
    copy_button=True,
    expand_button=False,
)

# -- Section 4: MermaidCell + HtmlCell -----------------------------------------
slides.add_section("4 — Mermaid and HTML", level=1)

slide4 = slides.add_slide(
    "MermaidCell and HtmlCell",
    nrows=2,
    ncols=1,
)

# MermaidCell — declarative diagram via Plugin('mermaid')
slide4.add_mermaid(
    """flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E""",
    caption="Decision flow — MermaidCell",
)

# HtmlCell — raw HTML without escaping
slide4.add_html(
    "<div style='padding:1.2rem;background:#f0f4ff;border-radius:8px;"
    "height:100%;box-sizing:border-box;display:flex;flex-direction:column;gap:.6rem'>"
    "<h3 style='margin:0;color:#3b5bdb'>HtmlCell</h3>"
    "<p style='margin:0'>Accepts <strong>any HTML</strong> without escaping.</p>"
    "<ul style='margin:0;padding-left:1.4rem'>"
    "<li>Flexible</li><li>Inline styles</li><li>Custom components</li>"
    "</ul>"
    "</div>",
    caption="Raw HTML — HtmlCell",
)

# -- Section 5: IframeCell + EmptyCell -----------------------------------------
slides.add_section("5 — Iframe and Empty", level=1)

slide5 = slides.add_slide(
    "IframeCell and EmptyCell",
    nrows=1,
    ncols=2,
    notes="IframeCell requires an internet connection. EmptyCell only reserves grid space.",
)

# IframeCell — embed external content
slide5.add_iframe(
    "https://www.openstreetmap.org/export/embed.html"
    "?bbox=-43.2,-22.95,-43.1,-22.85&layer=mapnik",
    caption="Map — IframeCell (requires internet)",
)

# EmptyCell — reserves grid space without rendering content
# slide5.add_empty()

# -- Section 6: PlotlyCell -----------------------------------------------------
slides.add_section("6 — Plotly", level=1)

slide6 = slides.add_slide(
    "PlotlyCell",
    nrows=1,
    ncols=2,
    col_widths=["70%", "30%"],
)
fig = px.scatter(
    px.data.iris(),
    x="sepal_width",
    y="sepal_length",
    color="species",
    title="Iris Dataset — PlotlyCell",
)
slide6.add_plotly(fig, caption="Interactive Plotly chart", expand_button=False)
slide6.add_text(
    "# Conclusions:\n\n"
    "This is a PlotlyCell rendering an interactive scatter plot of the Iris dataset. "
    "You can zoom, pan, and hover over points to see details.\n\n"
    "markdown list:\n"
    "- item 1\n"
    "- item 2\n"
    "  - subitem 2.1\n"
    "- item 3\n",
)
# -- Section 7: ImageSliderCell ------------------------------------------------
slides.add_section("7 — Image Slider", level=1)

slide7 = slides.add_slide(
    "ImageSliderCell",
    nrows=1,
    ncols=1,
)

slide7.add_image_slider(
    [
        "https://th.bing.com/th/id/R.1605a2f78b69d25167b860fecd52d8c3?rik=PN2LlyaaDMgd4A&pid=ImgRaw&r=0",
        "https://tse2.mm.bing.net/th/id/OIP.O5IF7N9qPSsKwQr9LCJELgHaDs?rs=1&pid=ImgDetMain&o=7&rm=3",
        "https://tse3.mm.bing.net/th/id/OIP.qQtDWBb5hCGy8xeDLRlt4gHaEG?rs=1&pid=ImgDetMain&o=7&rm=3",
    ],
    captions=["Image 1", "Image 2", "Image 3"],
    caption="Carousel with lightbox — ImageSliderCell",
)

# -- Section 7: ImageSliderCell ------------------------------------------------
slides.add_section("7 — Image Slider", level=1)

slide7 = slides.add_slide(
    "grid",
    nrows=2,
    ncols=4,
)

slide7.add_image(
    "https://th.bing.com/th/id/R.1605a2f78b69d25167b860fecd52d8c3?rik=PN2LlyaaDMgd4A&pid=ImgRaw&r=0",
    caption="Image 1",
)
slide7.add_image(
    "https://tse2.mm.bing.net/th/id/OIP.O5IF7N9qPSsKwQr9LCJELgHaDs?rs=1&pid=ImgDetMain&o=7&rm=3",
    caption="Image 2",
)
slide7.add_image(
    "https://tse3.mm.bing.net/th/id/OIP.qQtDWBb5hCGy8xeDLRlt4gHaEG?rs=1&pid=ImgDetMain&o=7&rm=3",
    caption="Image 3",
)
slide7.add_image(
    "https://th.bing.com/th/id/R.1605a2f78b69d25167b860fecd52d8c3?rik=PN2LlyaaDMgd4A&pid=ImgRaw&r=0",
    caption="Image 1",
)
slide7.add_image(
    "https://tse2.mm.bing.net/th/id/OIP.O5IF7N9qPSsKwQr9LCJELgHaDs?rs=1&pid=ImgDetMain&o=7&rm=3",
    caption="Image 2",
)
slide7.add_image(
    "https://tse3.mm.bing.net/th/id/OIP.qQtDWBb5hCGy8xeDLRlt4gHaEG?rs=1&pid=ImgDetMain&o=7&rm=3",
    caption="Image 3",
)
slide7.add_text(
    "# explanation\n\n"
    "This *slide* demonstrates a 2x4 grid layout filled with ImageCells. and  \n"
    "a _markdown_ written cell \n\n"
    "- mardown lista\n"
    "- with multiple items\n"
    "- and subitems\n",
    colspan=2,
    transparent=False
)
# -- Generate ------------------------------------------------------------------
output = slides.write("_static/demo", open_browser=False)
print(f"Generated: {output.resolve()}")
