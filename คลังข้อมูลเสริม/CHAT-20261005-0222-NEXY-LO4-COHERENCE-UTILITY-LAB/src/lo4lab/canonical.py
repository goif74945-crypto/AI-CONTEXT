from __future__ import annotations

from dataclasses import asdict, is_dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any


class CanonicalizationError(ValueError):
    """Raised when a value cannot be represented in deterministic JSON."""


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        value = asdict(value)
    if value is None or isinstance(value, (bool, str, int)):
        return value
    if isinstance(value, float):
        if not isfinite(value):
            raise CanonicalizationError("non-finite floats are forbidden")
        return value
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("mapping keys must be strings")
            if key in out:
                raise CanonicalizationError(f"duplicate key: {key}")
            out[key] = _normalize(item)
        return {key: out[key] for key in sorted(out)}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if isinstance(value, (set, frozenset)):
        normalized = [_normalize(item) for item in value]
        return sorted(normalized, key=lambda item: canonical_json(item))
    raise CanonicalizationError(f"unsupported canonical type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        _normalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def fingerprint(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()
