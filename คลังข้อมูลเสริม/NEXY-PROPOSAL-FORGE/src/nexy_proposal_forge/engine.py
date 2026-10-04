from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .canon import sha256_fingerprint
from .models import Proposal
from .overlap import OverlapResult, rank_overlaps

Recommendation = Literal[
    "PROMOTE_FOR_HUMAN_REVIEW",
    "MERGE_WITH_EXISTING",
    "NEEDS_EVIDENCE",
    "REJECT_DUPLICATE",
    "FREEZE_CONFLICT",
]


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    proposal_id: str
    fingerprint_sha256: str
    recommendation: Recommendation
    advisory_only: bool
    authoritative: bool
    deterministic: bool
    reasons: tuple[str, ...]
    evidence_gap_count: int
    top_overlaps: tuple[OverlapResult, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "proposal_id": self.proposal_id,
            "fingerprint_sha256": self.fingerprint_sha256,
            "recommendation": self.recommendation,
            "advisory_only": self.advisory_only,
            "authoritative": self.authoritative,
            "deterministic": self.deterministic,
            "reasons": list(self.reasons),
            "evidence_gap_count": self.evidence_gap_count,
            "top_overlaps": [item.to_dict() for item in self.top_overlaps],
        }


def _evidence_gap_count(proposal: Proposal) -> int:
    gaps = 0
    factual = {"SOURCE_FACT", "REPO_FACT", "RUNTIME_FACT", "EXTERNAL_FACT"}
    if len(proposal.evidence) < 2:
        gaps += 2 - len(proposal.evidence)
    if not any(item.role == "AUTHORITY" and item.truth_class in factual for item in proposal.evidence):
        gaps += 1
    if not any(item.role == "DUPLICATE_CHECK" for item in proposal.evidence):
        gaps += 1
    if proposal.assumptions and not any(
        item.role == "ASSUMPTION" and item.truth_class == "ASSUMPTION"
        for item in proposal.evidence
    ):
        gaps += 1
    return gaps


def evaluate_proposal(candidate: Proposal, catalog: tuple[Proposal, ...] = ()) -> EvaluationResult:
    """Evaluate one proposal without granting implementation authority."""

    fingerprint = sha256_fingerprint(candidate.to_dict())
    overlaps = rank_overlaps(candidate, catalog)
    top_overlaps = overlaps[:5]
    top_score = top_overlaps[0].score_bp if top_overlaps else 0
    gaps = _evidence_gap_count(candidate)
    reasons: list[str] = []

    identity_match = next((item for item in catalog if item.proposal_id == candidate.proposal_id), None)
    identity_same = identity_match is not None and sha256_fingerprint(identity_match.to_dict()) == fingerprint

    if candidate.authority_conflicts:
        recommendation: Recommendation = "FREEZE_CONFLICT"
        reasons.append("proposal declares unresolved authority conflict(s)")
    elif identity_match is not None and not identity_same:
        recommendation = "FREEZE_CONFLICT"
        reasons.append("proposal_id collides with an existing catalog entry but content differs")
    elif identity_same:
        recommendation = "REJECT_DUPLICATE"
        reasons.append("proposal_id and canonical content exactly match an existing catalog entry")
    elif top_score >= 9_500:
        recommendation = "REJECT_DUPLICATE"
        reasons.append(f"duplicate threshold reached: overlap={top_score}bp >= 9500bp")
    elif top_score >= 7_000:
        recommendation = "MERGE_WITH_EXISTING"
        reasons.append(f"near-duplicate threshold reached: overlap={top_score}bp >= 7000bp")
    elif gaps > 0:
        recommendation = "NEEDS_EVIDENCE"
        reasons.append(f"evidence contract has {gaps} unresolved gap(s)")
    else:
        recommendation = "PROMOTE_FOR_HUMAN_REVIEW"
        reasons.append("candidate is sufficiently distinct and meets the proposal evidence contract")

    reasons.append("result is advisory only; it cannot create or modify NEXY requirements")
    reasons.append("human/project authority must explicitly approve any promotion or implementation")

    return EvaluationResult(
        proposal_id=candidate.proposal_id,
        fingerprint_sha256=fingerprint,
        recommendation=recommendation,
        advisory_only=True,
        authoritative=False,
        deterministic=True,
        reasons=tuple(reasons),
        evidence_gap_count=gaps,
        top_overlaps=top_overlaps,
    )
