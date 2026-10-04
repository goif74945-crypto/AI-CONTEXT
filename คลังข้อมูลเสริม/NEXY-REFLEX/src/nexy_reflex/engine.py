"""Fail-closed deterministic evaluation engine for NEXY-REFLEX."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .canonical import canonical_json, sha256_digest
from .models import (
    NON_GATING_SCOPES,
    EvidenceRecord,
    Finding,
    GateAction,
    GateDecision,
    RequirementClaim,
    Severity,
    Snapshot,
    TruthStatus,
)
from .semantics import snapshot_digest


def evaluate_snapshot(snapshot: Snapshot) -> GateDecision:
    """Evaluate a snapshot deterministically without mutating external systems."""
    input_digest = snapshot_digest(snapshot)
    findings: list[Finding] = []

    structural_findings = _validate_structure(snapshot)
    findings.extend(structural_findings)
    if any(item.severity is Severity.BLOCKING for item in structural_findings):
        return _finalize(snapshot, input_digest, (), (), findings)

    effective, non_gating, authority_findings = _resolve_authority(snapshot)
    findings.extend(authority_findings)

    cycle_findings = _dependency_findings(effective)
    findings.extend(cycle_findings)

    evidence_findings = _evaluate_evidence(snapshot, effective)
    findings.extend(evidence_findings)

    return _finalize(
        snapshot,
        input_digest,
        tuple(sorted(claim.claim_id for claim in effective.values())),
        tuple(sorted(non_gating)),
        findings,
    )



def _validate_structure(snapshot: Snapshot) -> list[Finding]:
    findings: list[Finding] = []
    requirement_by_id: dict[str, RequirementClaim] = {}
    for claim in snapshot.requirements:
        previous = requirement_by_id.get(claim.claim_id)
        if previous is None:
            requirement_by_id[claim.claim_id] = claim
        else:
            identical = canonical_json(previous.to_dict()) == canonical_json(claim.to_dict())
            findings.append(
                Finding(
                    code="DUPLICATE_REQUIREMENT_ID",
                    status=TruthStatus.BLOCKED,
                    severity=Severity.BLOCKING,
                    subject=claim.claim_id,
                    detail=(
                        "duplicate requirement id is not allowed, even when definitions match"
                        if identical
                        else "duplicate requirement id has non-identical definitions"
                    ),
                    related_ids=(claim.claim_id,),
                )
            )

        if claim.authority not in snapshot.authority_order:
            findings.append(
                Finding(
                    code="UNKNOWN_AUTHORITY",
                    status=TruthStatus.BLOCKED,
                    severity=Severity.BLOCKING,
                    subject=claim.claim_id,
                    detail=f"authority {claim.authority!r} is absent from authority_order",
                    related_ids=(claim.claim_id,),
                )
            )

    seen_evidence: dict[str, EvidenceRecord] = {}
    for record in snapshot.evidence:
        previous = seen_evidence.get(record.evidence_id)
        if previous is None:
            seen_evidence[record.evidence_id] = record
        else:
            identical = canonical_json(previous.to_dict()) == canonical_json(record.to_dict())
            findings.append(
                Finding(
                    code="DUPLICATE_EVIDENCE_ID",
                    status=TruthStatus.BLOCKED,
                    severity=Severity.BLOCKING,
                    subject=record.evidence_id,
                    detail=(
                        "duplicate evidence id is not allowed, even when definitions match"
                        if identical
                        else "duplicate evidence id has non-identical definitions"
                    ),
                    related_ids=(record.evidence_id,),
                )
            )

        if record.requirement_id not in requirement_by_id:
            findings.append(
                Finding(
                    code="ORPHAN_EVIDENCE",
                    status=TruthStatus.BLOCKED,
                    severity=Severity.BLOCKING,
                    subject=record.evidence_id,
                    detail=f"evidence references missing requirement {record.requirement_id!r}",
                    related_ids=(record.evidence_id, record.requirement_id),
                )
            )

    return findings


def _resolve_authority(
    snapshot: Snapshot,
) -> tuple[dict[str, RequirementClaim], set[str], list[Finding]]:
    rank = {name: idx for idx, name in enumerate(snapshot.authority_order)}
    by_key: dict[str, list[RequirementClaim]] = defaultdict(list)
    for claim in snapshot.requirements:
        by_key[claim.key].append(claim)

    effective: dict[str, RequirementClaim] = {}
    non_gating: set[str] = set()
    findings: list[Finding] = []

    for key in sorted(by_key):
        claims = by_key[key]
        top_rank = min(rank[claim.authority] for claim in claims)
        top = [claim for claim in claims if rank[claim.authority] == top_rank]
        value_buckets: dict[str, list[RequirementClaim]] = defaultdict(list)
        for claim in top:
            value_buckets[_normative_signature(claim)].append(claim)

        if len(value_buckets) > 1:
            related = tuple(sorted(claim.claim_id for claim in top))
            findings.append(
                Finding(
                    code="TOP_AUTHORITY_CONFLICT",
                    status=TruthStatus.CONFLICT,
                    severity=Severity.BLOCKING,
                    subject=key,
                    detail="same highest authority supplies conflicting values for the same requirement key",
                    related_ids=related,
                )
            )
            continue

        chosen = sorted(top, key=lambda claim: claim.claim_id)[0]
        effective[key] = chosen
        if chosen.scope in NON_GATING_SCOPES:
            non_gating.add(chosen.claim_id)

        for claim in sorted(claims, key=lambda item: item.claim_id):
            if claim.claim_id == chosen.claim_id:
                continue
            if rank[claim.authority] > top_rank:
                findings.append(
                    Finding(
                        code="SHADOWED_LOWER_AUTHORITY",
                        status=TruthStatus.PASS,
                        severity=Severity.INFO,
                        subject=claim.claim_id,
                        detail=f"claim is shadowed by higher authority claim {chosen.claim_id}",
                        related_ids=(claim.claim_id, chosen.claim_id),
                    )
                )
            elif _normative_signature(claim) == _normative_signature(chosen):
                findings.append(
                    Finding(
                        code="EQUIVALENT_TOP_AUTHORITY_DUPLICATE",
                        status=TruthStatus.PASS,
                        severity=Severity.INFO,
                        subject=claim.claim_id,
                        detail=f"equivalent top-authority claim collapsed into {chosen.claim_id}",
                        related_ids=(claim.claim_id, chosen.claim_id),
                    )
                )

    return effective, non_gating, findings



def _normative_signature(claim: RequirementClaim) -> str:
    """Hash normative content while excluding identity and source-rank label."""
    return canonical_json(
        {
            "value": claim.value,
            "scope": claim.scope,
            "accepted_evidence_classes": sorted(claim.accepted_evidence_classes),
            "dependencies": sorted(claim.dependencies),
        }
    )

def _dependency_findings(effective: dict[str, RequirementClaim]) -> list[Finding]:
    by_id = {claim.claim_id: claim for claim in effective.values()}
    findings: list[Finding] = []
    for claim in sorted(by_id.values(), key=lambda item: item.claim_id):
        for dep in claim.dependencies:
            if dep not in by_id:
                findings.append(
                    Finding(
                        code="MISSING_EFFECTIVE_DEPENDENCY",
                        status=TruthStatus.BLOCKED,
                        severity=Severity.BLOCKING,
                        subject=claim.claim_id,
                        detail=f"dependency {dep!r} is not an effective requirement",
                        related_ids=(claim.claim_id, dep),
                    )
                )

    color: dict[str, int] = {claim_id: 0 for claim_id in by_id}
    stack: list[str] = []

    def visit(claim_id: str) -> None:
        color[claim_id] = 1
        stack.append(claim_id)
        for dep in sorted(by_id[claim_id].dependencies):
            if dep not in by_id:
                continue
            if color[dep] == 0:
                visit(dep)
            elif color[dep] == 1:
                cycle_start = stack.index(dep)
                cycle = tuple(stack[cycle_start:] + [dep])
                findings.append(
                    Finding(
                        code="DEPENDENCY_CYCLE",
                        status=TruthStatus.BLOCKED,
                        severity=Severity.BLOCKING,
                        subject=claim_id,
                        detail="effective requirement dependency graph contains a cycle",
                        related_ids=cycle,
                    )
                )
        stack.pop()
        color[claim_id] = 2

    for claim_id in sorted(by_id):
        if color[claim_id] == 0:
            visit(claim_id)
    return _dedupe_findings(findings)


def _evaluate_evidence(
    snapshot: Snapshot,
    effective: dict[str, RequirementClaim],
) -> list[Finding]:
    by_req: dict[str, list[EvidenceRecord]] = defaultdict(list)
    for record in snapshot.evidence:
        by_req[record.requirement_id].append(record)

    findings: list[Finding] = []
    for claim in sorted(effective.values(), key=lambda item: item.claim_id):
        if claim.scope in NON_GATING_SCOPES:
            continue

        candidates = sorted(by_req.get(claim.claim_id, []), key=lambda item: item.evidence_id)
        current: list[EvidenceRecord] = []
        stale: list[EvidenceRecord] = []
        for record in candidates:
            if _evidence_matches_target(record, snapshot):
                current.append(record)
            else:
                stale.append(record)

        if stale:
            findings.append(
                Finding(
                    code="STALE_EVIDENCE_PRESENT",
                    status=TruthStatus.NOT_VERIFIED,
                    severity=Severity.WARNING,
                    subject=claim.claim_id,
                    detail="one or more evidence records target a different revision or content digest",
                    related_ids=tuple(item.evidence_id for item in stale),
                )
            )

        accepted = [
            item
            for item in current
            if item.evidence_class in claim.accepted_evidence_classes and item.status is TruthStatus.PASS
        ]
        explicit_failures = [
            item
            for item in current
            if item.evidence_class in claim.accepted_evidence_classes and item.status is TruthStatus.FAIL
        ]

        if explicit_failures:
            findings.append(
                Finding(
                    code="CURRENT_REQUIRED_EVIDENCE_FAIL",
                    status=TruthStatus.FAIL,
                    severity=Severity.BLOCKING,
                    subject=claim.claim_id,
                    detail="current evidence in an accepted evidence class explicitly failed",
                    related_ids=tuple(item.evidence_id for item in explicit_failures),
                )
            )
        elif not accepted:
            findings.append(
                Finding(
                    code="MISSING_CURRENT_PASS_EVIDENCE",
                    status=TruthStatus.NOT_VERIFIED,
                    severity=Severity.BLOCKING,
                    subject=claim.claim_id,
                    detail="no current PASS evidence exists in an accepted evidence class",
                    related_ids=tuple(item.evidence_id for item in current),
                )
            )

    return findings


def _evidence_matches_target(record: EvidenceRecord, snapshot: Snapshot) -> bool:
    if record.target_revision != snapshot.target.revision:
        return False
    if snapshot.target.content_digest is not None:
        return record.target_digest == snapshot.target.content_digest
    return True


def _finalize(
    snapshot: Snapshot,
    input_digest: str,
    effective_requirements: tuple[str, ...],
    non_gating_requirements: tuple[str, ...],
    findings: list[Finding],
) -> GateDecision:
    ordered = tuple(
        sorted(
            _dedupe_findings(findings),
            key=lambda item: (
                item.severity.value,
                item.status.value,
                item.code,
                item.subject,
                item.related_ids,
                item.detail,
            ),
        )
    )
    verdict = _derive_verdict(ordered)
    action = GateAction.ACCEPT_ADVISORY if verdict is TruthStatus.PASS else GateAction.FREEZE_RECOMMENDED
    decision_body: dict[str, Any] = {
        "snapshot_version": snapshot.snapshot_version,
        "target": snapshot.target.to_dict(),
        "verdict": verdict.value,
        "action": action.value,
        "input_digest": input_digest,
        "effective_requirements": list(effective_requirements),
        "non_gating_requirements": list(non_gating_requirements),
        "findings": [item.to_dict() for item in ordered],
    }
    return GateDecision(
        verdict=verdict,
        action=action,
        input_digest=input_digest,
        decision_digest=sha256_digest(decision_body),
        effective_requirements=effective_requirements,
        non_gating_requirements=non_gating_requirements,
        findings=ordered,
    )


def _derive_verdict(findings: tuple[Finding, ...]) -> TruthStatus:
    statuses = {item.status for item in findings if item.severity is Severity.BLOCKING}
    # Structural BLOCKED findings return early before authority evaluation.
    # After that gate, an authority CONFLICT is the primary causal truth and
    # must not be hidden by dependency cascades caused by the unresolved claim.
    if TruthStatus.CONFLICT in statuses:
        return TruthStatus.CONFLICT
    if TruthStatus.BLOCKED in statuses:
        return TruthStatus.BLOCKED
    if TruthStatus.FAIL in statuses:
        return TruthStatus.FAIL
    if TruthStatus.UNKNOWN in statuses:
        return TruthStatus.UNKNOWN
    if TruthStatus.NOT_VERIFIED in statuses:
        return TruthStatus.NOT_VERIFIED
    if TruthStatus.PARTIAL in statuses:
        return TruthStatus.PARTIAL
    return TruthStatus.PASS


def _dedupe_findings(findings: list[Finding]) -> list[Finding]:
    unique: dict[str, Finding] = {}
    for finding in findings:
        key = canonical_json(finding.to_dict())
        unique[key] = finding
    return list(unique.values())
