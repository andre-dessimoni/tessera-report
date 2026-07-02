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

The stylesheet for a deck is assembled in **three layers**, each able to
override the one before it:

1. **Base** — the `default` theme ships the complete set of component
   stylesheets (layout, slide, table, tabulator, list, toc, code, metric,
   image, toolbar). It is *always* loaded first, so every theme inherits a
   working layout and only has to change what it wants to look different.
2. **Theme** — the theme you select (`ink`, `dark`, …) layers on top,
   typically just re-declaring the colour variables in its `layout.css`.
3. **`custom_css`** — your own CSS, merged **last**, so it always wins.

Because the base supplies all the structure, a theme can be as small as a
single `:root` block that redefines a handful of variables.

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
3. **`custom_css`** — your CSS, merged last.

So `custom_css` always beats the theme, and the theme always beats the base.
Pick the closest built-in theme, then nudge the rest with `custom_css`.
