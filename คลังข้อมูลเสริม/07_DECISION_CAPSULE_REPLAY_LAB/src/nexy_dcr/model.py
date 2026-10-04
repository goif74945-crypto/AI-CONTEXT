from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable

from .canonical import ZERO_HASH, sha256_hex, validate_sha256
from .errors import SchemaError

SCHEMA_VERSION = "nexy-dcr/0.1"
PROPOSAL_STATUS = "AI_PROPOSAL_NOT_CANONICAL_NEXY_REQUIREMENT"


class EventKind(str, Enum):
    REQUEST = "REQUEST"
    CONTEXT_SELECTED = "CONTEXT_SELECTED"
    AUTHORITY_RESOLVED = "AUTHORITY_RESOLVED"
    DECISION = "DECISION"
    TOOL_INTENT = "TOOL_INTENT"
    TOOL_RESULT = "TOOL_RESULT"
    VERIFICATION = "VERIFICATION"
    FINAL = "FINAL"


class TerminalState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    FREEZE = "FREEZE"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"


@dataclass(frozen=True, slots=True)
class AuthorityRef:
    path: str
    sha: str
    role: str
    rank: int

    def __post_init__(self) -> None:
        if not self.path.strip():
            raise SchemaError("authority path cannot be empty")
        if not self.role.strip():
            raise SchemaError("authority role cannot be empty")
        if self.rank < 0:
            raise SchemaError("authority rank must be >= 0")
        validate_sha256(self.sha, field_name="authority sha")

    def to_dict(self) -> dict[str, Any]:
        return {"path": self.path, "sha": self.sha, "role": self.role, "rank": self.rank}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "AuthorityRef":
        required = {"path", "sha", "role", "rank"}
        missing = required - value.keys()
        if missing:
            raise SchemaError(f"authority ref missing fields: {sorted(missing)}")
        return cls(
            path=str(value["path"]),
            sha=str(value["sha"]),
            role=str(value["role"]),
            rank=int(value["rank"]),
        )


def normalize_authority_refs(refs: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    refs_tuple = tuple(refs)
    identities = [(r.path, r.sha, r.role, r.rank) for r in refs_tuple]
    if len(identities) != len(set(identities)):
        raise SchemaError("duplicate authority references are not allowed")
    return tuple(sorted(refs_tuple, key=lambda r: (r.rank, r.path, r.role, r.sha)))


def authority_fingerprint(refs: Iterable[AuthorityRef]) -> str:
    normalized = normalize_authority_refs(refs)
    return sha256_hex([r.to_dict() for r in normalized])


@dataclass(frozen=True, slots=True)
class Event:
    sequence: int
    kind: EventKind
    payload: dict[str, Any]
    prev_hash: str
    event_hash: str

    def __post_init__(self) -> None:
        if self.sequence < 0:
            raise SchemaError("event sequence must be >= 0")
        validate_sha256(self.prev_hash, field_name="prev_hash")
        validate_sha256(self.event_hash, field_name="event_hash")
        if not isinstance(self.payload, dict):
            raise SchemaError("event payload must be an object")

    @staticmethod
    def hash_material(
        *, sequence: int, kind: EventKind | str, payload: dict[str, Any], prev_hash: str
    ) -> dict[str, Any]:
        kind_value = EventKind(kind).value
        return {
            "sequence": sequence,
            "kind": kind_value,
            "payload": payload,
            "prev_hash": prev_hash,
        }

    @classmethod
    def create(
        cls,
        *,
        sequence: int,
        kind: EventKind | str,
        payload: dict[str, Any],
        prev_hash: str = ZERO_HASH,
    ) -> "Event":
        kind_enum = EventKind(kind)
        material = cls.hash_material(
            sequence=sequence,
            kind=kind_enum,
            payload=payload,
            prev_hash=prev_hash,
        )
        return cls(
            sequence=sequence,
            kind=kind_enum,
            payload=payload,
            prev_hash=prev_hash,
            event_hash=sha256_hex(material),
        )

    def recompute_hash(self) -> str:
        return sha256_hex(
            self.hash_material(
                sequence=self.sequence,
                kind=self.kind,
                payload=self.payload,
                prev_hash=self.prev_hash,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "kind": self.kind.value,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "event_hash": self.event_hash,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Event":
        required = {"sequence", "kind", "payload", "prev_hash", "event_hash"}
        missing = required - value.keys()
        if missing:
            raise SchemaError(f"event missing fields: {sorted(missing)}")
        try:
            kind = EventKind(str(value["kind"]))
        except ValueError as exc:
            raise SchemaError(f"unknown event kind: {value.get('kind')}") from exc
        return cls(
            sequence=int(value["sequence"]),
            kind=kind,
            payload=dict(value["payload"]),
            prev_hash=str(value["prev_hash"]),
            event_hash=str(value["event_hash"]),
        )


@dataclass(frozen=True, slots=True)
class Capsule:
    project_target: str
    authority_refs: tuple[AuthorityRef, ...]
    authority_fingerprint: str
    events: tuple[Event, ...]
    terminal_state: TerminalState
    schema_version: str = SCHEMA_VERSION
    proposal_status: str = PROPOSAL_STATUS

    def __post_init__(self) -> None:
        if not self.project_target.strip():
            raise SchemaError("project_target cannot be empty")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaError(
                f"unsupported schema_version: {self.schema_version!r}; expected {SCHEMA_VERSION!r}"
            )
        if self.proposal_status != PROPOSAL_STATUS:
            raise SchemaError("proposal_status cannot be promoted or rewritten in v0.1")
        validate_sha256(self.authority_fingerprint, field_name="authority_fingerprint")

    @property
    def capsule_id(self) -> str:
        return sha256_hex(
            {
                "schema_version": self.schema_version,
                "proposal_status": self.proposal_status,
                "project_target": self.project_target,
                "authority_fingerprint": self.authority_fingerprint,
                "event_hashes": [event.event_hash for event in self.events],
                "terminal_state": self.terminal_state.value,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        normalized_refs = normalize_authority_refs(self.authority_refs)
        return {
            "schema_version": self.schema_version,
            "proposal_status": self.proposal_status,
            "project_target": self.project_target,
            "authority_refs": [ref.to_dict() for ref in normalized_refs],
            "authority_fingerprint": self.authority_fingerprint,
            "events": [event.to_dict() for event in self.events],
            "terminal_state": self.terminal_state.value,
            "capsule_id": self.capsule_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Capsule":
        required = {
            "schema_version",
            "proposal_status",
            "project_target",
            "authority_refs",
            "authority_fingerprint",
            "events",
            "terminal_state",
        }
        missing = required - value.keys()
        if missing:
            raise SchemaError(f"capsule missing fields: {sorted(missing)}")
        refs = normalize_authority_refs(
            AuthorityRef.from_dict(item) for item in list(value["authority_refs"])
        )
        events = tuple(Event.from_dict(item) for item in list(value["events"]))
        try:
            terminal = TerminalState(str(value["terminal_state"]))
        except ValueError as exc:
            raise SchemaError(f"unknown terminal state: {value.get('terminal_state')}") from exc
        capsule = cls(
            schema_version=str(value["schema_version"]),
            proposal_status=str(value["proposal_status"]),
            project_target=str(value["project_target"]),
            authority_refs=refs,
            authority_fingerprint=str(value["authority_fingerprint"]),
            events=events,
            terminal_state=terminal,
        )
        provided_id = value.get("capsule_id")
        if provided_id is not None and str(provided_id) != capsule.capsule_id:
            raise SchemaError("capsule_id does not match capsule contents")
        return capsule
