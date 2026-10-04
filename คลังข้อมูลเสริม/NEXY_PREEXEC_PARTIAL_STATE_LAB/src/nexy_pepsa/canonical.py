from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


class CanonicalizationError(ValueError):
    pass


def _primitive(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise CanonicalizationError("floating-point values are forbidden in canonical PEPSA data")
    if isinstance(value, Enum):
        return _primitive(value.value)
    if is_dataclass(value):
        return _primitive(asdict(value))
    if isinstance(value, tuple):
        return [_primitive(item) for item in value]
    if isinstance(value, list):
        return [_primitive(item) for item in value]
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("canonical object keys must be strings")
            output[key] = _primitive(item)
        return output
    raise CanonicalizationError(f"unsupported canonical type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    primitive = _primitive(value)
    return json.dumps(
        primitive,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_hash(value: Any) -> str:
    payload = canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
