"""
montin.io
=========
JSON (de)serialisation helpers shared by the ``export`` / ``from_file`` methods
of :class:`~montin.cells.base.Cell`, :class:`~montin.core.slide.Slide`, and
:class:`~montin.core.deck.Deck`.

Three responsibilities:

- A single file *envelope* — ``{"montin_format": N, "kind": ..., <kind>: ...}`` —
  written by :func:`write_document` and validated by :func:`read_document`.
- Transparent **gzip** compression: every ``export`` takes a ``compress``
  tri-state (``None`` => infer from a ``.gz`` suffix, ``True`` / ``False`` =>
  force); readers auto-detect gzip by its magic bytes, so a file loads whether
  or not its extension advertises compression.
- Small value sanitisers (:func:`json_safe`, :func:`embed_image_source`) used by
  the per-cell ``to_dict`` implementations.
"""

from __future__ import annotations

import gzip
import json
import math
from pathlib import Path
from typing import Any, Iterable

#: On-disk format version. Bumped when the layout changes incompatibly. A reader
#: refuses a file written by a *newer* format than it understands.
FORMAT_VERSION = 1

_GZIP_MAGIC = b"\x1f\x8b"


def _should_compress(path: Path, compress: bool | None) -> bool:
    """Resolve the ``compress`` tri-state for ``path``."""
    if compress is None:
        return path.suffix.lower() == ".gz"
    return bool(compress)


def write_document(
    path: str | Path,
    kind: str,
    payload: Any,
    *,
    compress: bool | None = None,
) -> Path:
    """Write a Montin document envelope to ``path`` and return the path.

    The envelope is ``{"montin_format": N, "kind": kind, kind: payload}``.
    ``compress`` is ``None`` (infer gzip from a ``.gz`` suffix), ``True`` (force
    gzip), or ``False`` (force plain JSON).
    """
    path = Path(path)
    document = {"montin_format": FORMAT_VERSION, "kind": kind, kind: payload}
    text = json.dumps(document, ensure_ascii=False, indent=2)
    path.parent.mkdir(parents=True, exist_ok=True)
    if _should_compress(path, compress):
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            fh.write(text)
    else:
        path.write_text(text, encoding="utf-8")
    return path


def read_document(
    path: str | Path,
    expected_kinds: str | Iterable[str],
) -> tuple[str, Any]:
    """Read a Montin document, decompressing gzip transparently.

    Validates ``montin_format`` and that ``kind`` is one of ``expected_kinds``.
    Returns ``(kind, payload)``. Raises :class:`~montin.exceptions.InvalidDataError`
    on a malformed, mismatched, or too-new file.
    """
    from montin.exceptions import InvalidDataError

    path = Path(path)
    raw = path.read_bytes()
    text = (gzip.decompress(raw) if raw[:2] == _GZIP_MAGIC else raw).decode("utf-8")

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise InvalidDataError(f"{path} is not valid Montin JSON: {exc}") from exc

    if not isinstance(document, dict) or "montin_format" not in document:
        raise InvalidDataError(
            f"{path} is not a Montin document (missing 'montin_format')."
        )
    if document["montin_format"] > FORMAT_VERSION:
        raise InvalidDataError(
            f"{path} was written with a newer Montin format "
            f"(v{document['montin_format']} > v{FORMAT_VERSION}); upgrade montin to read it."
        )

    kind = document.get("kind")
    allowed = {expected_kinds} if isinstance(expected_kinds, str) else set(expected_kinds)
    if kind not in allowed:
        raise InvalidDataError(
            f"{path} has kind={kind!r}, expected one of {sorted(allowed)}."
        )
    return kind, document.get(kind)


def json_safe(value: Any) -> Any:
    """Coerce ``value`` into a JSON-native form, recursively.

    Handles the non-JSON scalars that show up in table rows, list items, and
    metric values: ``NaN`` / ``Inf`` -> ``None``, datetimes -> ISO strings, numpy
    scalars -> Python scalars, sets / tuples -> lists. Anything still foreign
    falls back to ``str``.
    """
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(v) for v in value]
    if hasattr(value, "isoformat"):            # datetime / date / Timestamp
        try:
            return value.isoformat()
        except Exception:
            pass
    if hasattr(value, "item"):                 # numpy scalar and friends
        try:
            return json_safe(value.item())
        except Exception:
            pass
    return str(value)


def embed_image_source(
    source: Any, *, to_webp: bool = False, quality: int | None = None
) -> str:
    """Resolve an image source to an embeddable string (a ``data:`` URI or a
    pass-through URL / data URI).

    Mirrors the Assembler's self-contained resolution: a matplotlib ``Figure`` is
    encoded to a data URI; a local path is read and base64-encoded; URLs, ``data:``
    URIs, and bare base64 strings are returned unchanged. Used to embed image
    cells when ``export(..., embed=True)``.
    """
    if hasattr(source, "savefig"):             # matplotlib Figure
        from montin.utils.media import data_uri, figure_to_payload

        fmt = "webp" if to_webp else "svg"
        payload, mime, _ext, _is_text = figure_to_payload(source, fmt, 150, quality)
        return data_uri(payload, mime)

    from montin.utils.image_encoder import encode

    return encode(source)
