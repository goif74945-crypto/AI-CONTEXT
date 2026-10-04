from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


NEGATIVE_OBLIGATIONS = frozenset({"FORBID", "FREEZE_ON", "DENY", "MUST_NOT"})


@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    obligation: str
    text: str = ""


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    requirement_ids: frozenset[str]
    polarity: str  # positive | negative
    status: str
    evidence_class: str


@dataclass(frozen=True)
class Finding:
    requirement_id: str
    status: str  # COVERED | MISSING_NEGATIVE_PATH
    qualifying_evidence_ids: tuple[str, ...]
    misleading_positive_ids: tuple[str, ...]
    failed_negative_ids: tuple[str, ...]


@dataclass(frozen=True)
class CoverageReport:
    negative_requirements: int
    covered: int
    missing: int
    coverage_ratio: float
    findings: tuple[Finding, ...]


def analyze_negative_space(
    requirements: Iterable[Requirement],
    evidence: Iterable[Evidence],
    *,
    accepted_evidence_classes: frozenset[str] = frozenset({"E2", "E3", "E4", "E5", "E6", "E7"}),
) -> CoverageReport:
    """Audit explicit negative-path proof for prohibition/freeze obligations."""
    reqs = tuple(sorted(requirements, key=lambda r: r.requirement_id))
    evs = tuple(sorted(evidence, key=lambda e: e.evidence_id))

    ids = [r.requirement_id for r in reqs]
    if len(ids) != len(set(ids)):
        raise ValueError("requirement_id values must be unique")
    ev_ids = [e.evidence_id for e in evs]
    if len(ev_ids) != len(set(ev_ids)):
        raise ValueError("evidence_id values must be unique")
    if not accepted_evidence_classes:
        raise ValueError("accepted_evidence_classes must not be empty")

    by_requirement: dict[str, list[Evidence]] = defaultdict(list)
    for ev in evs:
        if ev.polarity not in {"positive", "negative"}:
            raise ValueError(f"invalid evidence polarity: {ev.polarity}")
        for requirement_id in ev.requirement_ids:
            by_requirement[requirement_id].append(ev)

    findings = []
    for req in reqs:
        if req.obligation.upper() not in NEGATIVE_OBLIGATIONS:
            continue
        linked = by_requirement.get(req.requirement_id, ())
        qualifying = tuple(
            e.evidence_id
            for e in linked
            if e.polarity == "negative"
            and e.status == "PASS"
            and e.evidence_class in accepted_evidence_classes
        )
        misleading_positive = tuple(
            e.evidence_id for e in linked if e.polarity == "positive" and e.status == "PASS"
        )
        failed_negative = tuple(
            e.evidence_id
            for e in linked
            if e.polarity == "negative"
            and (e.status != "PASS" or e.evidence_class not in accepted_evidence_classes)
        )
        status = "COVERED" if qualifying else "MISSING_NEGATIVE_PATH"
        findings.append(
            Finding(
                requirement_id=req.requirement_id,
                status=status,
                qualifying_evidence_ids=qualifying,
                misleading_positive_ids=misleading_positive,
                failed_negative_ids=failed_negative,
            )
        )

    covered = sum(1 for f in findings if f.status == "COVERED")
    total = len(findings)
    ratio = 1.0 if total == 0 else covered / total
    return CoverageReport(
        negative_requirements=total,
        covered=covered,
        missing=total - covered,
        coverage_ratio=ratio,
        findings=tuple(findings),
    )
