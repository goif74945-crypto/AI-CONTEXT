from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Mapping, Sequence


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    FREEZE = "FREEZE"
    REVIEW = "REVIEW"


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: int
    message: str
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.severity <= 100:
            raise ValueError("severity must be in [0, 100]")
        if not self.code.strip():
            raise ValueError("finding code must not be empty")
        if not self.message.strip():
            raise ValueError("finding message must not be empty")


@dataclass(frozen=True, slots=True)
class Decision:
    engine: str
    verdict: Verdict
    score: int
    findings: tuple[Finding, ...]
    payload: Mapping[str, Any]
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("score must be in [0, 100]")
        if not self.engine.strip():
            raise ValueError("engine must not be empty")

    def canonical_dict(self) -> dict[str, Any]:
        return _normalize(asdict(self))

    def canonical_json(self) -> str:
        return json.dumps(
            self.canonical_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )

    def fingerprint(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


def _normalize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, Mapping):
        return {str(k): _normalize(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    if isinstance(value, set):
        return sorted(_normalize(v) for v in value)
    return value


def stable_tuple(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(sorted({v.strip() for v in values if v and v.strip()}))
