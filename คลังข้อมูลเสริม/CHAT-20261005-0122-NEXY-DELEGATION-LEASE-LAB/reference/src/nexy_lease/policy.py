from __future__ import annotations

from dataclasses import replace
from fnmatch import fnmatchcase
from typing import Iterable

from .canonical import plan_fingerprint
from .model import (
    Action,
    AuthorityLease,
    Decision,
    DecisionStatus,
    DriftReport,
    Effect,
    HIGH_IMPACT_EFFECTS,
    LeaseState,
    Plan,
)


POLICY_VERSION = "nexy-lease-ref/0.1"


def _freeze(lease: AuthorityLease, index: int, plan_hash: str, code: str) -> Decision:
    return Decision(
        status=DecisionStatus.FREEZE,
        reason_code=code,
        lease_id=lease.lease_id,
        action_index=index,
        plan_hash=plan_hash,
    )


def diff_plans(granted: Plan, current: Plan) -> DriftReport:
    old_hash = plan_fingerprint(granted)
    new_hash = plan_fingerprint(current)
    if old_hash == new_hash:
        return DriftReport(False, old_hash, new_hash, (), ())

    categories: set[str] = set()
    details: list[str] = []
    if len(granted.actions) != len(current.actions):
        categories.add("ACTION_COUNT")
        details.append(f"action_count:{len(granted.actions)}->{len(current.actions)}")

    for i, (old, new) in enumerate(zip(granted.actions, current.actions)):
        for field in ("resource", "verb", "effect", "destination", "cost_units"):
            old_value = getattr(old, field)
            new_value = getattr(new, field)
            if old_value != new_value:
                categories.add(field.upper())
                ov = old_value.value if isinstance(old_value, Effect) else old_value
                nv = new_value.value if isinstance(new_value, Effect) else new_value
                details.append(f"action[{i}].{field}:{ov!r}->{nv!r}")

    return DriftReport(True, old_hash, new_hash, tuple(sorted(categories)), tuple(details))


def evaluate_action(
    lease: AuthorityLease,
    state: LeaseState,
    current_plan: Plan,
    action_index: int,
    logical_tick: int,
) -> Decision:
    current_hash = plan_fingerprint(current_plan)

    if lease.policy_version != POLICY_VERSION:
        return _freeze(lease, action_index, current_hash, "POLICY_VERSION_MISMATCH")
    if state.revoked:
        return _freeze(lease, action_index, current_hash, "LEASE_REVOKED")
    if logical_tick < lease.issued_at_tick:
        return _freeze(lease, action_index, current_hash, "LEASE_NOT_ACTIVE")
    if logical_tick > lease.expires_at_tick:
        return _freeze(lease, action_index, current_hash, "LEASE_EXPIRED")
    if current_hash != lease.plan_hash:
        return _freeze(lease, action_index, current_hash, "PLAN_HASH_MISMATCH_REAUTHORIZE")
    if action_index < 0 or action_index >= len(current_plan.actions):
        return _freeze(lease, action_index, current_hash, "ACTION_INDEX_INVALID")

    action = current_plan.actions[action_index]
    if not any(fnmatchcase(action.resource, pattern) for pattern in lease.allowed_resource_patterns):
        return _freeze(lease, action_index, current_hash, "RESOURCE_OUT_OF_SCOPE")
    if action.verb not in lease.allowed_verbs:
        return _freeze(lease, action_index, current_hash, "VERB_OUT_OF_SCOPE")
    if action.effect not in lease.allowed_effects:
        return _freeze(lease, action_index, current_hash, "EFFECT_OUT_OF_SCOPE")
    if action.effect in HIGH_IMPACT_EFFECTS and not lease.allow_high_impact:
        return _freeze(lease, action_index, current_hash, "HIGH_IMPACT_NOT_EXPLICITLY_AUTHORIZED")
    if state.used_actions + 1 > lease.max_actions:
        return _freeze(lease, action_index, current_hash, "ACTION_BUDGET_EXCEEDED")
    if state.used_cost_units + action.cost_units > lease.max_cost_units:
        return _freeze(lease, action_index, current_hash, "COST_BUDGET_EXCEEDED")

    return Decision(
        status=DecisionStatus.ALLOW,
        reason_code="LEASE_VALID",
        lease_id=lease.lease_id,
        action_index=action_index,
        plan_hash=current_hash,
    )


def commit_allowed_action(state: LeaseState, action: Action, decision: Decision) -> LeaseState:
    if not decision.allowed:
        raise ValueError("cannot commit a frozen decision")
    if state.revoked:
        raise ValueError("cannot commit against revoked lease state")
    return replace(
        state,
        used_actions=state.used_actions + 1,
        used_cost_units=state.used_cost_units + action.cost_units,
    )


def revoke(state: LeaseState) -> LeaseState:
    return replace(state, revoked=True)


def _contains_wildcard(pattern: str) -> bool:
    return any(ch in pattern for ch in "*?[")


def _resource_scope_is_subset(child_patterns: Iterable[str], parent_patterns: tuple[str, ...]) -> bool:
    for child in child_patterns:
        if child in parent_patterns:
            continue
        if _contains_wildcard(child):
            # Generic glob-subset proofs are surprisingly easy to get wrong.
            # Reference policy therefore rejects novel child globs rather than guessing.
            return False
        if not any(fnmatchcase(child, parent) for parent in parent_patterns):
            return False
    return True


def derive_child_lease(
    parent: AuthorityLease,
    *,
    lease_id: str,
    subject: str,
    allowed_resource_patterns: tuple[str, ...],
    allowed_verbs: tuple[str, ...],
    allowed_effects: tuple[Effect, ...],
    max_cost_units: int,
    max_actions: int,
    issued_at_tick: int,
    expires_at_tick: int,
    plan_hash: str,
    allow_high_impact: bool = False,
) -> AuthorityLease:
    if not _resource_scope_is_subset(allowed_resource_patterns, parent.allowed_resource_patterns):
        raise ValueError("child resource scope is not provably within parent scope")
    if not set(v.upper() for v in allowed_verbs).issubset(set(parent.allowed_verbs)):
        raise ValueError("child verb scope exceeds parent")
    child_effects = tuple(e if isinstance(e, Effect) else Effect(e) for e in allowed_effects)
    if not set(child_effects).issubset(set(parent.allowed_effects)):
        raise ValueError("child effect scope exceeds parent")
    if max_cost_units > parent.max_cost_units:
        raise ValueError("child cost budget exceeds parent")
    if max_actions > parent.max_actions:
        raise ValueError("child action budget exceeds parent")
    if issued_at_tick < parent.issued_at_tick:
        raise ValueError("child begins before parent")
    if expires_at_tick > parent.expires_at_tick:
        raise ValueError("child expires after parent")
    if allow_high_impact and not parent.allow_high_impact:
        raise ValueError("child cannot escalate high-impact authorization")

    return AuthorityLease(
        lease_id=lease_id,
        subject=subject,
        allowed_resource_patterns=allowed_resource_patterns,
        allowed_verbs=allowed_verbs,
        allowed_effects=child_effects,
        max_cost_units=max_cost_units,
        max_actions=max_actions,
        issued_at_tick=issued_at_tick,
        expires_at_tick=expires_at_tick,
        plan_hash=plan_hash,
        policy_version=parent.policy_version,
        allow_high_impact=allow_high_impact,
        parent_lease_id=parent.lease_id,
    )
