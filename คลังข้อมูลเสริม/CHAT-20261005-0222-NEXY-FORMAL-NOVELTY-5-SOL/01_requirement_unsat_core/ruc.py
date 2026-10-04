from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any, Iterable, Mapping, Sequence


class ModelTooLargeError(ValueError):
    """Raised when exhaustive finite-domain verification would exceed the configured bound."""


@dataclass(frozen=True)
class Rule:
    kind: str
    left: str
    value: Any | None = None
    values: tuple[Any, ...] = ()
    right: str | None = None
    right_value: Any | None = None

    def evaluate(self, assignment: Mapping[str, Any]) -> bool:
        left_value = assignment[self.left]
        if self.kind == "eq":
            return left_value == self.value
        if self.kind == "neq":
            return left_value != self.value
        if self.kind == "in":
            return left_value in self.values
        if self.kind == "not_in":
            return left_value not in self.values
        if self.kind == "same":
            if self.right is None:
                raise ValueError("same requires right")
            return left_value == assignment[self.right]
        if self.kind == "different":
            if self.right is None:
                raise ValueError("different requires right")
            return left_value != assignment[self.right]
        if self.kind == "implies":
            if self.right is None:
                raise ValueError("implies requires right")
            return left_value != self.value or assignment[self.right] == self.right_value
        raise ValueError(f"unsupported rule kind: {self.kind}")

    def variables(self) -> set[str]:
        result = {self.left}
        if self.right is not None:
            result.add(self.right)
        return result


@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    rules: tuple[Rule, ...]


@dataclass(frozen=True)
class SolveResult:
    satisfiable: bool
    witness: Mapping[str, Any] | None
    core_ids: tuple[str, ...]
    assignments_checked: int


class RequirementUnsatCore:
    """Finite-domain conflict witness engine.

    It deliberately fails closed when exhaustive verification would exceed max_assignments.
    """

    def __init__(self, domains: Mapping[str, Sequence[Any]], max_assignments: int = 100_000):
        normalized: dict[str, tuple[Any, ...]] = {}
        for name, values in domains.items():
            unique = tuple(dict.fromkeys(values))
            if not unique:
                raise ValueError(f"domain {name!r} is empty")
            normalized[name] = unique
        if not normalized:
            raise ValueError("at least one domain is required")
        if max_assignments < 1:
            raise ValueError("max_assignments must be positive")
        self.domains = normalized
        self.max_assignments = max_assignments

    def _validate_requirements(self, requirements: Iterable[Requirement]) -> tuple[Requirement, ...]:
        reqs = tuple(requirements)
        ids = [r.requirement_id for r in reqs]
        if len(ids) != len(set(ids)):
            raise ValueError("requirement_id values must be unique")
        known = set(self.domains)
        for req in reqs:
            if not req.rules:
                raise ValueError(f"requirement {req.requirement_id!r} has no rules")
            for rule in req.rules:
                unknown = rule.variables() - known
                if unknown:
                    raise ValueError(f"requirement {req.requirement_id!r} uses unknown variables: {sorted(unknown)}")
        return reqs

    def _search(self, requirements: Sequence[Requirement]) -> tuple[bool, Mapping[str, Any] | None, int]:
        names = tuple(sorted(self.domains))
        cardinality = 1
        for name in names:
            cardinality *= len(self.domains[name])
            if cardinality > self.max_assignments:
                raise ModelTooLargeError(
                    f"assignment space {cardinality} exceeds max_assignments={self.max_assignments}"
                )

        checked = 0
        for values in product(*(self.domains[name] for name in names)):
            checked += 1
            assignment = dict(zip(names, values, strict=True))
            if all(rule.evaluate(assignment) for req in requirements for rule in req.rules):
                return True, assignment, checked
        return False, None, checked

    def solve(self, requirements: Iterable[Requirement]) -> SolveResult:
        reqs = self._validate_requirements(requirements)
        satisfiable, witness, checked = self._search(reqs)
        if satisfiable:
            return SolveResult(True, witness, (), checked)

        core = list(reqs)
        index = 0
        # Deterministic deletion-based MUS approximation: irreducible, not guaranteed minimum-cardinality.
        while index < len(core):
            trial = core[:index] + core[index + 1 :]
            trial_sat, _, _ = self._search(trial)
            if not trial_sat:
                core = trial
            else:
                index += 1
        return SolveResult(False, None, tuple(r.requirement_id for r in core), checked)
