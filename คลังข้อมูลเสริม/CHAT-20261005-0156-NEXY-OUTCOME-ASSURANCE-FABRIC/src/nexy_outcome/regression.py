from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .errors import ObservationValidationError
from .model import Criterion, OutcomeContract
from .verifier import resolve_path, verify_outcome


def _guard_regressed(criterion: Criterion, baseline: Any, candidate: Any) -> tuple[bool, str]:
    if criterion.op == "max":
        if isinstance(baseline, bool) or isinstance(candidate, bool):
            return True, "numeric_type_mismatch"
        if not isinstance(baseline, (int, float)) or not isinstance(candidate, (int, float)):
            return True, "numeric_type_mismatch"
        return candidate > baseline + criterion.max_regression, "higher_is_worse"
    if criterion.op == "min":
        if isinstance(baseline, bool) or isinstance(candidate, bool):
            return True, "numeric_type_mismatch"
        if not isinstance(baseline, (int, float)) or not isinstance(candidate, (int, float)):
            return True, "numeric_type_mismatch"
        return candidate + criterion.max_regression < baseline, "lower_is_worse"
    # For eq/range/in, preserve satisfaction rather than inventing an ordering.
    from .verifier import evaluate_relation

    baseline_ok, _, _ = evaluate_relation(criterion.op, criterion.value, baseline)
    candidate_ok, _, _ = evaluate_relation(criterion.op, criterion.value, candidate)
    return baseline_ok and not candidate_ok, "satisfaction_lost"


def benefit_regression_guard(
    contract: OutcomeContract,
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(baseline, Mapping) or not isinstance(candidate, Mapping):
        raise ObservationValidationError("baseline and candidate must be objects")

    baseline_report = verify_outcome(contract, baseline)
    candidate_report = verify_outcome(contract, candidate)
    if baseline_report["status"] == "FREEZE" or candidate_report["status"] == "FREEZE":
        return {
            "status": "FREEZE",
            "regressions": [],
            "baseline_status": baseline_report["status"],
            "candidate_status": candidate_report["status"],
            "reason": "missing_observation",
        }

    regressions: list[dict[str, Any]] = []
    for criterion in contract.criteria:
        if not criterion.regression_guard:
            continue
        base_value = resolve_path(baseline, criterion.path)
        candidate_value = resolve_path(candidate, criterion.path)
        # Missing paths have already forced FREEZE, so these are present here.
        regressed, reason = _guard_regressed(criterion, base_value, candidate_value)
        if regressed:
            regressions.append(
                {
                    "criterion_id": criterion.criterion_id,
                    "path": criterion.path,
                    "baseline": base_value,
                    "candidate": candidate_value,
                    "max_regression": criterion.max_regression,
                    "reason": reason,
                }
            )

    if candidate_report["status"] == "FAIL" or regressions:
        status = "FAIL"
    else:
        status = "PASS"
    return {
        "status": status,
        "regressions": sorted(regressions, key=lambda x: x["criterion_id"]),
        "baseline_status": baseline_report["status"],
        "candidate_status": candidate_report["status"],
        "baseline_soft_score": baseline_report["soft_score"],
        "candidate_soft_score": candidate_report["soft_score"],
    }
