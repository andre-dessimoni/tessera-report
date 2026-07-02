# Themes

Every deck is rendered with a **theme** — a small set of CSS that controls
colours, fonts, and corner radius across the whole report: sidebar, toolbar,
cells, tables, code blocks, metrics, and cover slides. The default theme matches
this documentation site (a clean light look); switch to another built-in with
one argument, or override any detail with your own CSS.

```python
from montin import Deck

deck = Deck(title="Report", theme="montin")   # the Montin brand look
```

---

## Built-in themes

| `theme=` | Look |
|---|---|
| `"default"` | **The default** — matches this documentation site (light): white content, grey sidebar, blue links, Inter/Sora. Identical to `"docs"`. |
| `"docs-dark"` | The documentation site in dark mode — `#131416` surface, blue links. |
| `"montin"` | **Brand light** — Sand background, Ink text, orange Accent (was the default). |
| `"ink"` | **Brand dark** — Ink background, Sand text, orange Accent. |
| `"midnight"` | The original Montin look — deep navy with a vivid pink-red accent. |
| `"light"` | Neutral professional light, blue accent. |
| `"dark"` | Charcoal, VS Code-inspired. |
| `"light-blue"` | Soft blue-tinted light. |
| `"academic"` | Serif, paper-like, restrained. |
| `"sobrio"` | Minimalist, borderless, generous whitespace. |

