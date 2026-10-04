from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Iterable

from .q64 import Q64


class WorkStatus(str, Enum):
    WIP = "WIP"
    READY = "READY"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class VoteRound(str, Enum):
    KEEP = "KEEP"
    CUT = "CUT"


class Disposition(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class EvidenceKind(str, Enum):
    SPEC = "SPEC"
    CODE = "CODE"
    AI_CONTEXT = "AI_CONTEXT"
    TEST = "TEST"
    SEMANTIC_DUPLICATE = "SEMANTIC_DUPLICATE"
    DEPENDENCY = "DEPENDENCY"
    SECURITY = "SECURITY"


class EventKind(str, Enum):
    SET_STATUS = "SET_STATUS"
    ATTACH_EVIDENCE = "ATTACH_EVIDENCE"
    KEEP = "KEEP"
    CUT = "CUT"
    DEFER = "DEFER"
    REVISE_VOTE = "REVISE_VOTE"
    CLAIM_DUPLICATE = "CLAIM_DUPLICATE"
    ATTEMPT_PROMOTION = "ATTEMPT_PROMOTION"
    ATTEMPT_CORE_MUTATION = "ATTEMPT_CORE_MUTATION"
    ATTEMPT_CANON_OVERRIDE = "ATTEMPT_CANON_OVERRIDE"


@dataclass(frozen=True, slots=True, order=True)
class EvidenceRef:
    kind: EvidenceKind
    locator: str
    digest: str
    commit_sha: str = ""
    semantic_target: str = ""
    semantic_witness: str = ""

    def validate(self) -> None:
        if not self.locator.strip():
            raise ValueError("EVIDENCE_LOCATOR_REQUIRED")
        if len(self.digest) != 64 or any(c not in "0123456789abcdef" for c in self.digest):
            raise ValueError("EVIDENCE_DIGEST_INVALID")
        if self.commit_sha and (
            len(self.commit_sha) != 40
            or any(c not in "0123456789abcdef" for c in self.commit_sha)
        ):
            raise ValueError("EVIDENCE_COMMIT_INVALID")
        if self.kind is EvidenceKind.SEMANTIC_DUPLICATE:
            if not self.semantic_target.strip() or not self.semantic_witness.strip():
                raise ValueError("SEMANTIC_DUPLICATE_WITNESS_REQUIRED")


@dataclass(frozen=True, slots=True)
class VoteRecord:
    vote_id: str
    chat_id: str
    round: VoteRound
    timestamp: str
    spec_id: str
    spec_hash: str
    nexy_repo: str
    nexy_branch: str
    nexy_commit_sha: str
    ai_context_commit_sha: str
    candidate_id: str
    candidate_path: str
    status_before: WorkStatus
    verdict: str
    spec_evidence: tuple[str, ...]
    code_evidence: tuple[str, ...]
    ai_context_evidence: tuple[str, ...]
    test_evidence: tuple[str, ...]
    architecture_fit_q64: Q64
    canon_compatibility_q64: Q64
    novelty_q64: Q64
    overlap_q64: Q64
    implementation_value_q64: Q64
    verification_value_q64: Q64
    security_impact_q64: Q64
    determinism_impact_q64: Q64
    maintenance_cost_q64: Q64
    conflicts: tuple[str, ...]
    duplicates: tuple[str, ...]
    dependencies: tuple[str, ...]
    fact: tuple[str, ...]
    assumption: tuple[str, ...]
    unknown: tuple[str, ...]
    reason: str
    counterargument: str
    final_justification: str
    disposition: Disposition


@dataclass(frozen=True, slots=True)
class VoteRevision:
    revision_id: str
    vote_id: str
    appended_evidence: tuple[str, ...]
    note: str


@dataclass(frozen=True, slots=True)
class CourtPins:
    spec_id: str
    spec_hash: str
    nexy_repo: str
    nexy_branch: str
    nexy_commit_sha: str
    ai_context_commit_sha: str

    def validate(self) -> None:
        if not self.spec_id.strip():
            raise ValueError("SPEC_ID_REQUIRED")
        if len(self.spec_hash) != 64 or any(c not in "0123456789abcdef" for c in self.spec_hash):
            raise ValueError("SPEC_HASH_INVALID")
        if not self.nexy_repo.strip() or not self.nexy_branch.strip():
            raise ValueError("NEXY_PIN_REQUIRED")
        for value, code in (
            (self.nexy_commit_sha, "NEXY_COMMIT_INVALID"),
            (self.ai_context_commit_sha, "AI_CONTEXT_COMMIT_INVALID"),
        ):
            if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
                raise ValueError(code)


@dataclass(frozen=True, slots=True)
class CourtState:
    chat_id: str
    candidate_id: str
    candidate_path: str
    pins: CourtPins
    status: WorkStatus = WorkStatus.WIP
    evidence: tuple[EvidenceRef, ...] = ()
    votes: tuple[VoteRecord, ...] = ()
    revisions: tuple[VoteRevision, ...] = ()
    defer_count: int = 0
    disposition: Disposition = Disposition.ACTIVE
    promoted: bool = False
    external_core_mutations: int = 0
    canon_overrides: int = 0

    def with_evidence(self, evidence: Iterable[EvidenceRef]) -> "CourtState":
        unique = {e: e for e in (*self.evidence, *tuple(evidence))}
        ordered = tuple(sorted(unique.values()))
        return replace(self, evidence=ordered)

    def count_round(self, round_: VoteRound) -> int:
        return sum(1 for vote in self.votes if vote.round is round_)

    def evidence_of(self, kind: EvidenceKind) -> tuple[EvidenceRef, ...]:
        return tuple(e for e in self.evidence if e.kind is kind)

    def required_evidence_complete(self) -> bool:
        required = {EvidenceKind.SPEC, EvidenceKind.CODE, EvidenceKind.AI_CONTEXT, EvidenceKind.TEST}
        return required.issubset({e.kind for e in self.evidence})

    def evidence_coverage_q64(self) -> Q64:
        required = {EvidenceKind.SPEC, EvidenceKind.CODE, EvidenceKind.AI_CONTEXT, EvidenceKind.TEST}
        have = len(required.intersection({e.kind for e in self.evidence}))
        return Q64.from_ratio(have, len(required))


@dataclass(frozen=True, slots=True)
class Event:
    kind: EventKind
    status: WorkStatus | None = None
    evidence: EvidenceRef | None = None
    vote_id: str = ""
    timestamp: str = ""
    reason: str = ""
    counterargument: str = ""
    final_justification: str = ""
    target_vote_id: str = ""
    revision_id: str = ""
    note: str = ""
    semantic_target: str = ""
    semantic_witness: str = ""
    requested_disposition: Disposition = Disposition.ARCHIVED


@dataclass(frozen=True, slots=True)
class TransitionResult:
    state: CourtState
    accepted: bool
    code: str
