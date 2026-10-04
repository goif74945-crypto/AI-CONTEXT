from __future__ import annotations

import hashlib
import json
import math
from dataclasses import fields, is_dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping


HASH_DOMAIN = b"nexy-mvk-canonical-v1\0"


class CanonicalizationError(TypeError):
    pass


def to_canonical_data(value: Any) -> Any:
    """Convert supported Python values into stable JSON-compatible data.

    The function intentionally rejects unknown objects instead of using repr(),
    because repr() can contain memory addresses or nondeterministic state.
    """

    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalizationError("non-finite floats are not canonical")
        return value
    if isinstance(value, Enum):
        return to_canonical_data(value.value)
    if is_dataclass(value) and not isinstance(value, type):
        return to_canonical_data({field.name: getattr(value, field.name) for field in fields(value)})
    if isinstance(value, MappingProxyType):
        return to_canonical_data(dict(value))
    if isinstance(value, Mapping):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("mapping keys must be strings")
            out[key] = to_canonical_data(item)
        return {key: out[key] for key in sorted(out)}
    if isinstance(value, (tuple, list)):
        return [to_canonical_data(item) for item in value]
    if isinstance(value, (set, frozenset)):
        normalized = [to_canonical_data(item) for item in value]
        try:
            return sorted(normalized, key=lambda x: canonical_json(x))
        except TypeError as exc:
            raise CanonicalizationError("set contains non-canonical values") from exc
    raise CanonicalizationError(f"unsupported canonicalization type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        to_canonical_data(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def stable_hash(value: Any) -> str:
    payload = HASH_DOMAIN + canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
