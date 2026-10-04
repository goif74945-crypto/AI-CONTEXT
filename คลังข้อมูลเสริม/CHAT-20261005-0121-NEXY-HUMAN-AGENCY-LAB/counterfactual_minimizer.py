from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
from itertools import combinations
import json
from typing import Any

from human_agency_lab import AgencyDecisionEngine, AgencyPolicy, Decision, RequestProfile


_DECISION_RANK = {
    Decision.PROCEED: 0,
    Decision.PREVIEW: 1,
    Decision.CONFIRM: 2,
    Decision.FREEZE: 3,
}


class InterventionKind(str, Enum):
    RESOLVE_AMBIGUITY = "RESOLVE_AMBIGUITY"
    IMPROVE_CONFIDENCE = "IMPROVE_CONFIDENCE"
    REDUCE_SCOPE = "REDUCE_SCOPE"
    ADD_ROLLBACK = "ADD_ROLLBACK"
    REDACT_SENSITIVE_DATA = "REDACT_SENSITIVE_DATA"
    ISOLATE_EXTERNAL_EFFECT = "ISOLATE_EXTERNAL_EFFECT"
    REMOVE_MATERIAL_COST = "REMOVE_MATERIAL_COST"
    USE_REVERSIBLE_ALTERNATIVE = "USE_REVERSIBLE_ALTERNATIVE"


_INTERVENTION_COST = {
    InterventionKind.RESOLVE_AMBIGUITY: 1,
    InterventionKind.IMPROVE_CONFIDENCE: 1,
    InterventionKind.REDUCE_SCOPE: 2,
    InterventionKind.ADD_ROLLBACK: 2,
    InterventionKind.REDACT_SENSITIVE_DATA: 2,
    InterventionKind.ISOLATE_EXTERNAL_EFFECT: 3,
    InterventionKind.REMOVE_MATERIAL_COST: 3,
    InterventionKind.USE_REVERSIBLE_ALTERNATIVE: 4,
}


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class CounterfactualCapabilities:
    can_resolve_ambiguity: bool = False
    can_improve_confidence: bool = False
    can_reduce_scope: bool = False
    can_build_rollback: bool = False
    can_redact_data: bool = False
    can_isolate_external_effect: bool = False
    can_remove_material_cost: bool = False
    can_use_reversible_alternative: bool = False

    def allowed(self) -> tuple[InterventionKind, ...]:
        pairs = (
            (self.can_resolve_ambiguity, InterventionKind.RESOLVE_AMBIGUITY),
            (self.can_improve_confidence, InterventionKind.IMPROVE_CONFIDENCE),
            (self.can_reduce_scope, InterventionKind.REDUCE_SCOPE),
            (self.can_build_rollback, InterventionKind.ADD_ROLLBACK),
            (self.can_redact_data, InterventionKind.REDACT_SENSITIVE_DATA),
            (
                self.can_isolate_external_effect,
                InterventionKind.ISOLATE_EXTERNAL_EFFECT,
            ),
            (self.can_remove_material_cost, InterventionKind.REMOVE_MATERIAL_COST),
            (
                self.can_use_reversible_alternative,
                InterventionKind.USE_REVERSIBLE_ALTERNATIVE,
            ),
        )
        return tuple(sorted((kind for enabled, kind in pairs if enabled), key=lambda k: k.value))


@dataclass(frozen=True)
class CounterfactualPlan:
    original_decision: Decision
    target_decision: Decision
    achieved_decision: Decision
    interventions: tuple[InterventionKind, ...]
    modified_request: RequestProfile
    total_cost: int

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "achieved_decision": self.achieved_decision.value,
            "interventions": [kind.value for kind in self.interventions],
            "modified_request": self.modified_request.canonical_dict(),
            "original_decision": self.original_decision.value,
            "target_decision": self.target_decision.value,
            "total_cost": self.total_cost,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


def _apply_intervention(
    request: RequestProfile,
    kind: InterventionKind,
    policy: AgencyPolicy,
) -> RequestProfile:
    if kind is InterventionKind.RESOLVE_AMBIGUITY:
        return replace(request, ambiguity=0.0)
    if kind is InterventionKind.IMPROVE_CONFIDENCE:
        return replace(request, confidence=1.0)
    if kind is InterventionKind.REDUCE_SCOPE:
        safe_scope = min(
            request.scope_breadth,
            max(0.0, min(policy.high_impact_scope, policy.broad_scope) - 0.01),
        )
        return replace(request, scope_breadth=safe_scope)
    if kind is InterventionKind.ADD_ROLLBACK:
        return replace(
            request,
            rollback_available=True,
            reversibility=max(request.reversibility, min(1.0, policy.low_reversibility + 0.01)),
        )
    if kind is InterventionKind.REDACT_SENSITIVE_DATA:
        return replace(request, data_sensitivity=0.0)
    if kind is InterventionKind.ISOLATE_EXTERNAL_EFFECT:
        return replace(request, external_side_effect=False)
    if kind is InterventionKind.REMOVE_MATERIAL_COST:
        return replace(request, monetary_cost=0.0)
    if kind is InterventionKind.USE_REVERSIBLE_ALTERNATIVE:
        return replace(
            request,
            destructive=False,
            rollback_available=True,
            reversibility=max(request.reversibility, min(1.0, policy.low_reversibility + 0.01)),
        )
    raise AssertionError(f"unsupported intervention: {kind}")


def _apply_set(
    request: RequestProfile,
    kinds: tuple[InterventionKind, ...],
    policy: AgencyPolicy,
) -> RequestProfile:
    current = request
    for kind in sorted(kinds, key=lambda item: item.value):
        current = _apply_intervention(current, kind, policy)
    return current


def minimize_gate(
    request: RequestProfile,
    *,
    target: Decision,
    capabilities: CounterfactualCapabilities,
    policy: AgencyPolicy | None = None,
    max_steps: int = 3,
) -> CounterfactualPlan | None:
    if max_steps < 0:
        raise ValueError("max_steps must be >= 0")
    policy = policy or AgencyPolicy()
    engine = AgencyDecisionEngine(policy)
    original = engine.evaluate(request).decision

    if _DECISION_RANK[original] <= _DECISION_RANK[target]:
        return CounterfactualPlan(
            original_decision=original,
            target_decision=target,
            achieved_decision=original,
            interventions=tuple(),
            modified_request=request,
            total_cost=0,
        )

    allowed = capabilities.allowed()
    candidates: list[tuple[tuple[int, int, tuple[str, ...]], CounterfactualPlan]] = []
    for size in range(1, min(max_steps, len(allowed)) + 1):
        for kinds in combinations(allowed, size):
            modified = _apply_set(request, kinds, policy)
            if modified == request:
                continue
            achieved = engine.evaluate(modified).decision
            if _DECISION_RANK[achieved] > _DECISION_RANK[target]:
                continue
            total_cost = sum(_INTERVENTION_COST[kind] for kind in kinds)
            score = (
                total_cost,
                len(kinds),
                tuple(kind.value for kind in kinds),
            )
            candidates.append(
                (
                    score,
                    CounterfactualPlan(
                        original_decision=original,
                        target_decision=target,
                        achieved_decision=achieved,
                        interventions=kinds,
                        modified_request=modified,
                        total_cost=total_cost,
                    ),
                )
            )

    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0])
    return candidates[0][1]
