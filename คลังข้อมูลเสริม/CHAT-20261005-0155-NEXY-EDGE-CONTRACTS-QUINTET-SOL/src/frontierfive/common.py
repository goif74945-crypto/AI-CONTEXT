from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return sha256(canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class Verdict:
    status: str
    reasons: tuple[str, ...]
    payload: dict[str, Any]

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "payload": self.payload,
            "reasons": list(self.reasons),
            "status": self.status,
        }

    @property
    def fingerprint(self) -> str:
        return digest(self.canonical_dict())


def freeze(*reasons: str, payload: dict[str, Any] | None = None) -> Verdict:
    return Verdict("FREEZE", tuple(sorted(set(reasons))), payload or {})


def allow(payload: dict[str, Any] | None = None) -> Verdict:
    return Verdict("ALLOW", tuple(), payload or {})
