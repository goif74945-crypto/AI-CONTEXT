from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

from authority_provenance import (
    AuthorityRef,
    GovernedDecision,
    PolicyEnvelope,
    evaluate_governed,
)
from human_agency_lab import Decision, RecoveryLevel, RecoveryPlan, RequestProfile, plan_recovery


_DECISION_RANK = {
    Decision.PROCEED: 0,
    Decision.PREVIEW: 1,
    Decision.CONFIRM: 2,
    Decision.FREEZE: 3,
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
class TransactionNode:
    node_id: str
    request: RequestProfile
    depends_on: tuple[str, ...] = tuple()

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError("node_id must be non-empty")
        if self.node_id in self.depends_on:
            raise ValueError("node cannot depend on itself")
        if len(set(self.depends_on)) != len(self.depends_on):
            raise ValueError("duplicate dependency in node")

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "depends_on": sorted(self.depends_on),
            "node_id": self.node_id,
            "request": self.request.canonical_dict(),
        }


@dataclass(frozen=True)
class TransactionPlan:
    transaction_id: str
    nodes: tuple[TransactionNode, ...]

    def __post_init__(self) -> None:
        if not self.transaction_id.strip():
            raise ValueError("transaction_id must be non-empty")
        if not self.nodes:
            raise ValueError("transaction must contain at least one node")
        ids = [node.node_id for node in self.nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate node_id in transaction")
        known = set(ids)
        unknown = sorted(
            {
                dependency
                for node in self.nodes
                for dependency in node.depends_on
                if dependency not in known
            }
        )
        if unknown:
            raise ValueError(f"unknown dependencies: {unknown}")
        self.topological_order()

    def topological_order(self) -> tuple[str, ...]:
        by_id = {node.node_id: node for node in self.nodes}
        indegree = {node_id: 0 for node_id in by_id}
        children: dict[str, list[str]] = {node_id: [] for node_id in by_id}
        for node in self.nodes:
            for dependency in node.depends_on:
                indegree[node.node_id] += 1
                children[dependency].append(node.node_id)
        ready = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
        order: list[str] = []
        while ready:
            current = ready.pop(0)
            order.append(current)
            for child in sorted(children[current]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
                    ready.sort()
        if len(order) != len(by_id):
            raise ValueError("transaction dependency graph contains a cycle")
        return tuple(order)

    def canonical_dict(self) -> dict[str, Any]:
        by_id = {node.node_id: node for node in self.nodes}
        return {
            "nodes": [by_id[node_id].canonical_dict() for node_id in self.topological_order()],
            "transaction_id": self.transaction_id,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


@dataclass(frozen=True)
class NodeEvaluation:
    node_id: str
    governed: GovernedDecision
    recovery: RecoveryPlan

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "governed": self.governed.canonical_dict(),
            "node_id": self.node_id,
            "recovery": {
                "level": self.recovery.level.value,
                "required_steps": list(self.recovery.required_steps),
            },
        }


@dataclass(frozen=True)
class RecoveryGroups:
    blocked: tuple[str, ...]
    rollback_required: tuple[str, ...]
    checkpoint_required: tuple[str, ...]

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "blocked": list(self.blocked),
            "checkpoint_required": list(self.checkpoint_required),
            "rollback_required": list(self.rollback_required),
        }


@dataclass(frozen=True)
class TransactionEvaluation:
    transaction_id: str
    overall_decision: Decision
    topological_order: tuple[str, ...]
    nodes: tuple[NodeEvaluation, ...]
    recovery_groups: RecoveryGroups
    plan_digest: str
    policy_digest: str

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "nodes": [node.canonical_dict() for node in self.nodes],
            "overall_decision": self.overall_decision.value,
            "plan_digest": self.plan_digest,
            "policy_digest": self.policy_digest,
            "recovery_groups": self.recovery_groups.canonical_dict(),
            "topological_order": list(self.topological_order),
            "transaction_id": self.transaction_id,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


def evaluate_transaction(
    plan: TransactionPlan,
    *,
    authorities: Mapping[str, AuthorityRef | None],
    revision: int,
    policy: PolicyEnvelope,
) -> TransactionEvaluation:
    by_id = {node.node_id: node for node in plan.nodes}
    order = plan.topological_order()
    evaluations: list[NodeEvaluation] = []

    for node_id in order:
        node = by_id[node_id]
        governed = evaluate_governed(
            node.request,
            authority=authorities.get(node_id),
            revision=revision,
            policy=policy,
        )
        evaluations.append(
            NodeEvaluation(
                node_id=node_id,
                governed=governed,
                recovery=plan_recovery(node.request),
            )
        )

    overall = max(
        (item.governed.decision.decision for item in evaluations),
        key=_DECISION_RANK.__getitem__,
    )
    blocked = tuple(
        item.node_id
        for item in evaluations
        if item.recovery.level is RecoveryLevel.BLOCKED
    )
    rollback_required = tuple(
        item.node_id
        for item in evaluations
        if item.recovery.level is RecoveryLevel.ROLLBACK_REQUIRED
    )
    checkpoint_required = tuple(
        item.node_id
        for item in evaluations
        if item.recovery.level is RecoveryLevel.CHECKPOINT
    )

    return TransactionEvaluation(
        transaction_id=plan.transaction_id,
        overall_decision=overall,
        topological_order=order,
        nodes=tuple(evaluations),
        recovery_groups=RecoveryGroups(
            blocked=blocked,
            rollback_required=rollback_required,
            checkpoint_required=checkpoint_required,
        ),
        plan_digest=plan.digest(),
        policy_digest=policy.digest(),
    )
