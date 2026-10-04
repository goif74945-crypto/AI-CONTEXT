from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .canonical import record_digest
from .comparator import compare_pair
from .models import DecisionRecord, Finding, GateReport, Severity


def evaluate_datasets(
    stable_records: Iterable[DecisionRecord],
    candidate_records: Iterable[DecisionRecord],
) -> GateReport:
    stable_list = tuple(stable_records)
    candidate_list = tuple(candidate_records)

    findings: list[Finding] = []
    stable = _index_unique(stable_list, "stable", findings)
    candidate = _index_candidate(candidate_list, findings)

    stable_ids = set(stable)
    candidate_ids = set(candidate)

    for case_id in sorted(stable_ids - candidate_ids):
        findings.append(
            Finding(
                code="COVERAGE_GAP",
                severity=Severity.BLOCKING,
                case_id=case_id,
                message="candidate has no result for a stable baseline case",
            )
        )

    for case_id in sorted(candidate_ids - stable_ids):
        findings.append(
            Finding(
                code="UNBASELINED_CASE",
                severity=Severity.WARNING,
                case_id=case_id,
                message="candidate produced a case with no stable comparison baseline",
            )
        )

    compared = 0
    for case_id in sorted(stable_ids & candidate_ids):
        compared += 1
        findings.extend(compare_pair(stable[case_id], candidate[case_id]))

    blocking = any(f.severity is Severity.BLOCKING for f in findings)
    warnings = any(f.severity is Severity.WARNING for f in findings)
    status = "FAIL" if blocking else ("NOT_VERIFIED" if warnings else "PASS")
    return GateReport(
        status=status,
        stable_cases=len(stable_list),
        candidate_cases=len(candidate_list),
        compared_cases=compared,
        findings=tuple(findings),
    )


def _index_unique(records: tuple[DecisionRecord, ...], side: str, findings: list[Finding]) -> dict[str, DecisionRecord]:
    result: dict[str, DecisionRecord] = {}
    for record in records:
        if record.case_id in result:
            findings.append(
                Finding(
                    code="DUPLICATE_BASELINE_CASE",
                    severity=Severity.BLOCKING,
                    case_id=record.case_id,
                    message=f"{side} dataset contains duplicate case IDs",
                )
            )
            continue
        result[record.case_id] = record
    return result


def _index_candidate(records: tuple[DecisionRecord, ...], findings: list[Finding]) -> dict[str, DecisionRecord]:
    grouped: dict[str, list[DecisionRecord]] = defaultdict(list)
    for record in records:
        grouped[record.case_id].append(record)

    result: dict[str, DecisionRecord] = {}
    for case_id, group in grouped.items():
        digests = {record_digest(record) for record in group}
        if len(digests) > 1:
            findings.append(
                Finding(
                    code="NONDETERMINISTIC_CANDIDATE",
                    severity=Severity.BLOCKING,
                    case_id=case_id,
                    message="candidate emitted structurally different records for the same case ID",
                )
            )
        elif len(group) > 1:
            findings.append(
                Finding(
                    code="DUPLICATE_IDENTICAL_CANDIDATE",
                    severity=Severity.WARNING,
                    case_id=case_id,
                    message="candidate repeated an identical decision record",
                )
            )
        result[case_id] = group[0]
    return result
