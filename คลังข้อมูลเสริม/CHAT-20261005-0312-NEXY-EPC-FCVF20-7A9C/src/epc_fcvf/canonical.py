from __future__ import annotations

import dataclasses
import hashlib
import json
from enum import Enum
from typing import Any

from .q64 import Q64


def to_primitive(value: Any) -> Any:
    if isinstance(value, Q64):
        return {"q64_raw": str(value.raw)}
    if isinstance(value, Enum):
        return value.value
    if dataclasses.is_dataclass(value):
        out = {}
        for field in dataclasses.fields(value):
            out[field.name] = to_primitive(getattr(value, field.name))
        return out
    if isinstance(value, dict):
        return {str(k): to_primitive(v) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))}
    if isinstance(value, tuple):
        return [to_primitive(v) for v in value]
    if isinstance(value, list):
        return [to_primitive(v) for v in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, float):
        raise TypeError("BINARY_FLOAT_FORBIDDEN")
    raise TypeError(f"UNSUPPORTED_CANONICAL_TYPE:{type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        to_primitive(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
