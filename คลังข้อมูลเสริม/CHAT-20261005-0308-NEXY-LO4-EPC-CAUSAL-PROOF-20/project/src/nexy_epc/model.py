"""Immutable data model for the Lo4 EPC evidence kernel."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Sequence

from .q64 import Q64


class GateStatus(str, Enum):
    PASS = "PASS"
    DEFER = "DEFER"
    FREEZE = "FREEZE"


class ProposalStatus(str, Enum):
    WIP = "WIP"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class VoteRound(str, Enum):
    KEEP = "KEEP"
    CUT = "CUT"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    evidence_id: str
    kind: str
    locator: str
    sha256: str
    verified: bool
    age_ticks: int = 0

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id required")
        if not self.kind.strip():
            raise ValueError("evidence kind required")
        if not self.locator.strip():
            raise ValueError("evidence locator required")
        if len(self.sha256) != 64 or any(c not in "0123456789abcdef" for c in self.sha256):
            raise ValueError("evidence sha256 must be lowercase hex64")
        if type(self.verified) is not bool:
            raise TypeError("verified must be bool")
        if type(self.age_ticks) is not int or self.age_ticks < 0:
            raise ValueError("age_ticks must be nonnegative int")


@dataclass(frozen=True, slots=True)
class ProposalSnapshot:
    candidate_id: str
    candidate_path: str
    status: ProposalStatus
    spec_id: str
    spec_hash: str
    nexy_repo: str
    nexy_branch: str
    nexy_commit_sha: str
    ai_context_commit_sha: str
    facts: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    duplicates: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    evidence: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        for name in ("candidate_id", "candidate_path", "spec_id", "spec_hash", "nexy_repo", "nexy_branch", "nexy_commit_sha", "ai_context_commit_sha"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} required")
        for name in ("spec_hash", "nexy_commit_sha", "ai_context_commit_sha"):
            value = getattr(self, name)
            if len(value) != 40 and name != "spec_hash":
                raise ValueError(f"{name} must be git SHA-1 hex40")
            if name == "spec_hash" and len(value) != 64:
                raise ValueError("spec_hash must be SHA-256 hex64")
            if any(c not in "0123456789abcdef" for c in value):
                raise ValueError(f"{name} must be lowercase hex")


@dataclass(frozen=True, slots=True)
class SemanticFacet:
    key: str
    weight: Q64

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("facet key required")
        if self.weight.raw < 0:
            raise ValueError("facet weight must be nonnegative")


@dataclass(frozen=True, slots=True)
class SemanticProfile:
    candidate_id: str
    facets: tuple[SemanticFacet, ...]

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("candidate_id required")
        keys = [f.key for f in self.facets]
        if len(set(keys)) != len(keys):
            raise ValueError("duplicate semantic facet key")


@dataclass(frozen=True, slots=True)
class GateResult:
    system_id: str
    status: GateStatus
    score: Q64
    reason_codes: tuple[str, ...]
    evidence_ids: tuple[str, ...] = ()
    details: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.system_id.strip():
            raise ValueError("system_id required")
        if not self.score.in_unit_interval():
            raise ValueError("GateResult score must be in [0,1]")
        if not self.reason_codes:
            raise ValueError("reason_codes required")
        frozen_details = MappingProxyType(dict(sorted(self.details.items())))
        object.__setattr__(self, "details", frozen_details)


@dataclass(frozen=True, slots=True)
class VoteRecord:
    vote_id: str
    chat_id: str
    round: VoteRound
    timestamp: str
    candidate_id: str
    candidate_path: str
    verdict: str
    evidence_digest: str

    def __post_init__(self) -> None:
        for name in ("vote_id", "chat_id", "timestamp", "candidate_id", "candidate_path", "verdict"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} required")
        if len(self.evidence_digest) != 64 or any(c not in "0123456789abcdef" for c in self.evidence_digest):
            raise ValueError("evidence_digest must be lowercase hex64")


@dataclass(frozen=True, slots=True)
class CourtDossier:
    candidate_id: str
    status: GateStatus
    composite_score: Q64
    hard_failures: tuple[str, ...]
    deferred: tuple[str, ...]
    passed: tuple[str, ...]
    canonical_digest: str
    recommendation: str


def frozen_tuple(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(values)
