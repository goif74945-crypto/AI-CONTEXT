from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable

from human_agency_lab import Decision, InteractionDecision, RequestProfile


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
class CoalescingPolicy:
    """Fail-closed limits for one human-facing interaction batch."""

    policy_id: str = "human-agency/coalescing/v1"
    max_actions: int = 5
    max_attention_cost: int = 8
    sensitive_data_threshold: float = 0.65
    material_cost_threshold: float = 0.50

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if self.max_actions < 1:
            raise ValueError("max_actions must be >= 1")
        if self.max_attention_cost < 0:
            raise ValueError("max_attention_cost must be >= 0")
        for name in ("sensitive_data_threshold", "material_cost_threshold"):
            value = float(getattr(self, name))
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be within [0, 1]")

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "material_cost_threshold": self.material_cost_threshold,
            "max_actions": self.max_actions,
            "max_attention_cost": self.max_attention_cost,
            "policy_id": self.policy_id,
            "sensitive_data_threshold": self.sensitive_data_threshold,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


@dataclass(frozen=True)
class InteractionCandidate:
    """One decision plus identities required to prove batching compatibility."""

    request: RequestProfile
    decision: InteractionDecision
    authority_digest: str
    decision_policy_digest: str
    interaction_context: str

    def __post_init__(self) -> None:
        if self.request.action_id != self.decision.action_id:
            raise ValueError("request and decision action_id must match")
        for name in ("authority_digest", "decision_policy_digest", "interaction_context"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "authority_digest": self.authority_digest,
            "decision": self.decision.canonical_dict(),
            "decision_policy_digest": self.decision_policy_digest,
            "interaction_context": self.interaction_context,
            "request": self.request.canonical_dict(),
        }


@dataclass(frozen=True)
class ActionExplanation:
    action_id: str
    decision: Decision
    reason_codes: tuple[str, ...]
    original_attention_cost: int

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "decision": self.decision.value,
            "original_attention_cost": self.original_attention_cost,
            "reason_codes": list(self.reason_codes),
        }


@dataclass(frozen=True)
class InteractionBatch:
    batch_id: str
    decision: Decision
    action_ids: tuple[str, ...]
    explanations: tuple[ActionExplanation, ...]
    total_attention_cost: int
    authority_digest: str
    decision_policy_digest: str
    interaction_context: str
    isolated: bool
    isolation_reasons: tuple[str, ...]

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "action_ids": list(self.action_ids),
            "authority_digest": self.authority_digest,
            "batch_id": self.batch_id,
            "decision": self.decision.value,
            "decision_policy_digest": self.decision_policy_digest,
            "explanations": [item.canonical_dict() for item in self.explanations],
            "interaction_context": self.interaction_context,
            "isolated": self.isolated,
            "isolation_reasons": list(self.isolation_reasons),
            "total_attention_cost": self.total_attention_cost,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


@dataclass(frozen=True)
class CoalescingMetrics:
    candidate_actions: int
    proceed_actions: int
    interruptions_before: int
    interruptions_after: int
    interruptions_avoided: int
    reduction_ratio: float
    isolated_batches: int

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "candidate_actions": self.candidate_actions,
            "interruptions_after": self.interruptions_after,
            "interruptions_avoided": self.interruptions_avoided,
            "interruptions_before": self.interruptions_before,
            "isolated_batches": self.isolated_batches,
            "proceed_actions": self.proceed_actions,
            "reduction_ratio": self.reduction_ratio,
        }


@dataclass(frozen=True)
class CoalescingPlan:
    batches: tuple[InteractionBatch, ...]
    proceed_action_ids: tuple[str, ...]
    metrics: CoalescingMetrics
    coalescing_policy_digest: str

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "batches": [batch.canonical_dict() for batch in self.batches],
            "coalescing_policy_digest": self.coalescing_policy_digest,
            "metrics": self.metrics.canonical_dict(),
            "proceed_action_ids": list(self.proceed_action_ids),
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


def _isolation_reasons(
    candidate: InteractionCandidate,
    policy: CoalescingPolicy,
) -> tuple[str, ...]:
    request = candidate.request
    reasons: list[str] = []
    if candidate.decision.decision is Decision.FREEZE:
        reasons.append("FREEZE_ISOLATED")
    if request.destructive:
        reasons.append("DESTRUCTIVE_BOUNDARY")
    if request.crosses_auth_boundary:
        reasons.append("AUTH_BOUNDARY")
    if request.external_side_effect:
        reasons.append("EXTERNAL_EFFECT_BOUNDARY")
    if request.data_sensitivity >= policy.sensitive_data_threshold:
        reasons.append("SENSITIVE_DATA_BOUNDARY")
    if request.monetary_cost >= policy.material_cost_threshold:
        reasons.append("MATERIAL_COST_BOUNDARY")
    if candidate.decision.attention_cost > policy.max_attention_cost:
        reasons.append("ATTENTION_COST_EXCEEDS_BATCH_LIMIT")
    return tuple(sorted(set(reasons)))


