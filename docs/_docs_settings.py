"""Shared settings for the docs example generator scripts.

The generator scripts under ``docs/examples/*/*.py`` each import this module and
apply the values to their ``Deck`` so every embedded preview is standardized.
Edit the values in ``docs/script-settings.yaml``.

These generators only run locally (``make.bat html`` / ``make.bat deck``); Read
the Docs serves the committed ``_static/*.html`` instead, so this module is not
imported during an RTD build.
"""

from __future__ import annotations

from pathlib import Path

import yaml

_SETTINGS_FILE = Path(__file__).resolve().parent / "script-settings.yaml"


def load_settings() -> dict:
    """Return the docs script settings, or ``{}`` if the file is absent."""
    if not _SETTINGS_FILE.exists():
        return {}
    return yaml.safe_load(_SETTINGS_FILE.read_text(encoding="utf-8")) or {}


SETTINGS = load_settings()

# Font scale applied to every generated docs deck (Deck(fontsize_scale=...)).
FONTSCALE: float = float(SETTINGS.get("fontscale", 1.0))
