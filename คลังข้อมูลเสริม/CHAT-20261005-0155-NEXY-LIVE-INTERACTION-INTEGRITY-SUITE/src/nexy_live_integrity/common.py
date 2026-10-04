from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Mapping, Sequence


class GateStatus(str, Enum):
    PASS = "PASS"
    FREEZE = "FREEZE"
    REJECT = "REJECT"


@dataclass(frozen=True, slots=True)
class GateDecision:
    status: GateStatus
    code: str
    detail: str
    fingerprint: str

    @property
    def allowed(self) -> bool:
        return self.status is GateStatus.PASS


def _to_primitive(value: Any) -> Any:
    if is_dataclass(value):
        return {k: _to_primitive(v) for k, v in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(k): _to_primitive(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_to_primitive(v) for v in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    raise TypeError(f"Unsupported canonical value: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        _to_primitive(value),
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def require_nonempty(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def require_digest(name: str, value: str) -> str:
    value = require_nonempty(name, value).lower()
    if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError(f"{name} must be a lowercase/uppercase SHA-256 hex digest")
    return value


def normalized_text(value: str) -> str:
    value = require_nonempty("text", value)
    return " ".join(value.split())


def normalized_string_tuple(values: Sequence[str], *, name: str) -> tuple[str, ...]:
    out = tuple(require_nonempty(name, v) for v in values)
    if len(set(out)) != len(out):
        raise ValueError(f"{name} contains duplicate values")
    return out
