"""Canonical serialization and hashing helpers."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any

from .q64 import Q64


def _normalize(value: Any) -> Any:
    if isinstance(value, Q64):
        return {"q64_raw": value.canonical()}
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {field.name: _normalize(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {str(k): _normalize(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (tuple, list)):
        return [_normalize(v) for v in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    raise TypeError(f"unsupported canonical type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()
