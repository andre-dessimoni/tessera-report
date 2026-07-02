"""
montin.core.theme_options
==========================
``ThemeOptions`` — a structured customization layer that sits between the chosen
``theme`` and ``custom_css`` in the cascade (default → theme → **theme_options**
→ custom_css). It groups common branding knobs into small nested dataclasses and
emits the CSS for them via :meth:`ThemeOptions.to_css`; the rendered features
(footer, watermark, logo) are turned into HTML by the assembler/template.

Every field is optional so a partial ``ThemeOptions`` only overrides what it sets.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any, Literal


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _len(value: int | str | None) -> str | None:
    """Normalise a CSS length: a bare ``int`` becomes ``"<n>px"``; a string
    (``"1rem"``, ``"12px"``, ``"2fr"``) is passed through."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return f"{value}px"
    return str(value)


# ---------------------------------------------------------------------------
# nested option groups
# ---------------------------------------------------------------------------

@dataclass
class Header:
    """Slide-title (header) styling.

    Attributes:
        style: ``"ruler"`` (accent underline, the default), ``"background"``
            (title sits in a translucent band of ``color``), or ``"gradient"``
            (a horizontal fade of ``color``).
        color: Header accent colour. Defaults to the theme's ``--color-accent``.
        thickness: Ruler thickness in px (``"ruler"`` style only; default 2).
        subtitle_style: ``"plain"``, ``"italic"``, or ``"muted"``.
        subtitle_color: Explicit subtitle colour.
    """

    style:          Literal["ruler", "background", "gradient"] = "ruler"
    color:          str | None = None
    thickness:      int | None = None
    subtitle_style: Literal["plain", "italic", "muted"] | None = None
    subtitle_color: str | None = None


@dataclass
class Bars:
    """Sidebar + toolbar (chrome) colours.

    Attributes:
        sidebar: Sidebar background — a colour or a full ``gradient(...)`` string.
        toolbar: Toolbar background — a colour or gradient string.
        text: Chrome text colour (sidebar items / toolbar), optional.
    """

    sidebar: str | None = None
    toolbar: str | None = None
    text:    str | None = None


@dataclass
class Cells:
    """Cell grid spacing and card styling.

    Attributes:
        gap: Grid gap between cells (px int or CSS length).
        radius: Card corner radius (px int or CSS length).
        border: Card border colour.
        shadow: ``True`` for a soft shadow, ``False`` for none, or a custom
            ``box-shadow`` string.
    """

    gap:    int | str | None = None
    radius: int | str | None = None
    border: str | None = None
    shadow: bool | str | None = None


@dataclass
class Fonts:
    """Typography.

    Attributes:
        family: Body/UI font stack (``--font-sans``).
        mono: Monospace font stack (``--font-mono``).
        color: Primary text colour (``--color-text``).
        scale: Deck-wide font scale. Overrides ``Deck(fontsize_scale=…)`` when set
            (same ``--deck-font-scale`` mechanism — this is not a second system).
    """

    family: str | None = None
    mono:   str | None = None
    color:  str | None = None
    scale:  float | None = None


@dataclass
class Footer:
    """A footer strip rendered on every content slide.

    ``text`` supports the tokens ``{page}``, ``{total}`` and ``{title}``, filled
    per slide at render time.

    Attributes:
        text: Footer text (with optional tokens).
        height: Reserved footer height (px or CSS length); optional.
        color: Text colour.
        background: Footer background colour.
        align: ``"left"``, ``"center"`` (default) or ``"right"``.
    """

    text:       str = ""
    height:     int | str | None = None
    color:      str | None = None
    background: str | None = None
    align:      Literal["left", "center", "right"] = "center"


@dataclass
class Watermark:
    """A faint overlay drawn on every slide (text or image).

    Attributes:
        text: Watermark text (mutually exclusive with ``image``).
        image: Path / URL / base64 for an image watermark (embedded as a data
            URI in self-contained mode).
        position: ``"center"`` (default), a corner (``"top-left"`` …), or
            ``"tiled"`` (image only; text falls back to centred).
        opacity: 0–1 (default ``0.08``).
        size: Font size (text) or width (image) — px int or CSS length.
        color: Text-watermark colour (defaults to the theme text colour).
    """

    text:     str | None = None
    image:    str | Path | None = None
    position: Literal["center", "top-left", "top-right",
                      "bottom-left", "bottom-right", "tiled"] = "center"
    opacity:  float = 0.08
    size:     int | str | None = None
    color:    str | None = None


