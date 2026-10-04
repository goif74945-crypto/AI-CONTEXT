from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import content_hash
from .errors import ObservationValidationError
from .model import Criterion, CriterionResult, OutcomeContract

_MISSING = object()


def resolve_path(observation: Mapping[str, Any], path: str) -> Any:
    current: Any = observation
    for segment in path.split("."):
        if not isinstance(current, Mapping) or segment not in current:
            return _MISSING
        current = current[segment]
    return current


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    if result != result or result in (float("inf"), float("-inf")):
        return None
    return result


def evaluate_relation(op: str, expected: Any, actual: Any) -> tuple[bool, float | None, str]:
    if op in {"min", "max"}:
        a = _numeric(actual)
        e = _numeric(expected)
        if a is None or e is None:
            return False, None, "numeric_type_mismatch"
        if op == "min":
            margin = a - e
            return a >= e, margin, "actual>=minimum" if a >= e else "below_minimum"
        margin = e - a
        return a <= e, margin, "actual<=maximum" if a <= e else "above_maximum"
    if op == "eq":
        ok = actual == expected
        if _numeric(actual) is not None and _numeric(expected) is not None:
            margin = -abs(float(actual) - float(expected))
        else:
            margin = 0.0 if ok else -1.0
        return ok, margin, "equal" if ok else "not_equal"
    if op == "range":
        a = _numeric(actual)
        if a is None:
            return False, None, "numeric_type_mismatch"
        low, high = float(expected[0]), float(expected[1])
        if low <= a <= high:
            return True, min(a - low, high - a), "inside_range"
        distance = low - a if a < low else a - high
        return False, -distance, "outside_range"
    if op == "in":
        ok = actual in expected
        return ok, 0.0 if ok else -1.0, "member" if ok else "not_member"
    raise ObservationValidationError(f"unsupported operator at runtime: {op}")


def evaluate_criterion(criterion: Criterion, observation: Mapping[str, Any]) -> CriterionResult | None:
    actual = resolve_path(observation, criterion.path)
    if actual is _MISSING:
        return None
    satisfied, margin, reason = evaluate_relation(criterion.op, criterion.value, actual)
    safe_actual = None if reason == "numeric_type_mismatch" else actual
    return CriterionResult(
        criterion_id=criterion.criterion_id,
        path=criterion.path,
        hard=criterion.hard,
        satisfied=satisfied,
        actual=safe_actual,
        expected=criterion.value,
        margin=margin,
        reason=reason,
    )


def verify_outcome(contract: OutcomeContract, observation: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(observation, Mapping):
        raise ObservationValidationError("observation must be an object")

    results: list[CriterionResult] = []
    missing: list[str] = []
    invalid: list[str] = []
    hard_failures: list[str] = []
    soft_failures: list[str] = []

    for criterion in contract.criteria:
        result = evaluate_criterion(criterion, observation)
        if result is None:
            missing.append(criterion.path)
            continue
        results.append(result)
        if result.reason == "numeric_type_mismatch":
            invalid.append(criterion.path)
            continue
        if not result.satisfied:
            (hard_failures if criterion.hard else soft_failures).append(criterion.criterion_id)

    forbidden_violations: list[dict[str, Any]] = []
    for effect in contract.forbidden_effects:
        actual = resolve_path(observation, effect.path)
        if actual is _MISSING:
            missing.append(effect.path)
            continue
        matched, _, reason = evaluate_relation(effect.op, effect.value, actual)
        if reason == "numeric_type_mismatch":
            invalid.append(effect.path)
            continue
        if matched:
            forbidden_violations.append(
                {"effect_id": effect.effect_id, "path": effect.path, "actual": actual, "reason": reason}
            )

    missing = sorted(set(missing))
    invalid = sorted(set(invalid))
    if missing or invalid:
        status = "FREEZE"
    elif forbidden_violations or hard_failures:
        status = "FAIL"
    elif soft_failures:
        status = "PARTIAL"
    else:
        status = "PASS"

    soft_total = sum(item.weight for item in contract.criteria if not item.hard)
    soft_pass = sum(
        item.weight
        for item in contract.criteria
        if not item.hard and item.criterion_id not in soft_failures
    )
    soft_score = 1.0 if soft_total == 0 else soft_pass / soft_total

    report = {
        "status": status,
        "contract_hash": content_hash(contract.to_dict()),
        "objective_id": contract.objective_id,
        "soft_score": soft_score,
        "criteria": [item.to_dict() for item in sorted(results, key=lambda x: x.criterion_id)],
        "hard_failures": sorted(hard_failures),
        "soft_failures": sorted(soft_failures),
        "forbidden_violations": sorted(forbidden_violations, key=lambda x: x["effect_id"]),
        "missing_observations": missing,
        "invalid_observations": invalid,
    }
    report["report_hash"] = content_hash(report)
    return report
