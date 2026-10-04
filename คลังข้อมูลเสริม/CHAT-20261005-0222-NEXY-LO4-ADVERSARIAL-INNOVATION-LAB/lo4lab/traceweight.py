from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping


@dataclass(frozen=True)
class InfluenceNode:
    node_id: str
    parents: Mapping[str, float]
    is_agent_source: bool = False
    verified: bool = False

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("node_id must be non-empty")
        if self.is_agent_source and self.parents:
            raise ValueError("agent source nodes cannot have parents")
        for parent, weight in self.parents.items():
            if not parent:
                raise ValueError("parent ids must be non-empty")
            if not isfinite(weight) or weight <= 0:
                raise ValueError("influence weights must be finite and > 0")


@dataclass(frozen=True)
class InfluenceReport:
    target_id: str
    source_influence: tuple[tuple[str, float], ...]
    dominant_source: str
    dominance_ratio: float
    effective_source_count: float
    unverified_influence: float
    status: str
    reasons: tuple[str, ...]


class InfluenceGraph:
    def __init__(self, nodes: list[InfluenceNode] | tuple[InfluenceNode, ...]):
        if not nodes:
            raise ValueError("at least one node is required")
        self._nodes = {node.node_id: node for node in nodes}
        if len(self._nodes) != len(nodes):
            raise ValueError("node_id values must be unique")
        for node in nodes:
            missing = set(node.parents) - set(self._nodes)
            if missing:
                raise ValueError(f"missing parent nodes for {node.node_id}: {sorted(missing)}")

    def _contributions(self, node_id: str, visiting: set[str], memo: dict[str, dict[str, float]]) -> dict[str, float]:
        if node_id in memo:
            return memo[node_id]
        if node_id in visiting:
            raise ValueError(f"cycle detected at {node_id}")
        node = self._nodes[node_id]
        if node.is_agent_source:
            memo[node_id] = {node_id: 1.0}
            return memo[node_id]
        if not node.parents:
            raise ValueError(f"non-source node {node_id} has no parents")

        visiting.add(node_id)
        total_edge_weight = sum(node.parents.values())
        out: dict[str, float] = {}
        for parent_id, edge_weight in sorted(node.parents.items()):
            parent_factor = edge_weight / total_edge_weight
            for source, influence in self._contributions(parent_id, visiting, memo).items():
                out[source] = out.get(source, 0.0) + parent_factor * influence
        visiting.remove(node_id)
        memo[node_id] = out
        return out

    def analyze(
        self,
        target_id: str,
        *,
        max_dominance_ratio: float = 0.70,
        max_unverified_influence: float = 0.10,
    ) -> InfluenceReport:
        if target_id not in self._nodes:
            raise ValueError("unknown target_id")
        if not (0.0 <= max_dominance_ratio <= 1.0):
            raise ValueError("max_dominance_ratio must be within [0, 1]")
        if not (0.0 <= max_unverified_influence <= 1.0):
            raise ValueError("max_unverified_influence must be within [0, 1]")

        contrib = self._contributions(target_id, set(), {})
        if not contrib:
            raise ValueError("target has no agent-source ancestry")
        total = sum(contrib.values())
        normalized = {k: v / total for k, v in contrib.items()}
        ordered = tuple(sorted(normalized.items(), key=lambda kv: (-kv[1], kv[0])))
        dominant_source, dominance = ordered[0]
        concentration = sum(v * v for _, v in ordered)
        effective_count = 1.0 / concentration
        unverified = sum(
            v for source, v in ordered if not self._nodes[source].verified
        )

        reasons: list[str] = []
        if dominance > max_dominance_ratio:
            reasons.append("single_source_dominance")
        if unverified > max_unverified_influence:
            reasons.append("unverified_influence_exceeded")

        return InfluenceReport(
            target_id=target_id,
            source_influence=ordered,
            dominant_source=dominant_source,
            dominance_ratio=dominance,
            effective_source_count=effective_count,
            unverified_influence=unverified,
            status="PASS" if not reasons else "FREEZE",
            reasons=tuple(reasons),
        )
