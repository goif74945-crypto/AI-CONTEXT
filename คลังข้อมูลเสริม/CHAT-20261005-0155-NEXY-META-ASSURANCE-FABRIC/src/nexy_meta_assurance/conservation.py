from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class ConservationError(ValueError):
    """Raised when a conservation rule or state is incomplete or malformed."""


@dataclass(frozen=True)
class ConservationRule:
    name: str
    keys: tuple[str, ...]


@dataclass(frozen=True)
class ConservationResult:
    rule: str
    passed: bool
    before_total: int
    after_total: int
    declared_external_delta: int
    residual: int
    reason: str


def _validate_rule(rule: ConservationRule) -> None:
    if not rule.name.strip():
        raise ConservationError("rule name must be non-empty")
    if not rule.keys:
        raise ConservationError("rule must include at least one key")
    if len(set(rule.keys)) != len(rule.keys):
        raise ConservationError("rule keys must be unique")
    if any(not key.strip() for key in rule.keys):
        raise ConservationError("rule keys must be non-empty")


def _state_total(state: Mapping[str, int], rule: ConservationRule, label: str) -> int:
    missing = [key for key in rule.keys if key not in state]
    if missing:
        raise ConservationError(f"{label} missing required keys: {', '.join(sorted(missing))}")
    total = 0
    for key in rule.keys:
        value = state[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ConservationError(f"{label}.{key} must be an integer")
        total += value
    return total


def verify_transition(
    before: Mapping[str, int],
    after: Mapping[str, int],
    rule: ConservationRule,
    *,
    declared_external_delta: int = 0,
) -> ConservationResult:
    _validate_rule(rule)
    if isinstance(declared_external_delta, bool) or not isinstance(declared_external_delta, int):
        raise ConservationError("declared_external_delta must be an integer")

    before_total = _state_total(before, rule, "before")
    after_total = _state_total(after, rule, "after")
    residual = after_total - before_total - declared_external_delta
    passed = residual == 0
    reason = (
        "conservation satisfied"
        if passed
        else f"undeclared net change detected: residual={residual}"
    )
    return ConservationResult(
        rule=rule.name,
        passed=passed,
        before_total=before_total,
        after_total=after_total,
        declared_external_delta=declared_external_delta,
        residual=residual,
        reason=reason,
    )


def verify_sequence(
    states: Sequence[Mapping[str, int]],
    rule: ConservationRule,
    *,
    declared_external_deltas: Sequence[int] | None = None,
) -> tuple[ConservationResult, ...]:
    _validate_rule(rule)
    if len(states) < 2:
        raise ConservationError("sequence requires at least two states")
    if declared_external_deltas is None:
        declared_external_deltas = [0] * (len(states) - 1)
    if len(declared_external_deltas) != len(states) - 1:
        raise ConservationError("declared_external_deltas length must equal transition count")
    return tuple(
        verify_transition(
            states[index],
            states[index + 1],
            rule,
            declared_external_delta=declared_external_deltas[index],
        )
        for index in range(len(states) - 1)
    )
