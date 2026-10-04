from __future__ import annotations

from dataclasses import asdict, is_dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

from .q64 import Q64


class ContractError(ValueError):
    pass


def require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be non-empty text")
    return value


def require_unit(value: Q64, field: str) -> Q64:
    if not isinstance(value, Q64) or not value.is_unit_interval():
        raise ContractError(f"{field} must be Q64.64 in [0,1]")
    return value


def canonicalize(value: Any) -> Any:
    if isinstance(value, Q64):
        return value.canonical()
    if is_dataclass(value):
        return canonicalize(asdict(value))
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise ContractError("mapping keys must be strings")
        return {k: canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value, (tuple, list)):
        return [canonicalize(v) for v in value]
    raise ContractError(f"unsupported canonical type: {type(value).__name__}")


def fingerprint(value: Any) -> str:
    payload = json.dumps(
        canonicalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256(payload).hexdigest()
