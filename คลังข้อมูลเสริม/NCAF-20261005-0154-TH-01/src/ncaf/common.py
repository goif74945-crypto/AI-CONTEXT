from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


class ContractError(ValueError):
    """Raised when an input violates a deterministic companion contract."""


def canonical_data(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise ContractError("floating point values are forbidden in canonical contract data")
    if isinstance(value, Enum):
        return canonical_data(value.value)
    if is_dataclass(value):
        return canonical_data(asdict(value))
    if isinstance(value, tuple):
        return [canonical_data(v) for v in value]
    if isinstance(value, list):
        return [canonical_data(v) for v in value]
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key in sorted(value):
            if not isinstance(key, str):
                raise ContractError("canonical object keys must be strings")
            out[key] = canonical_data(value[key])
        return out
    raise ContractError(f"unsupported canonical type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonical_data(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def require_nonempty(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty string")
    return value
