from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Mapping


class FrontierStatus(str, Enum):
    PASS = "PASS"
    FREEZE = "FREEZE"
    NOT_VERIFIED = "NOT_VERIFIED"


class FrontierInputError(ValueError):
    """Raised when a prototype receives structurally invalid input."""


def require_text(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise FrontierInputError(f"{field}:NOT_STRING")
    value = value.strip()
    if not value:
        raise FrontierInputError(f"{field}:EMPTY")
    return value


def canonicalize(value: Any) -> Any:
    if is_dataclass(value):
        return canonicalize(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(k): canonicalize(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (tuple, list)):
        return [canonicalize(v) for v in value]
    if isinstance(value, set):
        return [canonicalize(v) for v in sorted(value, key=repr)]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise FrontierInputError(f"NON_CANONICAL_TYPE:{type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonicalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def stable_hash(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()
