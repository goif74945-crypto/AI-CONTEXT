from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from typing import Any

from .errors import CanonicalizationError

_MAX_DEPTH = 64


def _validate(value: Any, *, depth: int = 0) -> None:
    if depth > _MAX_DEPTH:
        raise CanonicalizationError(f"maximum nesting depth {_MAX_DEPTH} exceeded")
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalizationError("non-finite floats are forbidden")
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("object keys must be strings")
            _validate(item, depth=depth + 1)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            _validate(item, depth=depth + 1)
        return
    raise CanonicalizationError(f"unsupported type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Return stable UTF-8 JSON suitable for hashing and replay identity."""
    _validate(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
