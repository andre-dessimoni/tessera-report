"""Tests for the theme system — resolution and CSS generation."""

import pytest

from montin import Deck
from montin.exceptions import ThemeNotFoundError
from montin.utils.theme_resolver import ThemeResolver

SUPPORTED_THEMES = [
    "default", "montin", "ink", "midnight", "docs", "docs-dark",
    "light", "dark", "light-blue", "academic", "sobrio",
]


# ---------------------------------------------------------------------------
# ThemeResolver
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("theme", SUPPORTED_THEMES)
def test_theme_resolves_without_error(theme):
    css = ThemeResolver().resolve(theme)
    assert isinstance(css, str)
    assert len(css) > 0


def test_unknown_theme_raises():
    with pytest.raises(ThemeNotFoundError, match="does-not-exist"):
        ThemeResolver().resolve("does-not-exist")


# ---------------------------------------------------------------------------
# CSS variable presence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("theme", SUPPORTED_THEMES)
def test_css_contains_accent_variable(theme):
    css = ThemeResolver().resolve(theme)
    assert "--color-accent" in css


@pytest.mark.parametrize("theme", SUPPORTED_THEMES)
def test_css_contains_surface_variable(theme):
    css = ThemeResolver().resolve(theme)
    assert "--color-surface" in css


# ---------------------------------------------------------------------------
# Theme-specific overrides
# ---------------------------------------------------------------------------

def test_default_theme_is_docs_light():
    css = ThemeResolver().resolve("default")
    # The default look is now the documentation-site light theme.
    assert "#2757dd" in css        # Furo brand-content link blue
    assert ".theme-default #sidebar" in css   # grey chrome, scoped to default
    assert "Inter" in css          # docs-site body font


def test_montin_theme_uses_brand_sand_background():
    css = ThemeResolver().resolve("montin")
    # The brand "Sand" light palette moved from default to the `montin` theme.
    assert "#e9ecef" in css        # Sand background
    assert "#e07a3f" in css        # Accent


def test_slide_title_spans_full_width_by_default():
    # display:block makes the accent underline reach the right margin.
    css = ThemeResolver().resolve("default")
    rule = css.split(".slide-title {", 1)[1].split("}", 1)[0]
    assert "display: block" in rule


def test_ink_theme_uses_brand_ink_background():
    css = ThemeResolver().resolve("ink")
    # ink is the brand dark theme; the last :root wins.
    assert "#0f1f2e" in css        # Ink background
    assert "#e07a3f" in css        # Accent


def test_midnight_theme_preserves_original_default():
    css = ThemeResolver().resolve("midnight")
    # midnight keeps the original navy + pink-red look.
    assert "#1a1a2e" in css        # navy background
    assert "#e94560" in css        # pink-red accent


def test_docs_theme_matches_furo_light():
    css = ThemeResolver().resolve("docs")
    assert "#f8f9fb" in css        # Furo secondary (sidebar/toolbar)
    assert "#2757dd" in css        # Furo brand-content link blue
    assert "Sora" in css           # docs-site heading font


def test_docs_dark_theme_matches_furo_dark():
    css = ThemeResolver().resolve("docs-dark")
    assert "#131416" in css        # Furo dark content background
    assert "#5ca5ff" in css        # Furo dark link blue
    assert "Sora" in css


def test_light_theme_overrides_background():
    css = ThemeResolver().resolve("light")
    # Light theme defines a light bg; the last :root wins
    assert "#f4f4f5" in css


def test_dark_theme_overrides_background():
    css = ThemeResolver().resolve("dark")
    assert "#1e1e1e" in css


def test_light_blue_theme_overrides_background():
    css = ThemeResolver().resolve("light-blue")
    assert "#eff6ff" in css


def test_academic_theme_uses_serif_font():
    css = ThemeResolver().resolve("academic")
    assert "Georgia" in css or "serif" in css


def test_sobrio_theme_overrides_background():
    css = ThemeResolver().resolve("sobrio")
    assert "#ffffff" in css


def test_light_theme_delta_colours():
    css = ThemeResolver().resolve("light")
    # Accessible green/red for light backgrounds
    assert "#16a34a" in css
    assert "#dc2626" in css


def test_sobrio_has_no_title_border():
    css = ThemeResolver().resolve("sobrio")
    assert "border-bottom: none" in css


def test_academic_has_thin_title_border():
    css = ThemeResolver().resolve("academic")
    assert "1px solid var(--color-border)" in css


# ---------------------------------------------------------------------------
# custom_css — inline string vs. file path (both must be injected, last)
# ---------------------------------------------------------------------------

def test_inline_custom_css_string_is_injected():
    # A str holding CSS is used inline (not mistaken for a file path).
    css = ThemeResolver().resolve("default", ".slide-title { display: block; }")
    assert ".slide-title { display: block; }" in css
    # ...and it lands after the base rule so it wins the cascade.
    assert css.rindex("display: block") > css.index("display: inline-block")


def test_custom_css_file_path_is_read(tmp_path):
    f = tmp_path / "brand.css"
    f.write_text(".slide-title { color: red; }", encoding="utf-8")
    css = ThemeResolver().resolve("default", f)
    assert "color: red" in css


def test_custom_css_file_path_as_string_is_read(tmp_path):
    f = tmp_path / "brand.css"
    f.write_text(".cell { color: blue; }", encoding="utf-8")
    css = ThemeResolver().resolve("default", str(f))
    assert "color: blue" in css


def test_inline_custom_css_survives_deck(tmp_path):
    # End-to-end: Deck no longer coerces the str to a (missing) Path.
    deck = Deck(title="T", custom_css=".slide-title { display: block; }")
    s = deck.add_slide("S", nrows=1, ncols=1)
    s.add_text("hi")
    out = deck.write(tmp_path / "out", open_browser=False)
    assert ".slide-title { display: block; }" in out.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# End-to-end: write() with each theme
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("theme", SUPPORTED_THEMES)
def test_write_with_theme(tmp_path, theme):
    deck = Deck(title="Test", theme=theme)
    s = deck.add_slide("S", nrows=1, ncols=1)
    s.add_metric(value=99, label="Score", delta=+5, delta_label="vs last")
    out = deck.write(tmp_path / f"out_{theme}", open_browser=False)
    assert out.exists()
    html = out.read_text(encoding="utf-8")
    assert "Test" in html
    assert "Score" in html
