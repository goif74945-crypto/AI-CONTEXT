from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EvidenceState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


class SignalKind(str, Enum):
    INFO = "INFO"
    PROGRESS = "PROGRESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DECISION_REQUIRED = "DECISION_REQUIRED"
    FREEZE = "FREEZE"
    SECURITY = "SECURITY"
    COMPLETION = "COMPLETION"


class Severity(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Salience(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Delivery(str, Enum):
    NOW = "NOW"
    BATCH = "BATCH"
    SILENT_LOG = "SILENT_LOG"


@dataclass(frozen=True)
class OperatorSignal:
    signal_id: str
    sequence: int
    component: str
    kind: SignalKind
    severity: Severity
    evidence: EvidenceState
    state: str
    message: str = ""
    requires_user: bool = False
    blocking: bool = False
    state_changed: bool = False
    evidence_changed: bool = False
    requires_ack: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "OperatorSignal":
        required = ("signal_id", "sequence", "component", "kind", "severity", "evidence", "state")
        missing = [key for key in required if key not in raw]
        if missing:
            raise ValueError(f"missing signal fields: {','.join(sorted(missing))}")
        signal_id = raw["signal_id"]
        component = raw["component"]
        state = raw["state"]
        message = raw.get("message", "")
        sequence = raw["sequence"]
        if not isinstance(signal_id, str) or not signal_id:
            raise ValueError("signal_id must be a non-empty string")
        if not isinstance(component, str) or not component:
            raise ValueError("component must be a non-empty string")
        if not isinstance(state, str) or not state:
            raise ValueError("state must be a non-empty string")
        if not isinstance(message, str):
            raise ValueError("message must be a string")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
            raise ValueError("sequence must be a non-negative integer")
        bool_fields: dict[str, bool] = {}
        for key in ("requires_user", "blocking", "state_changed", "evidence_changed", "requires_ack"):
            value = raw.get(key, False)
            if not isinstance(value, bool):
                raise ValueError(f"{key} must be boolean")
            bool_fields[key] = value
        try:
            kind = SignalKind(raw["kind"])
            severity = Severity(raw["severity"])
            evidence = EvidenceState(raw["evidence"])
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        return cls(
            signal_id=signal_id,
            sequence=sequence,
            component=component,
            kind=kind,
            severity=severity,
            evidence=evidence,
            state=state,
            message=message,
            **bool_fields,
        )

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "blocking": self.blocking,
            "component": self.component,
            "evidence": self.evidence.value,
            "evidence_changed": self.evidence_changed,
            "kind": self.kind.value,
            "message": self.message,
            "requires_ack": self.requires_ack,
            "requires_user": self.requires_user,
            "sequence": self.sequence,
            "severity": self.severity.value,
            "signal_id": self.signal_id,
            "state": self.state,
            "state_changed": self.state_changed,
        }
