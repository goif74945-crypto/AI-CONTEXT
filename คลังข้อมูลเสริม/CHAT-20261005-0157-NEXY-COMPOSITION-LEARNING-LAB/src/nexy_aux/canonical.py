from __future__ import annotations

import dataclasses
import hashlib
import json
import math
from collections.abc import Mapping, Set
from typing import Any


def normalize(value: Any) -> Any:
    """Convert supported Python values into a deterministic JSON-compatible form.

    Canonicalization fails closed for values that JSON cannot represent portably,
    including NaN/Infinity and mapping keys that collide after string conversion.
    """
    if dataclasses.is_dataclass(value):
        value = dataclasses.asdict(value)
    if isinstance(value, Mapping):
        out: dict[str, Any] = {}
        for key in sorted(value, key=lambda x: str(x)):
            normalized_key = str(key)
            if normalized_key in out:
                raise ValueError(f"canonical mapping key collision: {normalized_key!r}")
            out[normalized_key] = normalize(value[key])
        return out
    if isinstance(value, Set) and not isinstance(value, (str, bytes, bytearray)):
        normalized = [normalize(v) for v in value]
        return sorted(
            normalized,
            key=lambda x: json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False),
        )
    if isinstance(value, tuple):
        return [normalize(v) for v in value]
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite floats are forbidden in canonical JSON")
        return value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise TypeError(f"Unsupported canonical value type: {type(value).__name__}")


def dumps(value: Any) -> str:
    return json.dumps(
        normalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def sha256(value: Any) -> str:
    return hashlib.sha256(dumps(value).encode("utf-8")).hexdigest()
