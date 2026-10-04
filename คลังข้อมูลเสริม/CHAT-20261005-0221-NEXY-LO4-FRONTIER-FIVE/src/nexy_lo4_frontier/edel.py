from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .common import FrontierInputError, require_text, stable_hash


@dataclass(frozen=True, slots=True)
class ProofClaim:
    claim_id: str
    required_evidence_class: int
    criticality: int = 1
    subjects: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EvidenceArtifact:
    evidence_id: str
    claim_ids: tuple[str, ...]
    evidence_class: int
    subject_versions: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class ClaimDebt:
    claim_id: str
    status: str
    debt_points: int
    reasons: tuple[str, ...]
    usable_evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DebtReport:
    status: str
    total_debt_points: int
    directly_invalid_claims: tuple[str, ...]
    propagated_invalid_claims: tuple[str, ...]
    reverify_frontier: tuple[str, ...]
    claims: tuple[ClaimDebt, ...]
    fingerprint: str


def _eclass(value: int, field: str) -> int:
    if not isinstance(value, int) or not 0 <= value <= 7:
        raise FrontierInputError(f"{field}:EVIDENCE_CLASS_OUT_OF_RANGE")
    return value


def _canon_claim(c: ProofClaim) -> ProofClaim:
    cid = require_text(c.claim_id, "claim_id")
    if not isinstance(c.criticality, int) or not 1 <= c.criticality <= 100:
        raise FrontierInputError(f"{cid}:CRITICALITY_OUT_OF_RANGE")
    subjects = tuple(sorted({require_text(x, f"{cid}.subject") for x in c.subjects}))
    deps = tuple(sorted({require_text(x, f"{cid}.depends_on") for x in c.depends_on}))
    if cid in deps:
        raise FrontierInputError(f"{cid}:SELF_DEPENDENCY")
    return ProofClaim(cid, _eclass(c.required_evidence_class, cid), c.criticality, subjects, deps)


def _canon_evidence(e: EvidenceArtifact) -> EvidenceArtifact:
    eid = require_text(e.evidence_id, "evidence_id")
    claim_ids = tuple(sorted({require_text(x, f"{eid}.claim") for x in e.claim_ids}))
    if not claim_ids:
        raise FrontierInputError(f"{eid}:NO_CLAIMS")
    versions: dict[str, str] = {}
    for pair in e.subject_versions:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise FrontierInputError(f"{eid}:VERSION_NOT_PAIR")
        subject = require_text(pair[0], f"{eid}.subject")
        version = require_text(pair[1], f"{eid}.version")
        if subject in versions and versions[subject] != version:
            raise FrontierInputError(f"{eid}:DUPLICATE_SUBJECT_VERSION:{subject}")
        versions[subject] = version
    return EvidenceArtifact(eid, claim_ids, _eclass(e.evidence_class, eid), tuple(sorted(versions.items())))


def assess_evidence_debt(
    claims: Iterable[ProofClaim],
    evidence: Iterable[EvidenceArtifact],
    current_subject_versions: Mapping[str, str],
) -> DebtReport:
    cs = tuple(sorted((_canon_claim(c) for c in claims), key=lambda c: c.claim_id))
    es = tuple(sorted((_canon_evidence(e) for e in evidence), key=lambda e: e.evidence_id))
    if not cs:
        raise FrontierInputError("NO_CLAIMS")
    claim_map = {c.claim_id: c for c in cs}
    if len(claim_map) != len(cs):
        raise FrontierInputError("DUPLICATE_CLAIM_ID")
    evidence_ids = [e.evidence_id for e in es]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise FrontierInputError("DUPLICATE_EVIDENCE_ID")

    versions = {require_text(str(k), "current_subject"): require_text(v, f"version:{k}") for k, v in current_subject_versions.items()}
    unknown_deps = sorted({d for c in cs for d in c.depends_on if d not in claim_map})
    if unknown_deps:
        raise FrontierInputError("UNKNOWN_DEPENDENCY:" + ",".join(unknown_deps))

    visiting: set[str] = set()
    visited: set[str] = set()

    def check_cycle(cid: str) -> None:
        if cid in visited:
            return
        if cid in visiting:
            raise FrontierInputError(f"DEPENDENCY_CYCLE:{cid}")
        visiting.add(cid)
        for dep in claim_map[cid].depends_on:
            check_cycle(dep)
        visiting.remove(cid)
        visited.add(cid)

    for cid in sorted(claim_map):
        check_cycle(cid)

    evidence_by_claim: dict[str, list[EvidenceArtifact]] = {c.claim_id: [] for c in cs}
    for artifact in es:
        for cid in artifact.claim_ids:
            if cid in evidence_by_claim:
                evidence_by_claim[cid].append(artifact)

    direct_reasons: dict[str, tuple[str, ...]] = {}
    usable_by_claim: dict[str, tuple[str, ...]] = {}
    for claim in cs:
        usable: list[str] = []
        reasons: set[str] = set()
        candidates = evidence_by_claim[claim.claim_id]
        if not candidates:
            reasons.add("NO_EVIDENCE")
        for artifact in candidates:
            if artifact.evidence_class < claim.required_evidence_class:
                reasons.add(f"INSUFFICIENT_CLASS:{artifact.evidence_id}")
                continue
            bound = dict(artifact.subject_versions)
            stale_subjects = [s for s in claim.subjects if versions.get(s) != bound.get(s)]
            if stale_subjects:
                reasons.add(f"STALE:{artifact.evidence_id}:{'|'.join(sorted(stale_subjects))}")
                continue
            usable.append(artifact.evidence_id)
        usable_by_claim[claim.claim_id] = tuple(sorted(usable))
        if not usable:
            direct_reasons[claim.claim_id] = tuple(sorted(reasons or {"NO_USABLE_EVIDENCE"}))

    invalid: set[str] = set(direct_reasons)
    changed = True
    while changed:
        changed = False
        for claim in cs:
            if claim.claim_id in invalid:
                continue
            broken = sorted(d for d in claim.depends_on if d in invalid)
            if broken:
                invalid.add(claim.claim_id)
                changed = True

    debt_rows: list[ClaimDebt] = []
    direct = set(direct_reasons)
    propagated = invalid - direct
    for claim in cs:
        reasons = list(direct_reasons.get(claim.claim_id, ()))
        broken = sorted(d for d in claim.depends_on if d in invalid)
        if claim.claim_id in propagated:
            reasons.append("DEPENDENCY_INVALID:" + "|".join(broken))
        status = "DEBT" if claim.claim_id in invalid else "VALID"
        multiplier = 2 if claim.claim_id in direct else 1
        debt = claim.criticality * multiplier if status == "DEBT" else 0
        debt_rows.append(ClaimDebt(claim.claim_id, status, debt, tuple(sorted(reasons)), usable_by_claim[claim.claim_id]))

    frontier = tuple(sorted(cid for cid in direct if not any(dep in direct for dep in claim_map[cid].depends_on)))
    total = sum(row.debt_points for row in debt_rows)
    status = "FREEZE" if total else "PASS"
    payload = {"status": status, "total": total, "frontier": frontier, "claims": debt_rows}
    return DebtReport(status, total, tuple(sorted(direct)), tuple(sorted(propagated)), frontier, tuple(debt_rows), stable_hash(payload))
