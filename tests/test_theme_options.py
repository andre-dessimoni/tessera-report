"""Tests for ThemeOptions — the structured customization layer."""

import pytest

from montin import (
    Bars, Cells, Deck, Fonts, Footer, Header, Logo, Security, ThemeOptions,
    Watermark,
)
from montin.exceptions import SecurityError
from montin.utils.theme_resolver import ThemeResolver

LOGO = "docs/_static/montin-logo-vertical.svg"


# ---------------------------------------------------------------------------
# to_css() — CSS-generatable options
# ---------------------------------------------------------------------------

def test_empty_options_emit_no_css():
    assert ThemeOptions().to_css() == ""


def test_header_ruler_uses_header_color_var():
    css = ThemeOptions(header=Header(style="ruler", color="#E07A3F")).to_css()
    assert "--header-color: #E07A3F" in css
    assert "border-bottom: 2px solid var(--header-color)" in css


def test_header_background_style_uses_color_mix():
    css = ThemeOptions(header=Header(style="background", color="#123456")).to_css()
    assert "color-mix(in srgb, var(--header-color) 15%, transparent)" in css
    assert "border-bottom: none" in css


def test_header_gradient_style():
    css = ThemeOptions(header=Header(style="gradient")).to_css()
    assert "linear-gradient(90deg" in css


def test_bars_colours():
    css = ThemeOptions(bars=Bars(sidebar="#0f1f2e", toolbar="#101010")).to_css()
    assert "#sidebar { background: #0f1f2e; }" in css
    assert "#toolbar { background: #101010; }" in css


def test_cells_gap_and_radius_are_lengths():
    css = ThemeOptions(cells=Cells(gap=20, radius="1rem")).to_css()
    assert "--cell-gap: 20px" in css
    assert "--radius: 1rem" in css


def test_fonts():
    css = ThemeOptions(fonts=Fonts(family="Georgia, serif", color="#111")).to_css()
    assert "--font-sans: Georgia, serif" in css
    assert "--color-text: #111" in css


def test_credit_false_hides_toolbar_credit():
    assert "#toolbar-credit { display: none; }" in ThemeOptions(credit=False).to_css()
    assert "toolbar-credit" not in ThemeOptions(credit=True).to_css()


# ---------------------------------------------------------------------------
# hierarchy: default -> theme -> theme_options -> custom_css
# ---------------------------------------------------------------------------

def test_options_css_sits_between_theme_and_custom_css():
    options_css = ThemeOptions(cells=Cells(radius=99)).to_css()
    css = ThemeResolver().resolve(
        "montin", custom_css=".x{}", options_css=options_css,
    )
    i_theme  = css.index("montin/layout.css") if "montin/layout.css" in css else css.index("Sand")
    i_opts   = css.index("/* --- theme_options --- */")
    i_custom = css.index("/* --- custom_css --- */")
    assert i_theme < i_opts < i_custom


# ---------------------------------------------------------------------------
# rendered features (footer / watermark / logo) in the HTML
# ---------------------------------------------------------------------------

def _deck(**opts_kw):
    d = Deck(title="T", theme="montin", theme_options=ThemeOptions(**opts_kw))
    d.add_title("Cover")
    d.add_slide("Results").add_text("hi")
    return d


def test_footer_tokens_filled_per_slide():
    html = _deck(footer=Footer(text="{title} {page}/{total}")).render()
    # 2 slides; the content slide fills its title + position.
    assert "Results 2/2" in html
    assert 'class="slide-footer footer-center"' in html


def test_footer_not_on_title_cover():
    html = _deck(footer=Footer(text="FT")).render()
    # The title cover (slide 1) has no footer element; the content slide does.
    assert html.count('<footer class="slide-footer') == 1


def test_text_watermark_rendered():
    html = _deck(watermark=Watermark(text="DRAFT", position="top-right")).render()
    assert 'class="slide-watermark wm-text wm-top-right"' in html
    assert ">DRAFT<" in html


def test_logo_text_in_sidebar():
    html = _deck(logo=Logo(text="ACME", placement="sidebar")).render()
    assert "deck-logo" in html
    assert "ACME" in html


def test_logo_image_embedded_as_data_uri():
    html = _deck(logo=Logo(image=LOGO, placement="header")).render()
    assert 'src="data:image/svg+xml' in html


# ---------------------------------------------------------------------------
# security
# ---------------------------------------------------------------------------

def test_block_external_allows_local_logo():
    d = Deck(title="T", theme="montin",
             theme_options=ThemeOptions(logo=Logo(image=LOGO)),
             security=Security(block_external=True))
    d.add_slide("S").add_text("x")
    assert "data:image/svg+xml" in d.render()


def test_block_external_rejects_external_image():
    d = Deck(title="T", theme="montin",
             theme_options=ThemeOptions(watermark=Watermark(image="https://e.com/w.png")),
             security=Security(block_external=True))
    d.add_slide("S").add_text("x")
    with pytest.raises(SecurityError):
        d.render()


# ---------------------------------------------------------------------------
# CSS export & round-trip
# ---------------------------------------------------------------------------

def test_export_css_matches_render_css(tmp_path):
    d = _deck(header=Header(style="gradient"), credit=False)
    p = d.export_css(tmp_path / "brand")
    assert p.suffix == ".css"
    assert p.read_text(encoding="utf-8") == d.render_css()


def test_exported_css_reloads_via_custom_css(tmp_path):
    d = _deck(cells=Cells(radius=13))
    p = d.export_css(tmp_path / "brand.css")
    d2 = Deck(title="Reused", custom_css=str(p))
    d2.add_slide("S").add_text("x")
    assert "--radius: 13px" in d2.render()


# ---------------------------------------------------------------------------
# serialization
# ---------------------------------------------------------------------------

def test_theme_options_survive_roundtrip():
    opts = ThemeOptions(
        header=Header(style="background", color="#abc"),
        footer=Footer(text="hi {page}"),
        logo=[Logo(text="A", placement="sidebar"), Logo(text="B", placement="toolbar")],
        credit=False,
    )
    d = Deck(title="T", theme="ink", theme_options=opts)
    d.add_slide("S").add_text("x")
    d2 = Deck.from_dict(d.to_dict())
    assert d2.theme_options.header.style == "background"
    assert d2.theme_options.footer.text == "hi {page}"
    assert len(d2.theme_options.logos()) == 2
    assert d2.theme_options.credit is False
