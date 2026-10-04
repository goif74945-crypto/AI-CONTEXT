from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping

from .canonical import fingerprint


class FailureAlgebraError(ValueError):
    pass


class Status(str, Enum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"
    FREEZE = "FREEZE"
    FAIL = "FAIL"
    CONFLICT = "CONFLICT"


DEFAULT_PRECEDENCE: Mapping[Status, int] = {
    Status.PASS: 0,
    Status.PARTIAL: 1,
    Status.NOT_VERIFIED: 2,
    Status.UNKNOWN: 3,
    Status.BLOCKED: 4,
    Status.FREEZE: 5,
    Status.FAIL: 6,
    Status.CONFLICT: 7,
}


@dataclass(frozen=True, slots=True)
class AggregateResult:
    status: Status
    member_statuses: tuple[Status, ...]
    reason_codes: tuple[str, ...]
    aggregate_fingerprint: str


def join_statuses(
    statuses: Iterable[Status],
    *,
    precedence: Mapping[Status, int] = DEFAULT_PRECEDENCE,
) -> AggregateResult:
    members = tuple(statuses)
    if not members:
        raise FailureAlgebraError("at least one status is required")
    missing = set(Status) - set(precedence)
    if missing:
        raise FailureAlgebraError(f"precedence missing statuses: {sorted(s.value for s in missing)}")
    ranks = list(precedence.values())
    if len(ranks) != len(set(ranks)):
        raise FailureAlgebraError("precedence ranks must be unique")

    dominant = max(members, key=lambda status: precedence[status])
    normalized_members = tuple(sorted(set(members), key=lambda status: (precedence[status], status.value)))
    reasons = tuple(f"HAS_{status.value}" for status in normalized_members if status != Status.PASS)
    if not reasons:
        reasons = ("ALL_REQUIRED_INPUTS_PASS",)
    payload = {
        "status": dominant.value,
        "member_statuses": [status.value for status in normalized_members],
        "reason_codes": list(reasons),
    }
    return AggregateResult(
        status=dominant,
        member_statuses=normalized_members,
        reason_codes=reasons,
        aggregate_fingerprint=fingerprint(payload),
    )


def gate_required_dependencies(
    own_status: Status,
    dependency_statuses: Iterable[Status],
    *,
    precedence: Mapping[Status, int] = DEFAULT_PRECEDENCE,
) -> AggregateResult:
    deps = tuple(dependency_statuses)
    if not deps:
        return join_statuses((own_status,), precedence=precedence)
    dep_join = join_statuses(deps, precedence=precedence)
    if dep_join.status == Status.PASS:
        return join_statuses((own_status,), precedence=precedence)
    if own_status == Status.PASS:
        # The node itself is locally clean, but the required dependency contract prevents legal completion.
        return join_statuses((Status.BLOCKED, dep_join.status), precedence=precedence)
    return join_statuses((own_status, dep_join.status), precedence=precedence)
