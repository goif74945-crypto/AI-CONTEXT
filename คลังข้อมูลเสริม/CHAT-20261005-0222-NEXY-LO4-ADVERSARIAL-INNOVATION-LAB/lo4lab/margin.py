from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Iterable


class Operator(str, Enum):
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    EQ = "=="


def _d(value: Decimal | int | str | float) -> Decimal:
    try:
        d = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid decimal value: {value!r}") from exc
    if not d.is_finite():
        raise ValueError("decimal values must be finite")
    return d


@dataclass(frozen=True)
class Constraint:
    name: str
    actual: Decimal | int | str | float
    operator: Operator
    limit: Decimal | int | str | float
    scale: Decimal | int | str | float = Decimal("1")
    required_margin: Decimal | int | str | float = Decimal("0")

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("constraint name must be non-empty")
        actual = _d(self.actual)
        limit = _d(self.limit)
        scale = _d(self.scale)
        required = _d(self.required_margin)
        if scale <= 0:
            raise ValueError("scale must be > 0")
        if required < 0:
            raise ValueError("required_margin must be >= 0")
        object.__setattr__(self, "actual", actual)
        object.__setattr__(self, "limit", limit)
        object.__setattr__(self, "scale", scale)
        object.__setattr__(self, "required_margin", required)


@dataclass(frozen=True)
class ConstraintResult:
    name: str
    legal: bool
    raw_slack: Decimal
    normalized_margin: Decimal
    status: str


@dataclass(frozen=True)
class DecisionMarginReport:
    results: tuple[ConstraintResult, ...]
    minimum_margin: Decimal
    release_status: str
    reasons: tuple[str, ...]


def _evaluate_one(c: Constraint) -> ConstraintResult:
    a = c.actual
    b = c.limit
    if c.operator is Operator.LE:
        legal, slack = a <= b, b - a
    elif c.operator is Operator.LT:
        legal, slack = a < b, b - a
    elif c.operator is Operator.GE:
        legal, slack = a >= b, a - b
    elif c.operator is Operator.GT:
        legal, slack = a > b, a - b
    else:
        legal, slack = a == b, Decimal("0") if a == b else -abs(a - b)

    margin = slack / c.scale
    if not legal:
        status = "VIOLATION"
    elif margin < c.required_margin:
        status = "FRAGILE_PASS"
    else:
        status = "ROBUST_PASS"
    return ConstraintResult(c.name, legal, slack, margin, status)


def evaluate_constraints(constraints: Iterable[Constraint]) -> DecisionMarginReport:
    data = tuple(constraints)
    if not data:
        raise ValueError("at least one constraint is required")
    names = [c.name for c in data]
    if len(names) != len(set(names)):
        raise ValueError("constraint names must be unique")

    results = tuple(_evaluate_one(c) for c in data)
    min_margin = min(r.normalized_margin for r in results)
    reasons: list[str] = []
    if any(r.status == "VIOLATION" for r in results):
        release_status = "FREEZE"
        reasons.extend(f"violation:{r.name}" for r in results if r.status == "VIOLATION")
    elif any(r.status == "FRAGILE_PASS" for r in results):
        release_status = "REVERIFY"
        reasons.extend(f"fragile:{r.name}" for r in results if r.status == "FRAGILE_PASS")
    else:
        release_status = "RELEASE"
    return DecisionMarginReport(results, min_margin, release_status, tuple(reasons))
