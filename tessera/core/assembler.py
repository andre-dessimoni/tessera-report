"""
tessera.core.assembler
=======================
Consumes a populated ``HTMLSlides`` instance and writes the final .html file.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import jinja2
from importlib.resources import files as _res_files

from tessera.cells import ImageCell, ImageSliderCell
from tessera.utils.theme_resolver import ThemeResolver

if TYPE_CHECKING:
    from tessera.core.slides import HTMLSlides


def _templates_dir() -> Path:
    return Path(str(_res_files("tessera.templates")))


def _static_dir() -> Path:
    return Path(str(_res_files("tessera.static")))


class Assembler:
    def __init__(self, deck: "HTMLSlides") -> None:
        self.deck = deck
        self._env = self._build_jinja_env()

    def write(self, path: Path) -> None:
        html = self._render()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")

    def _build_jinja_env(self) -> jinja2.Environment:
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(_templates_dir())),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _render(self) -> str:
        deck = self.deck

        # CSS — theme merge
        css = ThemeResolver().resolve(deck.theme, deck.custom_css)

        # Main JS
        js_path = _static_dir() / "main.js"
        main_js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""

        # Resolve ImageCell.resolved_src (base64 if self_contained, otherwise src as-is)
        if deck.self_contained:
            from tessera.utils.image_encoder import encode
            for slide in deck._slides:
                for cell in slide._cells:
                    if isinstance(cell, ImageCell) and not cell.resolved_src:
                        try:
                            cell.resolved_src = encode(cell.source)
                        except FileNotFoundError:
                            cell.resolved_src = str(cell.source)
                    elif isinstance(cell, ImageSliderCell) and not cell.resolved_srcs:
                        srcs = []
                        for s in cell.sources:
                            try:
                                srcs.append(encode(s))
                            except FileNotFoundError:
                                srcs.append(str(s))
                        cell.resolved_srcs = srcs
        else:
            for slide in deck._slides:
                for cell in slide._cells:
                    if isinstance(cell, ImageCell) and not cell.resolved_src:
                        cell.resolved_src = str(cell.source)
                    elif isinstance(cell, ImageSliderCell) and not cell.resolved_srcs:
                        cell.resolved_srcs = [str(s) for s in cell.sources]

        # Render cells
        rendered_slides = []
        for slide in deck._slides:
            rendered_cells = [cell.render(self._env) for cell in slide._cells]
            rendered_slides.append({
                "slide": slide,
                "rendered_cells": rendered_cells,
            })

        return self._env.get_template("base.html").render(
            deck=deck,
            rendered_slides=rendered_slides,
            css=css,
            main_js=main_js,
            plugins=deck.plugins,
            plugin_names=deck._plugin_names,
        )
