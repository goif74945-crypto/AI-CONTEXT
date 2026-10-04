from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any

_WS_RE = re.compile(r"\s+")
_WORD_RE = re.compile(r"[^\W_]+", flags=re.UNICODE)


def normalize_text(value: str) -> str:
    """Return a deterministic display-preserving text normalization.

    NFC is intentionally used instead of compatibility normalization so the
    canonicalizer does not silently rewrite compatibility characters.
    """

    if not isinstance(value, str):
        raise TypeError("normalize_text requires str")
    return _WS_RE.sub(" ", unicodedata.normalize("NFC", value).strip())


def matching_text(value: str) -> str:
    """Return deterministic comparison text.

    Case-folding is used only for duplicate detection. The original normalized
    text remains part of the canonical proposal and its fingerprint.
    """

    return normalize_text(value).casefold()


def canonicalize(value: Any) -> Any:
    """Canonicalize JSON-compatible data without inventing semantics.

    Dictionary keys are sorted during serialization, while list order is kept
    because some proposal fields may intentionally encode priority/order.
    """

    if isinstance(value, str):
        return normalize_text(value)
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        raise TypeError("floating-point values are forbidden in canonical proposal data")
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical object keys must be strings")
            normalized_key = normalize_text(key)
            if normalized_key in normalized:
                raise ValueError(f"canonical key collision after normalization: {normalized_key!r}")
            normalized[normalized_key] = canonicalize(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [canonicalize(item) for item in value]
    raise TypeError(f"unsupported canonical value type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        canonicalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def word_units(value: str) -> frozenset[str]:
    return frozenset(match.group(0) for match in _WORD_RE.finditer(matching_text(value)))


def ngram_units(value: str, *, n: int = 3) -> frozenset[str]:
    if n < 2:
        raise ValueError("n must be >= 2")
    compact = " ".join(sorted(word_units(value)))
    if not compact:
        return frozenset()
    if len(compact) <= n:
        return frozenset({compact})
    return frozenset(compact[i : i + n] for i in range(len(compact) - n + 1))


def jaccard_basis_points(left: frozenset[str], right: frozenset[str]) -> int:
    """Return an integer Jaccard score in [0, 10000]."""

    if not left and not right:
        return 10_000
    union = left | right
    if not union:
        return 10_000
    return (len(left & right) * 10_000) // len(union)
