from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


_REQUIRED_SET_FIELDS = (
    "authorized_scope",
    "success_invariants",
    "forbidden_actions",
    "assumptions",
    "required_evidence",
)


def _as_set(contract: Mapping[str, Any], key: str) -> frozenset[str]:
    raw = contract.get(key, ())
    if not isinstance(raw, (list, tuple, set, frozenset)):
        raise ValueError(f"{key} must be a sequence/set of strings")
    values = frozenset(raw)
    if any(not isinstance(item, str) or not item for item in values):
        raise ValueError(f"{key} must contain non-empty strings")
    return values


@dataclass(frozen=True)
class ContractDriftPolicy:
    max_total_cost: int = 3
    block_unapproved_scope_expansion: bool = True
    block_unapproved_invariant_weakening: bool = True
    block_unapproved_forbidden_weakening: bool = True
    block_unapproved_assumption_injection: bool = True
    block_unapproved_evidence_weakening: bool = True

    def __post_init__(self) -> None:
        if self.max_total_cost < 0:
            raise ValueError("max_total_cost must be >= 0")


@dataclass(frozen=True)
class DriftEvent:
    event_id: str
    kind: str
    item: str
    cost: int
    approved: bool


@dataclass(frozen=True)
class ContractDriftReport:
    events: tuple[DriftEvent, ...]
    total_cost: int
    status: str
    reasons: tuple[str, ...]


def analyze_contract_drift(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    approved_event_ids: Iterable[str] = (),
    policy: ContractDriftPolicy = ContractDriftPolicy(),
) -> ContractDriftReport:
    for field in _REQUIRED_SET_FIELDS:
        _as_set(before, field)
        _as_set(after, field)
    approved = frozenset(approved_event_ids)

    events: list[DriftEvent] = []

    def add(kind: str, item: str, cost: int) -> None:
        event_id = f"{kind}:{item}"
        events.append(DriftEvent(event_id, kind, item, cost, event_id in approved))

    b_scope, a_scope = _as_set(before, "authorized_scope"), _as_set(after, "authorized_scope")
    b_inv, a_inv = _as_set(before, "success_invariants"), _as_set(after, "success_invariants")
    b_forbid, a_forbid = _as_set(before, "forbidden_actions"), _as_set(after, "forbidden_actions")
    b_assume, a_assume = _as_set(before, "assumptions"), _as_set(after, "assumptions")
    b_evidence, a_evidence = _as_set(before, "required_evidence"), _as_set(after, "required_evidence")

    for item in sorted(a_scope - b_scope):
        add("scope_expansion", item, 8)
    for item in sorted(b_scope - a_scope):
        add("scope_narrowing", item, 1)
    for item in sorted(b_inv - a_inv):
        add("invariant_removed", item, 10)
    for item in sorted(b_forbid - a_forbid):
        add("forbidden_action_removed", item, 12)
    for item in sorted(a_assume - b_assume):
        add("assumption_added", item, 7)
    for item in sorted(b_evidence - a_evidence):
        add("required_evidence_removed", item, 9)

    reasons: list[str] = []
    for event in events:
        if event.approved:
            continue
        if event.kind == "scope_expansion" and policy.block_unapproved_scope_expansion:
            reasons.append(event.event_id)
        elif event.kind == "invariant_removed" and policy.block_unapproved_invariant_weakening:
            reasons.append(event.event_id)
        elif event.kind == "forbidden_action_removed" and policy.block_unapproved_forbidden_weakening:
            reasons.append(event.event_id)
        elif event.kind == "assumption_added" and policy.block_unapproved_assumption_injection:
            reasons.append(event.event_id)
        elif event.kind == "required_evidence_removed" and policy.block_unapproved_evidence_weakening:
            reasons.append(event.event_id)

    total_cost = sum(event.cost for event in events if not event.approved)
    if total_cost > policy.max_total_cost:
        reasons.append("drift_budget_exceeded")

    # Deterministic dedup while preserving first reason order.
    reasons = list(dict.fromkeys(reasons))
    return ContractDriftReport(
        events=tuple(events),
        total_cost=total_cost,
        status="PASS" if not reasons else "FREEZE",
        reasons=tuple(reasons),
    )
