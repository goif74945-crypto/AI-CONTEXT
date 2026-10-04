from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Iterable


class WitnessError(ValueError):
    """Raised when a requirement cannot be deterministically witnessed."""


@dataclass(frozen=True)
class RequirementSpec:
    requirement_id: str
    field: str
    operator: str
    value: Any
    required: bool = True


@dataclass(frozen=True)
class Witness:
    requirement_id: str
    kind: str
    payload: dict[str, Any]
    should_pass: bool
    reason: str


class RequirementBoundaryWitnessEngine:
    """Compiles a deliberately small explicit DSL into deterministic boundary witnesses."""

    SUPPORTED = {"eq", "neq", "min", "max", "in"}

    def generate(self, spec: RequirementSpec) -> tuple[Witness, ...]:
        self._validate(spec)
        positive = self._positive_value(spec)
        negative = self._negative_value(spec)
        witnesses = [
            Witness(spec.requirement_id, "positive", {spec.field: positive}, True, "canonical satisfying boundary"),
            Witness(spec.requirement_id, "negative", {spec.field: negative}, False, "canonical violating boundary"),
        ]
        if spec.required:
            witnesses.append(
                Witness(spec.requirement_id, "missing", {}, False, "required field omitted")
            )
        return tuple(witnesses)

    def detect_contradictions(
        self, specs: Iterable[RequirementSpec]
    ) -> tuple[tuple[str, str, str], ...]:
        items = list(specs)
        for spec in items:
            self._validate(spec)
        contradictions: list[tuple[str, str, str]] = []
        for i, left in enumerate(items):
            for right in items[i + 1 :]:
                if left.field != right.field:
                    continue
                reason = self._pair_contradiction(left, right)
                if reason is not None:
                    a, b = sorted((left.requirement_id, right.requirement_id))
                    contradictions.append((a, b, reason))
        return tuple(sorted(set(contradictions)))

    def evaluate(self, spec: RequirementSpec, payload: dict[str, Any]) -> bool:
        self._validate(spec)
        if spec.field not in payload:
            return not spec.required
        actual = payload[spec.field]
        try:
            if spec.operator == "eq":
                return actual == spec.value
            if spec.operator == "neq":
                return actual != spec.value
            if spec.operator == "min":
                return actual >= spec.value
            if spec.operator == "max":
                return actual <= spec.value
            if spec.operator == "in":
                return actual in spec.value
        except (TypeError, ValueError):
            return False
        raise AssertionError("unreachable")

    def _validate(self, spec: RequirementSpec) -> None:
        if not spec.requirement_id.strip():
            raise WitnessError("requirement_id is empty")
        if not spec.field.strip():
            raise WitnessError(f"{spec.requirement_id}: field is empty")
        if spec.operator not in self.SUPPORTED:
            raise WitnessError(f"{spec.requirement_id}: unsupported operator {spec.operator!r}")
        if spec.operator in {"eq", "neq"}:
            self._validate_scalar(spec.value, spec.requirement_id)
        if spec.operator in {"min", "max"}:
            if isinstance(spec.value, bool) or not isinstance(spec.value, (int, float)):
                raise WitnessError(f"{spec.requirement_id}: finite numeric boundary required")
            if isinstance(spec.value, float) and not math.isfinite(spec.value):
                raise WitnessError(f"{spec.requirement_id}: finite numeric boundary required")
        if spec.operator == "in":
            if not isinstance(spec.value, (tuple, list, frozenset)) or not spec.value:
                raise WitnessError(f"{spec.requirement_id}: non-empty finite set required")
            for value in spec.value:
                self._validate_scalar(value, spec.requirement_id)

    @staticmethod
    def _validate_scalar(value: Any, requirement_id: str) -> None:
        if value is None or isinstance(value, (bool, int, str)):
            return
        if isinstance(value, float) and math.isfinite(value):
            return
        raise WitnessError(f"{requirement_id}: value must be a finite JSON-like scalar")

    def _positive_value(self, spec: RequirementSpec) -> Any:
        if spec.operator in {"eq", "min", "max"}:
            return spec.value
        if spec.operator == "neq":
            return self._different_value(spec.value)
        if spec.operator == "in":
            return sorted(spec.value, key=lambda x: repr(x))[0]
        raise AssertionError("unreachable")

    def _negative_value(self, spec: RequirementSpec) -> Any:
        if spec.operator == "eq":
            return self._different_value(spec.value)
        if spec.operator == "neq":
            return spec.value
        if spec.operator == "min":
            return spec.value - 1
        if spec.operator == "max":
            return spec.value + 1
        if spec.operator == "in":
            candidate = "__NEXY_OUTSIDE_SET__"
            values = list(spec.value)
            if all(candidate != value for value in values):
                return candidate
            i = 0
            while any(f"{candidate}_{i}" == value for value in values):
                i += 1
            return f"{candidate}_{i}"
        raise AssertionError("unreachable")

    @staticmethod
    def _different_value(value: Any) -> Any:
        if isinstance(value, bool):
            return not value
        if isinstance(value, int):
            return value + 1
        if isinstance(value, float):
            return math.nextafter(value, math.inf)
        if isinstance(value, str):
            return value + "__DIFF"
        if value is None:
            return "__NON_NULL__"
        raise WitnessError("unsupported scalar value")

    @staticmethod
    def _pair_contradiction(left: RequirementSpec, right: RequirementSpec) -> str | None:
        if left.operator == right.operator == "eq" and left.value != right.value:
            return "distinct equality requirements on same field"
        pair = {left.operator, right.operator}
        if pair == {"min", "max"}:
            minimum = left.value if left.operator == "min" else right.value
            maximum = left.value if left.operator == "max" else right.value
            if minimum > maximum:
                return "minimum exceeds maximum"
        if left.operator == "eq" and right.operator == "neq" and left.value == right.value:
            return "equality conflicts with inequality"
        if right.operator == "eq" and left.operator == "neq" and right.value == left.value:
            return "equality conflicts with inequality"
        if left.operator == "eq" and right.operator == "in" and left.value not in right.value:
            return "equality value excluded by allowed set"
        if right.operator == "eq" and left.operator == "in" and right.value not in left.value:
            return "equality value excluded by allowed set"
        return None
