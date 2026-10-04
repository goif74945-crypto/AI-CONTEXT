from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Status = Literal["PASS", "PARTIAL", "FAIL", "FREEZE"]
Operator = Literal["min", "max", "eq", "range", "in"]


@dataclass(frozen=True, slots=True)
class Criterion:
    criterion_id: str
    path: str
    op: Operator
    value: Any
    hard: bool
    weight: float
    regression_guard: bool
    max_regression: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.criterion_id,
            "path": self.path,
            "op": self.op,
            "value": self.value,
            "hard": self.hard,
            "weight": self.weight,
            "regression_guard": self.regression_guard,
            "max_regression": self.max_regression,
        }


@dataclass(frozen=True, slots=True)
class ForbiddenEffect:
    effect_id: str
    path: str
    op: Operator
    value: Any

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.effect_id, "path": self.path, "op": self.op, "value": self.value}


@dataclass(frozen=True, slots=True)
class OutcomeContract:
    contract_version: str
    objective_id: str
    objective: str
    criteria: tuple[Criterion, ...]
    forbidden_effects: tuple[ForbiddenEffect, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_version": self.contract_version,
            "objective_id": self.objective_id,
            "objective": self.objective,
            "criteria": [item.to_dict() for item in self.criteria],
            "forbidden_effects": [item.to_dict() for item in self.forbidden_effects],
        }


@dataclass(frozen=True, slots=True)
class CriterionResult:
    criterion_id: str
    path: str
    hard: bool
    satisfied: bool
    actual: Any
    expected: Any
    margin: float | None
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "criterion_id": self.criterion_id,
            "path": self.path,
            "hard": self.hard,
            "satisfied": self.satisfied,
            "actual": self.actual,
            "expected": self.expected,
            "margin": self.margin,
            "reason": self.reason,
        }
