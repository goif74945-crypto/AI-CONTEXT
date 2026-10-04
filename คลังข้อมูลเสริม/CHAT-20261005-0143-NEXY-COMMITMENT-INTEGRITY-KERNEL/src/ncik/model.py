from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class AuthorityState(str, Enum):
    RESOLVED = "RESOLVED"
    UNRESOLVED = "UNRESOLVED"
    CONFLICT = "CONFLICT"


class TemporalMode(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    SCHEDULED = "SCHEDULED"
    CONDITIONAL = "CONDITIONAL"
    RECURRING = "RECURRING"


class BindingType(str, Enum):
    INLINE_SESSION = "INLINE_SESSION"
    SCHEDULED_TASK = "SCHEDULED_TASK"
    CONDITION_WATCH = "CONDITION_WATCH"
    RECURRING_TASK = "RECURRING_TASK"


class EffectClass(str, Enum):
    READ_ONLY = "READ_ONLY"
    REVERSIBLE_WRITE = "REVERSIBLE_WRITE"
    EXTERNAL_SIDE_EFFECT = "EXTERNAL_SIDE_EFFECT"
    IRREVERSIBLE_WRITE = "IRREVERSIBLE_WRITE"


class EvidenceClass(str, Enum):
    E0_PRESENCE = "E0_PRESENCE"
    E1_STATIC = "E1_STATIC"
    E2_UNIT = "E2_UNIT"
    E3_INTEGRATION = "E3_INTEGRATION"
    E4_E2E = "E4_E2E"
    E5_RUNTIME = "E5_RUNTIME"
    E6_DEPLOYMENT = "E6_DEPLOYMENT"
    E7_PHYSICAL = "E7_PHYSICAL"


class Decision(str, Enum):
    ALLOW_COMMITMENT = "ALLOW_COMMITMENT"
    ASK_AUTHORITY = "ASK_AUTHORITY"
    FREEZE = "FREEZE"


class CommitmentState(str, Enum):
    DRAFT = "DRAFT"
    ACCEPTED = "ACCEPTED"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    FULFILLED = "FULFILLED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class ExecutionBinding:
    binding_type: BindingType
    binding_ref: str
    durable: bool
    capability_proof_ref: str


@dataclass(frozen=True)
class CapabilityManifest:
    supported_bindings: frozenset[BindingType]
    supported_effects: frozenset[EffectClass]
    evidence_classes: frozenset[EvidenceClass]


@dataclass(frozen=True)
class Commitment:
    commitment_id: str
    revision: int
    issuer: str
    beneficiary: str
    objective: str
    deliverable: str
    scope: tuple[str, ...]
    protected_scope: tuple[str, ...]
    temporal_mode: TemporalMode
    effect: EffectClass
    authority_state: AuthorityState
    authority_refs: tuple[str, ...]
    required_evidence: tuple[EvidenceClass, ...]
    binding: ExecutionBinding
    trigger_spec: str | None = None
    deadline_spec: str | None = None
    supersedes_fingerprint: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Evaluation:
    decision: Decision
    reason_codes: tuple[str, ...]
    fingerprint: str


@dataclass(frozen=True)
class EvidenceBundle:
    target_fingerprint: str
    commitment_revision: int
    classes: frozenset[EvidenceClass]
    refs: tuple[str, ...]
    result: str


@dataclass(frozen=True)
class TransitionResult:
    previous: CommitmentState
    current: CommitmentState
    reason_code: str


@dataclass(frozen=True)
class LedgerEvent:
    sequence: int
    commitment_id: str
    revision: int
    event_type: str
    state: CommitmentState
    payload: Mapping[str, str]
    previous_hash: str
    event_hash: str


@dataclass(frozen=True)
class RevisionCheck:
    allowed: bool
    reason_codes: tuple[str, ...]
