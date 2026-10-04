from __future__ import annotations

from dataclasses import asdict, is_dataclass
from decimal import Decimal
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any

from .rational import canonical_fraction


def _normalize(value: Any) -> Any:
    if isinstance(value, Fraction):
        return canonical_fraction(value)
    if isinstance(value, Decimal):
        return canonical_fraction(Fraction(value))
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, dict):
        return {str(key): _normalize(value[key]) for key in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, float):
        raise TypeError("binary float is forbidden in canonical numeric artifacts")
    raise TypeError(f"unsupported canonical type: {type(value).__name__}")


def canonical_dumps(value: Any) -> str:
    return json.dumps(_normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_bytes(value: Any) -> bytes:
    return canonical_dumps(value).encode("utf-8")


def digest(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def _diagnostic_normalize(value: Any) -> Any:
    """Normalize even invalid inputs for forensic identity without legitimizing them."""
    if isinstance(value, float):
        return {"$invalid_binary_float_hex": value.hex()}
    if isinstance(value, Fraction):
        return {"$fraction": canonical_fraction(value)}
    if isinstance(value, Decimal):
        if value.is_finite():
            return {"$decimal": canonical_fraction(Fraction(value))}
        return {"$invalid_decimal": str(value)}
    if is_dataclass(value):
        return _diagnostic_normalize(asdict(value))
    if isinstance(value, dict):
        pairs = []
        for key, item in value.items():
            pairs.append((str(key), _diagnostic_normalize(item)))
        return {key: item for key, item in sorted(pairs, key=lambda pair: pair[0])}
    if isinstance(value, (list, tuple)):
        return [_diagnostic_normalize(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    return {"$unsupported_type": f"{type(value).__module__}.{type(value).__qualname__}"}


def diagnostic_digest(value: Any) -> str:
    payload = json.dumps(_diagnostic_normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()
