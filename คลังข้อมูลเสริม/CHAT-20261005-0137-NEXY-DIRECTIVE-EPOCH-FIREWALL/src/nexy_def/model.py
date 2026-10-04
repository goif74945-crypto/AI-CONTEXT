from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .canonical import canonical_json, sha256_hex


class DirectiveOperation(str, Enum):
    NEW = "NEW"
    REPLACE = "REPLACE"
    NARROW = "NARROW"
    REVOKE = "REVOKE"


class EngineStatus(str, Enum):
    EMPTY = "EMPTY"
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    FROZEN = "FROZEN"


class ActionKind(str, Enum):
    READ = "READ"
    REVERSIBLE_WRITE = "REVERSIBLE_WRITE"
    IRREVERSIBLE_WRITE = "IRREVERSIBLE_WRITE"


class DecisionStatus(str, Enum):
    ALLOW = "ALLOW"
    REJECT = "REJECT"
    FREEZE = "FREEZE"


class JournalKind(str, Enum):
    DIRECTIVE = "DIRECTIVE"
    COMMIT = "COMMIT"
    RECOVERY = "RECOVERY"


@dataclass(frozen=True)
class DirectiveEvent:
    event_id: str
    directive_id: str
    operation: DirectiveOperation
    expected_epoch: int | None = None
    allowed_actions: tuple[ActionKind, ...] = ()
    constraints: Mapping[str, Any] = field(default_factory=dict)
    note: str | None = None

    def normalized(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "directive_id": self.directive_id,
            "operation": self.operation.value,
            "expected_epoch": self.expected_epoch,
            "allowed_actions": sorted(a.value for a in self.allowed_actions),
            "constraints": dict(self.constraints),
            "note": self.note,
        }

    @classmethod
    def from_normalized(cls, data: Mapping[str, Any]) -> "DirectiveEvent":
        return cls(
            event_id=str(data["event_id"]),
            directive_id=str(data["directive_id"]),
            operation=DirectiveOperation(str(data["operation"])),
            expected_epoch=data.get("expected_epoch"),
            allowed_actions=tuple(ActionKind(str(x)) for x in data.get("allowed_actions", [])),
            constraints=dict(data.get("constraints", {})),
            note=data.get("note"),
        )

    @property
    def digest(self) -> str:
        return sha256_hex(self.normalized())


@dataclass(frozen=True)
class DirectiveState:
    epoch: int = 0
    status: EngineStatus = EngineStatus.EMPTY
    active_directive_id: str | None = None
    directive_hash: str = ""
    lineage_hash: str = "0" * 64
    allowed_actions: tuple[ActionKind, ...] = ()
    constraints: Mapping[str, Any] = field(default_factory=dict)
    freeze_reason: str | None = None

    def normalized(self) -> dict[str, Any]:
        return {
            "epoch": self.epoch,
            "status": self.status.value,
            "active_directive_id": self.active_directive_id,
            "directive_hash": self.directive_hash,
            "lineage_hash": self.lineage_hash,
            "allowed_actions": sorted(a.value for a in self.allowed_actions),
            "constraints": dict(self.constraints),
            "freeze_reason": self.freeze_reason,
        }

    @property
    def state_hash(self) -> str:
        return sha256_hex(self.normalized())


@dataclass(frozen=True)
class PreparedAction:
    action_id: str
    kind: ActionKind
    payload: Mapping[str, Any]
    action_digest: str
    prepared_epoch: int
    directive_hash: str
    lineage_hash: str
    approval_binding: str | None = None

    @staticmethod
    def compute_digest(action_id: str, kind: ActionKind, payload: Mapping[str, Any]) -> str:
        return sha256_hex(
            {
                "domain": "NEXY_DEF_ACTION_V1",
                "action_id": action_id,
                "kind": kind.value,
                "payload": dict(payload),
            }
        )

    def normalized(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "kind": self.kind.value,
            "payload": dict(self.payload),
            "action_digest": self.action_digest,
            "prepared_epoch": self.prepared_epoch,
            "directive_hash": self.directive_hash,
            "lineage_hash": self.lineage_hash,
            "approval_binding": self.approval_binding,
        }

    @classmethod
    def from_normalized(cls, data: Mapping[str, Any]) -> "PreparedAction":
        return cls(
            action_id=str(data["action_id"]),
            kind=ActionKind(str(data["kind"])),
            payload=dict(data.get("payload", {})),
            action_digest=str(data["action_digest"]),
            prepared_epoch=int(data["prepared_epoch"]),
            directive_hash=str(data["directive_hash"]),
            lineage_hash=str(data["lineage_hash"]),
            approval_binding=data.get("approval_binding"),
        )


@dataclass(frozen=True)
class CommitDecision:
    status: DecisionStatus
    code: str
    reason: str
    epoch: int
    state_hash: str

    @property
    def allowed(self) -> bool:
        return self.status is DecisionStatus.ALLOW


@dataclass(frozen=True)
class AppliedEvent:
    event: DirectiveEvent
    event_hash: str
    resulting_state_hash: str


@dataclass(frozen=True)
class JournalRecord:
    index: int
    kind: JournalKind
    payload: Mapping[str, Any]
    outcome_code: str
    resulting_state_hash: str
    previous_record_hash: str
    record_hash: str

    def hash_material(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "kind": self.kind.value,
            "payload": dict(self.payload),
            "outcome_code": self.outcome_code,
            "resulting_state_hash": self.resulting_state_hash,
            "previous_record_hash": self.previous_record_hash,
        }


class ProtocolError(ValueError):
    pass


def ensure_nonempty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ProtocolError(f"{field_name} must be a non-empty string")


def validate_event_shape(event: DirectiveEvent) -> None:
    ensure_nonempty(event.event_id, "event_id")
    ensure_nonempty(event.directive_id, "directive_id")
    if event.expected_epoch is not None and event.expected_epoch < 0:
        raise ProtocolError("expected_epoch must be >= 0")
    canonical_json(event.normalized())
