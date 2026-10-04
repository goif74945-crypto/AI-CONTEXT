from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


class CanonicalizationError(ValueError):
    pass


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        # Floats are intentionally rejected because cross-runtime canonical
        # representations and NaN/Infinity semantics are a poor fit for an
        # authority boundary.
        raise CanonicalizationError("floating-point values are not allowed")
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    if isinstance(value, (set, frozenset)):
        normalized = [_normalize(v) for v in value]
        return sorted(normalized, key=lambda v: json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("object keys must be strings")
            out[key] = _normalize(item)
        return out
    raise CanonicalizationError(f"unsupported canonical value type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    normalized = _normalize(value)
    try:
        return json.dumps(
            normalized,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise CanonicalizationError(str(exc)) from exc


def sha256_canonical(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
