from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence


class RelationDefinitionError(ValueError):
    """Raised when a relation is undefined, malformed, or unsafe to evaluate."""


@dataclass(frozen=True)
class MetamorphicRelation:
    name: str
    transform: str
    expectation: str
    transform_arg: int | None = None
    expectation_arg: int | None = None


@dataclass(frozen=True)
class MetamorphicResult:
    relation: str
    passed: bool
    base_output: Any
    transformed_input: Any
    transformed_output: Any
    reason: str


def _require_numeric(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RelationDefinitionError(f"{label} must be an integer")
    return value


def _transform(value: Any, relation: MetamorphicRelation) -> Any:
    op = relation.transform
    arg = relation.transform_arg
    if op == "identity":
        return value
    if op == "shift_int":
        return _require_numeric(value, "input") + _require_numeric(arg, "transform_arg")
    if op == "scale_int":
        return _require_numeric(value, "input") * _require_numeric(arg, "transform_arg")
    if op == "reverse_sequence":
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise RelationDefinitionError("reverse_sequence requires a non-string sequence")
        return list(reversed(value))
    if op == "sort_sequence":
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise RelationDefinitionError("sort_sequence requires a non-string sequence")
        try:
            return sorted(value)
        except TypeError as exc:
            raise RelationDefinitionError("sequence elements are not mutually sortable") from exc
    raise RelationDefinitionError(f"unknown transform: {op}")


def _same_multiset(left: Any, right: Any) -> bool:
    if isinstance(left, (str, bytes)) or isinstance(right, (str, bytes)):
        raise RelationDefinitionError("same_multiset does not accept strings/bytes")
    if not isinstance(left, Sequence) or not isinstance(right, Sequence):
        raise RelationDefinitionError("same_multiset requires sequence outputs")
    try:
        return sorted(left) == sorted(right)
    except TypeError as exc:
        raise RelationDefinitionError("output elements are not mutually sortable") from exc


def _check_expectation(base: Any, transformed: Any, relation: MetamorphicRelation) -> tuple[bool, str]:
    op = relation.expectation
    arg = relation.expectation_arg
    if op == "equal":
        return base == transformed, "outputs are equal" if base == transformed else "outputs differ"
    if op == "delta_int":
        delta = _require_numeric(arg, "expectation_arg")
        expected = _require_numeric(base, "base_output") + delta
        actual = _require_numeric(transformed, "transformed_output")
        return actual == expected, f"expected transformed output {expected}, observed {actual}"
    if op == "scale_int":
        factor = _require_numeric(arg, "expectation_arg")
        expected = _require_numeric(base, "base_output") * factor
        actual = _require_numeric(transformed, "transformed_output")
        return actual == expected, f"expected transformed output {expected}, observed {actual}"
    if op == "nondecreasing":
        left = _require_numeric(base, "base_output")
        right = _require_numeric(transformed, "transformed_output")
        return right >= left, f"expected transformed output >= {left}, observed {right}"
    if op == "same_multiset":
        ok = _same_multiset(base, transformed)
        return ok, "outputs preserve multiset" if ok else "outputs do not preserve multiset"
    raise RelationDefinitionError(f"unknown expectation: {op}")


def verify_relation(
    subject: Callable[[Any], Any],
    base_input: Any,
    relation: MetamorphicRelation,
) -> MetamorphicResult:
    if not callable(subject):
        raise RelationDefinitionError("subject must be callable")
    if not relation.name.strip():
        raise RelationDefinitionError("relation name must be non-empty")

    transformed_input = _transform(base_input, relation)
    base_output = subject(base_input)
    transformed_output = subject(transformed_input)
    passed, reason = _check_expectation(base_output, transformed_output, relation)
    return MetamorphicResult(
        relation=relation.name,
        passed=passed,
        base_output=base_output,
        transformed_input=transformed_input,
        transformed_output=transformed_output,
        reason=reason,
    )