The default (and its explicit `"docs"` alias) plus `"docs-dark"` mirror this
documentation site (built with [Furo](https://github.com/pradyunsg/furo),
MIT-licensed) — handy when you want a report to sit visually alongside your docs.
`"montin"` and `"ink"` are the two halves of the Montin brand palette — the same
five colours on a light or dark background. `"midnight"` preserves the look that
shipped as the default before the brand palette.

---

## Theme gallery

The same sample report rendered under each built-in theme. Toggle the sidebar
(the &#9776; button or `B`) or go fullscreen (&#x26F6; / `F`) to explore.

**`default`** — the documentation-site light look (also available as `"docs"`).

```{raw} html
<iframe class="montin-embed" src="../_static/deck/theme_default.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

**`docs-dark`** — the documentation site in dark mode.

```{raw} html
<iframe class="montin-embed" src="../_static/deck/theme_docs-dark.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

**`montin`** — brand Sand (light).

```{raw} html
<iframe class="montin-embed" src="../_static/deck/theme_montin.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

**`ink`** — brand Ink (dark).

```{raw} html
<iframe class="montin-embed" src="../_static/deck/theme_ink.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

**`midnight`** — the original navy + pink-red look.

```{raw} html
<iframe class="montin-embed" src="../_static/deck/theme_midnight.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

**`light`** · **`dark`** · **`light-blue`** · **`academic`** · **`sobrio`** —
the neutral / classic set.

```{raw} html
<iframe class="montin-embed" src="../_static/deck/theme_light.html#demo"
        loading="lazy" allowfullscreen></iframe>
<iframe class="montin-embed" src="../_static/deck/theme_dark.html#demo"
        loading="lazy" allowfullscreen></iframe>
<iframe class="montin-embed" src="../_static/deck/theme_light-blue.html#demo"
        loading="lazy" allowfullscreen></iframe>
<iframe class="montin-embed" src="../_static/deck/theme_academic.html#demo"
        loading="lazy" allowfullscreen></iframe>
<iframe class="montin-embed" src="../_static/deck/theme_sobrio.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

---

## The brand palette

The brand themes are built from five colours. They are worth knowing if you
plan to extend the palette in `custom_css`.

| Name | Hex | Role |
|---|---|---|
| Ink | `#0F1F2E` | Primary text (light theme) / background (dark theme) |
| Slate | `#35546B` | Secondary colour, borders, UI elements |
| Stone | `#9AA6B2` | Neutral, muted text |
| Sand | `#E9ECEF` | Light background, borders |
| Accent | `#E07A3F` | Highlights — links, active state, deltas, CTAs |

---

## How theming works

The stylesheet for a deck is assembled in **four layers**, each able to
override the one before it:

1. **Base** — the `default` theme ships the complete set of component
   stylesheets (layout, slide, table, tabulator, list, toc, code, metric,
   image, toolbar). It is *always* loaded first, so every theme inherits a
   working layout and only has to change what it wants to look different.
2. **Theme** — the theme you select (`ink`, `dark`, …) layers on top,
   typically just re-declaring the colour variables in its `layout.css`.
3. **`theme_options`** — structured customization (next section), emitted as CSS
   and rendered elements on top of the theme.
4. **`custom_css`** — your own CSS, merged **last**, so it always wins.

Because the base supplies all the structure, a theme can be as small as a
single `:root` block that redefines a handful of variables.

---

## Customizing with `ThemeOptions`

Pick the closest theme, then fine-tune it with **structured options** instead of
hand-writing CSS. `ThemeOptions` groups the common branding knobs into small
nested dataclasses; it sits between the theme and `custom_css` in the cascade
(overrides the theme, overridden by `custom_css`). Every field is optional — set
only what you want to change.

```python
from montin import (
    Deck, ThemeOptions, Header, Bars, Cells, Fonts, Footer, Watermark, Logo,
)

deck = Deck(
    title="ACME Analytics",
    theme="montin",
    theme_options=ThemeOptions(
        header=Header(style="gradient", color="#E07A3F", subtitle_style="italic"),
        bars=Bars(sidebar="#0f1f2e", toolbar="#0f1f2e", text="#e9ecef"),
        cells=Cells(gap=16, radius=12, shadow=True),
        fonts=Fonts(family="Georgia, serif"),
        footer=Footer(text="ACME · Confidential · {title} · {page}/{total}", align="right"),
        watermark=Watermark(text="CONFIDENTIAL", opacity=0.06),
        logo=Logo(image="logo.svg", placement="header", height=28),
        credit=False,   # hide the "Made with Montin" toolbar credit
    ),
)
```

The deck above (rendered with the docs logo) — one `ThemeOptions` object driving
the header, chrome colours, footer, watermark and logo at once:

```{raw} html
<iframe class="montin-embed" src="../_static/deck/themeopts_branded.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

### Option groups

| Group | Fields |
|---|---|
| `Header` | `style` (`"ruler"` / `"background"` / `"gradient"`), `color`, `thickness`, `subtitle_style` (`"plain"`/`"italic"`/`"muted"`), `subtitle_color` |
| `Bars` | `sidebar`, `toolbar` (colour or gradient string), `text` (chrome text colour) |
| `Cells` | `gap`, `radius`, `border`, `shadow` (`True`/`False`/custom) |
| `Fonts` | `family`, `mono`, `color`, `scale` |
| `Footer` | `text` (tokens `{page}` `{total}` `{title}`), `height`, `color`, `background`, `align` |
| `Watermark` | `text` **or** `image`, `position` (`"center"`, corners, `"tiled"`), `opacity`, `size`, `color` |
| `Logo` | `image` **or** `text`, `placement` (`"sidebar"`/`"toolbar"`/`"header"`/`"cover"`), `height`, `link` |
| *(top level)* | `logo` accepts one `Logo` **or a list**; `credit=False` hides the Montin credit |

### Header styles

`Header(style=…)` restyles the slide title three ways — an accent **ruler**
(default), a translucent **background** band, or a **gradient** fade:

```{raw} html
<iframe class="montin-embed" src="../_static/deck/themeopts_header_ruler.html#demo"
        loading="lazy" allowfullscreen></iframe>
<iframe class="montin-embed" src="../_static/deck/themeopts_header_background.html#demo"
        loading="lazy" allowfullscreen></iframe>
<iframe class="montin-embed" src="../_static/deck/themeopts_header_gradient.html#demo"
        loading="lazy" allowfullscreen></iframe>
```

### Footer, watermark & logo

These three are *rendered elements*, not just CSS:

- **Footer** appears on every content slide. Its `text` fills the `{page}`,
  `{total}` and `{title}` tokens per slide.
- **Watermark** is a faint overlay (`text` or `image`) on every slide.
- **Logo** (`image` or `text`) is placed in the sidebar, toolbar, each slide
  header, or the cover — pass a list for several placements.

Image `logo`/`watermark` sources (path, URL, or base64) are embedded as data
URIs in self-contained mode, so they stay offline-safe — a local image works even
under `Security(block_external=True)` (an external URL there raises, as elsewhere).

### Save & reuse a tuned theme

`render_css()` returns the whole computed stylesheet; `export_css()` writes it to
a file you can share, hand-edit, and load back via `custom_css`:

```python
deck.export_css("brand.css")            # capture theme + theme_options as CSS
# later / elsewhere:
Deck(title="Report", custom_css="brand.css")
```

The export captures the *visual* theme (colours, header, bars, cells, fonts,
hidden credit). The rendered features (footer text, watermark, logo elements) are
content rather than CSS, so keep those as `theme_options`.

---

## CSS variables

Almost every colour, font, and radius in the deck resolves to one of these
custom properties, declared in `:root`. Redefining them — in a theme or in
`custom_css` — restyles the whole report consistently.

| Variable | Controls |
|---|---|
| `--color-bg` | Page background |
| `--color-surface` | Cards, sidebar, toolbar, modals |
| `--color-surface2` | Inputs, hover states, inline code, action buttons |
| `--color-accent` | Links, active slide, title underline, list markers, deltas |
| `--color-text` | Primary text |
| `--color-text-muted` | Secondary text — captions, subtitles, counters |
| `--color-border` | Hairlines and dividers |
| `--font-sans` | UI and body font stack |
| `--font-mono` | Code / monospace font stack |
| `--radius` | Corner radius for cards, buttons, inputs |

> Plotly charts read `--color-text` and `--color-border` at render time, so
> chart text and gridlines follow the active theme automatically.

---

## Tweak the look with `custom_css`

For a one-off rebrand you don't need a whole theme — pass `custom_css`. It
accepts either an **inline CSS string** or a **path to a `.css` file**, and is
applied after the theme, so anything you set here takes precedence.

Re-point the accent and round the corners, keeping everything else from the
chosen theme:

```python
deck = Deck(
    title="Report",
    theme="ink",
    custom_css=""":root {
        --color-accent: #E07A3F;
        --radius: 12px;
    }""",
)
```

Or keep your brand CSS in a file and reference it:

```python
deck = Deck(title="Report", custom_css="brand.css")
```

```css
/* brand.css — swap fonts and the accent for the default light theme */
:root {
    --font-sans:    "Inter", system-ui, sans-serif;
    --font-mono:    "JetBrains Mono", monospace;
    --color-accent: #E07A3F;
}
```

`custom_css` is not limited to variables — it is plain CSS appended to the
deck, so you can target any selector. For example, give metric cards a tinted
background:

```python
deck = Deck(
    title="Report",
    custom_css="""
        .cell-metric { background: color-mix(in srgb, var(--color-accent) 8%, var(--color-surface)); }
        .metric-value { color: var(--color-accent); }
    """,
)
```

---

## Build a full theme

For a reusable theme (rather than per-deck CSS), add a folder under
`montin/themes/<name>/`. Each file in it overrides one component; a file you
don't provide simply falls back to the `default` base. The recognised
component filenames are:

```
layout.css  slide.css  table.css  tabulator.css  list.css
toc.css     code.css   metric.css image.css      toolbar.css
```

The smallest useful theme is a single `layout.css` that redefines the colour
variables — the brand `ink` theme is essentially just this:

```css
/* montin/themes/ink/layout.css */
:root {
    --color-bg:        #0f1f2e;   /* Ink   */
    --color-surface:   #17293a;
    --color-surface2:  #20384b;
    --color-accent:    #e07a3f;   /* Accent */
    --color-text:      #e9ecef;   /* Sand  */
    --color-text-muted:#9aa6b2;   /* Stone */
    --color-border:    #35546b;   /* Slate */
}
```

Add a `metric.css` if the default delta colours (tuned for the light
background) need adjusting for your background:

```css
/* montin/themes/ink/metric.css — brighter deltas for a dark bg */
.delta-positive { color: #4ade80; }
.delta-negative { color: #f87171; }
```

Then select it like any built-in:

```python
deck = Deck(title="Report", theme="ink")
```

---

## Precedence recap

For any rule or variable, the **last definition wins**, applied in this order:

1. **`default` base** — full component stylesheets.
2. **Selected `theme`** — overrides on top.
3. **`theme_options`** — structured customization.
4. **`custom_css`** — your CSS, merged last.

So `custom_css` beats `theme_options`, which beats the theme, which beats the
base. Pick the closest built-in theme, reach for `theme_options` next, and drop
to `custom_css` only for anything the options don't cover.