def _compatibility_key(candidate: InteractionCandidate) -> tuple[str, ...]:
    return (
        candidate.decision.decision.value,
        candidate.authority_digest,
        candidate.decision_policy_digest,
        candidate.interaction_context,
    )


def _explanation(candidate: InteractionCandidate) -> ActionExplanation:
    return ActionExplanation(
        action_id=candidate.request.action_id,
        decision=candidate.decision.decision,
        reason_codes=tuple(reason.value for reason in candidate.decision.reasons),
        original_attention_cost=candidate.decision.attention_cost,
    )


def _build_batch(
    candidates: tuple[InteractionCandidate, ...],
    *,
    policy_digest: str,
    isolated: bool,
    isolation_reasons: tuple[str, ...] = tuple(),
) -> InteractionBatch:
    first = candidates[0]
    action_ids = tuple(item.request.action_id for item in candidates)
    identity = {
        "action_ids": list(action_ids),
        "authority_digest": first.authority_digest,
        "coalescing_policy_digest": policy_digest,
        "decision": first.decision.decision.value,
        "decision_policy_digest": first.decision_policy_digest,
        "interaction_context": first.interaction_context,
        "isolated": isolated,
        "isolation_reasons": list(isolation_reasons),
    }
    return InteractionBatch(
        batch_id=_digest(identity),
        decision=first.decision.decision,
        action_ids=action_ids,
        explanations=tuple(_explanation(item) for item in candidates),
        total_attention_cost=sum(item.decision.attention_cost for item in candidates),
        authority_digest=first.authority_digest,
        decision_policy_digest=first.decision_policy_digest,
        interaction_context=first.interaction_context,
        isolated=isolated,
        isolation_reasons=isolation_reasons,
    )


def coalesce_interactions(
    candidates: Iterable[InteractionCandidate],
    policy: CoalescingPolicy | None = None,
) -> CoalescingPlan:
    """Produce deterministic batches without weakening or merging hard boundaries.

    The function reduces presentation interruptions only. It preserves every action's
    decision, reasons, and original attention cost; it never changes execution authority.
    """

    policy = policy or CoalescingPolicy()
    policy_digest = policy.digest()
    items = sorted(tuple(candidates), key=lambda item: item.request.action_id)
    action_ids = [item.request.action_id for item in items]
    if len(action_ids) != len(set(action_ids)):
        raise ValueError("duplicate action_id in candidates")

    proceed = tuple(
        item.request.action_id
        for item in items
        if item.decision.decision is Decision.PROCEED
    )
    interrupting = tuple(
        item for item in items if item.decision.decision is not Decision.PROCEED
    )

    batches: list[InteractionBatch] = []
    compatible: dict[tuple[str, ...], list[InteractionCandidate]] = {}
    for item in interrupting:
        isolation_reasons = _isolation_reasons(item, policy)
        if isolation_reasons:
            batches.append(
                _build_batch(
                    (item,),
                    policy_digest=policy_digest,
                    isolated=True,
                    isolation_reasons=isolation_reasons,
                )
            )
            continue
        compatible.setdefault(_compatibility_key(item), []).append(item)

    for key in sorted(compatible):
        group = compatible[key]
        current: list[InteractionCandidate] = []
        current_cost = 0
        for item in group:
            item_cost = item.decision.attention_cost
            exceeds_count = len(current) >= policy.max_actions
            exceeds_cost = bool(current) and current_cost + item_cost > policy.max_attention_cost
            if exceeds_count or exceeds_cost:
                batches.append(
                    _build_batch(tuple(current), policy_digest=policy_digest, isolated=False)
                )
                current = []
                current_cost = 0
            current.append(item)
            current_cost += item_cost
        if current:
            batches.append(
                _build_batch(tuple(current), policy_digest=policy_digest, isolated=False)
            )

    batches.sort(key=lambda batch: (batch.action_ids[0], batch.batch_id))
    before = len(interrupting)
    after = len(batches)
    avoided = before - after
    metrics = CoalescingMetrics(
        candidate_actions=len(items),
        proceed_actions=len(proceed),
        interruptions_before=before,
        interruptions_after=after,
        interruptions_avoided=avoided,
        reduction_ratio=0.0 if before == 0 else avoided / before,
        isolated_batches=sum(batch.isolated for batch in batches),
    )
    return CoalescingPlan(
        batches=tuple(batches),
        proceed_action_ids=proceed,
        metrics=metrics,
        coalescing_policy_digest=policy_digest,
    )
