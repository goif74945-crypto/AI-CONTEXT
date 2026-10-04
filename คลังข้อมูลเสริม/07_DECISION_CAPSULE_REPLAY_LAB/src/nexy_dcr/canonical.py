from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

from .errors import CanonicalizationError

ZERO_HASH = "0" * 64


def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        # json.dumps(..., allow_nan=False) rejects NaN/Infinity, but we normalize
        # through a round trip so callers cannot smuggle non-standard numbers.
        return value
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("canonical mappings require string keys")
            normalized[key] = _normalize(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize(item) for item in value]
    raise CanonicalizationError(f"unsupported canonical value type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Return a stable UTF-8 JSON representation.

    Properties:
    - mapping keys are sorted;
    - insignificant whitespace is removed;
    - Unicode is preserved rather than ASCII-escaped;
    - NaN/Infinity are rejected;
    - unsupported Python objects are rejected explicitly.
    """

    try:
        return json.dumps(
            _normalize(value),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise CanonicalizationError(str(exc)) from exc


def sha256_hex(value: Any) -> str:
    payload = canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_sha256(value: str, *, field_name: str = "sha256") -> None:
    if len(value) != 64:
        raise CanonicalizationError(f"{field_name} must be 64 lowercase hex characters")
    if value.lower() != value:
        raise CanonicalizationError(f"{field_name} must be lowercase")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CanonicalizationError(f"{field_name} must be hexadecimal") from exc
