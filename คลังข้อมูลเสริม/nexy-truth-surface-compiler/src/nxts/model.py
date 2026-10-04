from __future__ import annotations

from dataclasses import dataclass
from typing import Any

FACT_STATUSES = frozenset({"SOURCE_FACT", "REPO_FACT", "RUNTIME_FACT", "EXTERNAL_FACT"})
UNCERTAINTY_STATUSES = frozenset({"INFERENCE", "ASSUMPTION"})
BLOCKING_STATUSES = frozenset({"UNKNOWN", "CONFLICT", "NOT_VERIFIED"})
ALLOWED_STATUSES = FACT_STATUSES | UNCERTAINTY_STATUSES | BLOCKING_STATUSES
ALLOWED_MATERIALITY = frozenset({"MATERIAL", "NON_MATERIAL"})
ALLOWED_VISIBILITY = frozenset({"PUBLIC", "INTERNAL", "SENSITIVE"})

MAX_CLAIMS = 256
MAX_CLAIM_TEXT_CHARS = 8192
MAX_EVIDENCE_REFS_PER_CLAIM = 64
MAX_EVIDENCE_REF_CHARS = 512


@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: str
    text: str
    status: str
    materiality: str
    visibility: str
    evidence_refs: tuple[str, ...]

    @staticmethod
    def from_mapping(raw: dict[str, Any]) -> "Claim":
        claim_id = raw.get("id")
        text = raw.get("text")
        status = raw.get("status")
        materiality = raw.get("materiality", "MATERIAL")
        visibility = raw.get("visibility", "PUBLIC")
        evidence_refs = raw.get("evidence_refs", [])

        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValueError("claim.id must be a non-empty string")
        if len(claim_id) > 256:
            raise ValueError("claim.id exceeds 256 characters")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"claim {claim_id!r}: text must be a non-empty string")
        if len(text) > MAX_CLAIM_TEXT_CHARS:
            raise ValueError(f"claim {claim_id!r}: text exceeds {MAX_CLAIM_TEXT_CHARS} characters")
        if not isinstance(status, str):
            raise ValueError(f"claim {claim_id!r}: status must be a string")
        if len(status) > 64:
            raise ValueError(f"claim {claim_id!r}: status exceeds 64 characters")
        if materiality not in ALLOWED_MATERIALITY:
            raise ValueError(f"claim {claim_id!r}: invalid materiality {materiality!r}")
        if visibility not in ALLOWED_VISIBILITY:
            raise ValueError(f"claim {claim_id!r}: invalid visibility {visibility!r}")
        if not isinstance(evidence_refs, list) or any(not isinstance(x, str) or not x.strip() for x in evidence_refs):
            raise ValueError(f"claim {claim_id!r}: evidence_refs must be a list of non-empty strings")
        if len(evidence_refs) > MAX_EVIDENCE_REFS_PER_CLAIM:
            raise ValueError(f"claim {claim_id!r}: too many evidence_refs")
        if any(len(x) > MAX_EVIDENCE_REF_CHARS for x in evidence_refs):
            raise ValueError(f"claim {claim_id!r}: evidence_ref exceeds {MAX_EVIDENCE_REF_CHARS} characters")

        return Claim(
            claim_id=claim_id.strip(),
            text=text.strip(),
            status=status.strip(),
            materiality=materiality,
            visibility=visibility,
            evidence_refs=tuple(sorted(set(x.strip() for x in evidence_refs))),
        )