@dataclass
class Logo:
    """A logo (image or text) placed in the chrome or on slides.

    Attributes:
        image: Path / URL / base64 for the logo image (embedded as a data URI in
            self-contained mode).
        text: Text logo/wordmark (used when ``image`` is not set).
        placement: ``"sidebar"`` (default), ``"toolbar"``, ``"header"`` (every
            content slide) or ``"cover"`` (title/section slides).
        height: Logo height (px or CSS length).
        link: Optional URL — wraps the logo in a link.
    """

    image:     str | Path | None = None
    text:      str | None = None
    placement: Literal["sidebar", "toolbar", "header", "cover"] = "sidebar"
    height:    int | str | None = None
    link:      str | None = None


# ---------------------------------------------------------------------------
# container
# ---------------------------------------------------------------------------

@dataclass
class ThemeOptions:
    """Structured theme customization passed as ``Deck(theme_options=…)``.

    Overrides the chosen ``theme`` but is itself overridden by ``custom_css``.
    See :class:`Header`, :class:`Bars`, :class:`Cells`, :class:`Fonts`,
    :class:`Footer`, :class:`Watermark` and :class:`Logo`.

    Attributes:
        header, bars, cells, fonts, footer, watermark: The option groups above.
        logo: One :class:`Logo` or a list of them (several placements).
        credit: ``False`` hides the "Made with Montin" toolbar credit.
    """

    header:    Header | None = None
    bars:      Bars | None = None
    cells:     Cells | None = None
    fonts:     Fonts | None = None
    footer:    Footer | None = None
    watermark: Watermark | None = None
    logo:      "Logo | list[Logo] | None" = None
    credit:    bool = True

    # ------------------------------------------------------------------
    # CSS generation (the injected layer)
    # ------------------------------------------------------------------

    def to_css(self) -> str:
        """Return the CSS for the CSS-generatable options (everything except the
        footer/watermark/logo *content*, which is HTML). Empty string when nothing
        is set."""
        parts: list[str] = []
        root: list[str] = []

        if self.fonts:
            f = self.fonts
            if f.family is not None: root.append(f"  --font-sans: {f.family};")
            if f.mono is not None:   root.append(f"  --font-mono: {f.mono};")
            if f.color is not None:  root.append(f"  --color-text: {f.color};")
            if f.scale is not None:  root.append(f"  --deck-font-scale: {f.scale};")
        if self.cells:
            c = self.cells
            if c.gap is not None:    root.append(f"  --cell-gap: {_len(c.gap)};")
            if c.radius is not None: root.append(f"  --radius: {_len(c.radius)};")
        if self.header and self.header.color is not None:
            root.append(f"  --header-color: {self.header.color};")
        if self.watermark and self.watermark.opacity is not None:
            root.append(f"  --wm-opacity: {self.watermark.opacity};")
        if self.watermark and self.watermark.color is not None:
            root.append(f"  --wm-color: {self.watermark.color};")
        if self.watermark and self.watermark.size is not None:
            root.append(f"  --wm-size: {_len(self.watermark.size)};")

        if root:
            parts.append(":root {\n" + "\n".join(root) + "\n}")

        parts += self._header_css()
        parts += self._bars_css()
        parts += self._cells_css()
        parts += self._footer_css()

        if not self.credit:
            parts.append("#toolbar-credit { display: none; }")

        return "\n".join(parts)

    def _header_css(self) -> list[str]:
        h = self.header
        if not h:
            return []
        out: list[str] = []
        if h.style == "ruler":
            thk = f"{h.thickness}px" if h.thickness else "2px"
            out.append(f".slide-title {{ border-bottom: {thk} solid var(--header-color); }}")
        elif h.style == "background":
            out.append(
                ".slide-title {"
                " border-bottom: none;"
                " background: color-mix(in srgb, var(--header-color) 15%, transparent);"
                " padding: 6px 10px; border-radius: var(--radius); }"
            )
        elif h.style == "gradient":
            out.append(
                ".slide-title {"
                " border-bottom: none;"
                " background: linear-gradient(90deg,"
                " color-mix(in srgb, var(--header-color) 22%, transparent), transparent);"
                " padding: 6px 10px; border-radius: var(--radius); }"
            )
        sub: list[str] = []
        if h.subtitle_style == "italic":
            sub.append("font-style: italic;")
        elif h.subtitle_style == "muted":
            sub.append("opacity: 0.75;")
        elif h.subtitle_style == "plain":
            sub.append("font-style: normal; opacity: 1;")
        if h.subtitle_color is not None:
            sub.append(f"color: {h.subtitle_color};")
        if sub:
            out.append(".slide-subtitle, .slide-cover-subtitle { " + " ".join(sub) + " }")
        return out

    def _bars_css(self) -> list[str]:
        b = self.bars
        if not b:
            return []
        out: list[str] = []
        if b.sidebar is not None:
            out.append(f"#sidebar {{ background: {b.sidebar}; }}")
        if b.toolbar is not None:
            out.append(f"#toolbar {{ background: {b.toolbar}; }}")
        if b.text is not None:
            out.append(
                f"#sidebar, #sidebar .sidebar-item, #toolbar, #toolbar button "
                f"{{ color: {b.text}; }}"
            )
        return out

    def _cells_css(self) -> list[str]:
        c = self.cells
        if not c:
            return []
        out: list[str] = []
        if c.border is not None:
            out.append(f".cell {{ border-color: {c.border}; }}")
        if c.shadow is not None:
            if c.shadow is True:
                shadow = "0 1px 2px rgba(0,0,0,0.05), 0 6px 16px rgba(0,0,0,0.06)"
            elif c.shadow is False:
                shadow = "none"
            else:
                shadow = str(c.shadow)
            out.append(f".cell {{ box-shadow: {shadow}; }}")
        return out

    def _footer_css(self) -> list[str]:
        f = self.footer
        if not f:
            return []
        decl: list[str] = []
        if f.height is not None:     decl.append(f"min-height: {_len(f.height)};")
        if f.color is not None:      decl.append(f"color: {f.color};")
        if f.background is not None: decl.append(f"background: {f.background};")
        if not decl:
            return []
        return [".slide-footer { " + " ".join(decl) + " }"]

    # ------------------------------------------------------------------
    # view-model helpers (consumed by the assembler / template)
    # ------------------------------------------------------------------

    def logos(self) -> list[Logo]:
        """Normalise ``logo`` to a (possibly empty) list."""
        if self.logo is None:
            return []
        if isinstance(self.logo, Logo):
            return [self.logo]
        return list(self.logo)

    def footer_text_for(self, page: int, total: int, title: str) -> str:
        """Fill the footer ``{page}``/``{total}``/``{title}`` tokens (raw text —
        the template escapes it)."""
        if not self.footer:
            return ""
        return (
            self.footer.text
            .replace("{page}", str(page))
            .replace("{total}", str(total))
            .replace("{title}", title)
        )

    # ------------------------------------------------------------------
    # serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """JSON-native dict (Paths → str), mirroring ``Deck.to_dict``."""
        def conv(v: Any) -> Any:
            if is_dataclass(v):
                return {f.name: conv(getattr(v, f.name)) for f in fields(v)}
            if isinstance(v, list):
                return [conv(x) for x in v]
            if isinstance(v, Path):
                return str(v)
            return v
        return conv(self)

    @classmethod
    def from_dict(cls, data: dict | None) -> "ThemeOptions | None":
        if not data:
            return None

        def build(kind, value):
            if value is None:
                return None
            return kind(**value)

        logo_data = data.get("logo")
        if isinstance(logo_data, list):
            logo: Any = [Logo(**d) for d in logo_data]
        else:
            logo = build(Logo, logo_data)

        return cls(
            header    = build(Header, data.get("header")),
            bars      = build(Bars, data.get("bars")),
            cells     = build(Cells, data.get("cells")),
            fonts     = build(Fonts, data.get("fonts")),
            footer    = build(Footer, data.get("footer")),
            watermark = build(Watermark, data.get("watermark")),
            logo      = logo,
            credit    = data.get("credit", True),
        )
