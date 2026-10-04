from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any

from .q64 import Q64


def normalize(value: Any) -> Any:
    if isinstance(value, Q64):
        return {"q64_raw": value.raw}
    if is_dataclass(value):
        return normalize(asdict(value))
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key in sorted(value.keys()):
            if not isinstance(key, str):
                raise TypeError("canonical object keys must be strings")
            normalized[key] = normalize(value[key])
        return normalized
    if isinstance(value, tuple):
        return [normalize(item) for item in value]
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(normalize(value), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
