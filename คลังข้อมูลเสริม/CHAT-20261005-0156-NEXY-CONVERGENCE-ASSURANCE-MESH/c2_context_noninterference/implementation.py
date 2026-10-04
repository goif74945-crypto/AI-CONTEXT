from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any, Callable, Iterable, Mapping, Sequence

from shared import GateResult, sha256_hex


DecisionFn = Callable[[Mapping[str, Any]], Any]


@dataclass(frozen=True)
class MutationSet:
    field: str
    values: tuple[Any, ...]

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise ValueError("field must be non-empty")
        if not self.values:
            raise ValueError("mutation set must contain at least one value")


def _decision_fingerprint(decision: Any) -> str:
    return sha256_hex(decision)


def verify_noninterference(
    baseline_context: Mapping[str, Any],
    excluded_field_mutations: Iterable[MutationSet],
    decision_fn: DecisionFn,
    *,
    include_joint_case: bool = True,
    max_joint_cases: int = 64,
) -> GateResult:
    mutations = sorted(tuple(excluded_field_mutations), key=lambda item: item.field)
    fields = [item.field for item in mutations]
    if len(fields) != len(set(fields)):
        return GateResult("BLOCKED", "DUPLICATE_MUTATION_FIELD", {"fields": fields})
    if max_joint_cases < 0:
        return GateResult("BLOCKED", "INVALID_MAX_JOINT_CASES", {"value": max_joint_cases})

    try:
        baseline_decision = decision_fn(dict(baseline_context))
        baseline_hash = _decision_fingerprint(baseline_decision)
    except Exception as exc:
        return GateResult(
            "BLOCKED",
            "BASELINE_EVALUATION_FAILED",
            {"error_type": type(exc).__name__, "error": str(exc)},
        )

    checked: list[dict[str, Any]] = []

    def check_case(label: str, updates: Mapping[str, Any]) -> GateResult | None:
        candidate = dict(baseline_context)
        candidate.update(updates)
        try:
            decision = decision_fn(candidate)
            decision_hash = _decision_fingerprint(decision)
        except Exception as exc:
            return GateResult(
                "FAIL",
                "EXCLUDED_CONTEXT_CAUSED_EVALUATOR_FAILURE",
                {
                    "case": label,
                    "updates": dict(updates),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
        checked.append({"case": label, "updates": dict(updates), "decision_hash": decision_hash})
        if decision_hash != baseline_hash:
            return GateResult(
                "FAIL",
                "NONINTERFERENCE_VIOLATION",
                {
                    "case": label,
                    "updates": dict(updates),
                    "baseline_hash": baseline_hash,
                    "mutated_hash": decision_hash,
                    "baseline_decision": baseline_decision,
                    "mutated_decision": decision,
                },
            )
        return None

    for mutation in mutations:
        for index, value in enumerate(mutation.values):
            failure = check_case(f"single:{mutation.field}:{index}", {mutation.field: value})
            if failure:
                return failure

    joint_case_count = 0
    if include_joint_case and mutations:
        cardinality = 1
        for mutation in mutations:
            cardinality *= len(mutation.values)
        if cardinality > max_joint_cases:
            return GateResult(
                "BLOCKED",
                "JOINT_MUTATION_BUDGET_EXCEEDED",
                {"required_cases": cardinality, "max_joint_cases": max_joint_cases},
            )
        for index, values in enumerate(product(*(item.values for item in mutations))):
            updates = {mutation.field: value for mutation, value in zip(mutations, values, strict=True)}
            failure = check_case(f"joint:{index}", updates)
            if failure:
                return failure
            joint_case_count += 1

    return GateResult(
        "PASS",
        "TESTED_EXCLUDED_CONTEXT_DID_NOT_CHANGE_DECISION",
        {
            "baseline_hash": baseline_hash,
            "single_cases": sum(len(item.values) for item in mutations),
            "joint_cases": joint_case_count,
            "checked_fields": fields,
            "scope_note": "Finite mutation evidence only; not a universal noninterference proof.",
            "checked": checked,
        },
    )
