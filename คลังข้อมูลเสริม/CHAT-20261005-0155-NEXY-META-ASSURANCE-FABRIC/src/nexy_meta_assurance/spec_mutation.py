from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, Mapping


class SpecMutationError(ValueError):
    """Raised when the baseline spec, constraints, or validator contract is invalid."""


class ConstraintOp(str, Enum):
    EQ = "eq"
    MIN_INT = "min_int"
    MAX_INT = "max_int"
    MEMBER_OF = "member_of"
    NONEMPTY = "nonempty"


@dataclass(frozen=True)
class Constraint:
    constraint_id: str
    field: str
    op: ConstraintOp
    expected: Any = None


@dataclass(frozen=True)
class MutationCase:
    mutation_id: str
    constraint_id: str
    field: str
    original_value: Any
    mutated_value: Any


@dataclass(frozen=True)
class MutationReport:
    generated: tuple[MutationCase, ...]
    killed: tuple[str, ...]
    survivors: tuple[str, ...]
    passed: bool


def _validate_constraint(constraint: Constraint) -> None:
    if not constraint.constraint_id.strip():
        raise SpecMutationError("constraint_id must be non-empty")
    if not constraint.field.strip():
        raise SpecMutationError(f"constraint {constraint.constraint_id} field must be non-empty")
    if constraint.op in {ConstraintOp.MIN_INT, ConstraintOp.MAX_INT}:
        if isinstance(constraint.expected, bool) or not isinstance(constraint.expected, int):
            raise SpecMutationError(f"constraint {constraint.constraint_id} expected must be an integer")
    if constraint.op == ConstraintOp.MEMBER_OF:
        if not isinstance(constraint.expected, tuple) or not constraint.expected:
            raise SpecMutationError(
                f"constraint {constraint.constraint_id} MEMBER_OF expected must be a non-empty tuple"
            )


def validate_spec(spec: Mapping[str, Any], constraints: Iterable[Constraint]) -> tuple[str, ...]:
    violations: list[str] = []
    seen: set[str] = set()
    for constraint in constraints:
        _validate_constraint(constraint)
        if constraint.constraint_id in seen:
            raise SpecMutationError(f"duplicate constraint ID: {constraint.constraint_id}")
        seen.add(constraint.constraint_id)
        if constraint.field not in spec:
            violations.append(constraint.constraint_id)
            continue
        value = spec[constraint.field]
        if constraint.op == ConstraintOp.EQ:
            ok = value == constraint.expected
        elif constraint.op == ConstraintOp.MIN_INT:
            ok = not isinstance(value, bool) and isinstance(value, int) and value >= constraint.expected
        elif constraint.op == ConstraintOp.MAX_INT:
            ok = not isinstance(value, bool) and isinstance(value, int) and value <= constraint.expected
        elif constraint.op == ConstraintOp.MEMBER_OF:
            ok = value in constraint.expected
        elif constraint.op == ConstraintOp.NONEMPTY:
            ok = value is not None and hasattr(value, "__len__") and len(value) > 0
        else:
            raise SpecMutationError(f"unsupported constraint op: {constraint.op}")
        if not ok:
            violations.append(constraint.constraint_id)
    return tuple(sorted(violations))


def _different_scalar(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "__MUTATED__"
    if value is None:
        return "__MUTATED__"
    return "__ILLEGAL__"


def _illegal_value(spec_value: Any, constraint: Constraint) -> Any:
    if constraint.op == ConstraintOp.EQ:
        candidate = _different_scalar(constraint.expected)
        if candidate == constraint.expected:
            raise SpecMutationError(f"cannot synthesize EQ mutation for {constraint.constraint_id}")
        return candidate
    if constraint.op == ConstraintOp.MIN_INT:
        return constraint.expected - 1
    if constraint.op == ConstraintOp.MAX_INT:
        return constraint.expected + 1
    if constraint.op == ConstraintOp.MEMBER_OF:
        candidate = "__ILLEGAL_MEMBER__"
        while candidate in constraint.expected:
            candidate += "_X"
        return candidate
    if constraint.op == ConstraintOp.NONEMPTY:
        if isinstance(spec_value, str):
            return ""
        if isinstance(spec_value, tuple):
            return ()
        if isinstance(spec_value, list):
            return []
        if isinstance(spec_value, dict):
            return {}
        raise SpecMutationError(
            f"cannot synthesize NONEMPTY mutation for unsupported type: {type(spec_value).__name__}"
        )
    raise SpecMutationError(f"unsupported constraint op: {constraint.op}")


def generate_illegal_mutations(
    spec: Mapping[str, Any],
    constraints: Iterable[Constraint],
) -> tuple[MutationCase, ...]:
    constraints_tuple = tuple(constraints)
    baseline_violations = validate_spec(spec, constraints_tuple)
    if baseline_violations:
        raise SpecMutationError(
            "baseline spec must satisfy all constraints before mutation testing: "
            + ", ".join(baseline_violations)
        )

    mutations: list[MutationCase] = []
    for constraint in sorted(constraints_tuple, key=lambda item: item.constraint_id):
        original = spec[constraint.field]
        mutated = _illegal_value(original, constraint)
        mutations.append(
            MutationCase(
                mutation_id=f"MUT::{constraint.constraint_id}",
                constraint_id=constraint.constraint_id,
                field=constraint.field,
                original_value=original,
                mutated_value=mutated,
            )
        )
    return tuple(mutations)


def run_mutation_sentinel(
    spec: Mapping[str, Any],
    constraints: Iterable[Constraint],
    validator: Callable[[Mapping[str, Any]], bool],
) -> MutationReport:
    if not callable(validator):
        raise SpecMutationError("validator must be callable")
    constraints_tuple = tuple(constraints)
    mutations = generate_illegal_mutations(spec, constraints_tuple)
    baseline_result = validator(spec)
    if not isinstance(baseline_result, bool):
        raise SpecMutationError("validator must return bool")
    if not baseline_result:
        raise SpecMutationError("validator rejects the valid baseline spec")

    killed: list[str] = []
    survivors: list[str] = []
    for mutation in mutations:
        mutated_spec = dict(spec)
        mutated_spec[mutation.field] = mutation.mutated_value
        accepted = validator(mutated_spec)
        if not isinstance(accepted, bool):
            raise SpecMutationError("validator must return bool")
        if accepted:
            survivors.append(mutation.mutation_id)
        else:
            killed.append(mutation.mutation_id)

    return MutationReport(
        generated=mutations,
        killed=tuple(killed),
        survivors=tuple(survivors),
        passed=not survivors,
    )
