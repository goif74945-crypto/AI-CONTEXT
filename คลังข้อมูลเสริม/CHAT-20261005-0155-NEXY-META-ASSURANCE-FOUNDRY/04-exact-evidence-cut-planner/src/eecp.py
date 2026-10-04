from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, product
import json
from typing import Iterable, Mapping, Any


class GraphError(ValueError):
    pass


class PlanningLimitExceeded(RuntimeError):
    pass


def _id(value: str, name: str = "id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise GraphError(f"{name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class Evidence:
    node_id: str
    cost: int = 1

    def __post_init__(self) -> None:
        object.__setattr__(self, "node_id", _id(self.node_id, "node_id"))
        if not isinstance(self.cost, int) or self.cost <= 0:
            raise GraphError("evidence cost must be a positive integer")


@dataclass(frozen=True)
class Claim:
    node_id: str
    op: str
    children: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "node_id", _id(self.node_id, "node_id"))
        op = self.op.upper() if isinstance(self.op, str) else ""
        if op not in {"AND", "OR"}:
            raise GraphError("claim op must be AND or OR")
        object.__setattr__(self, "op", op)
        cleaned = tuple(_id(child, "child") for child in self.children)
        if not cleaned:
            raise GraphError("claim must contain at least one child")
        if len(set(cleaned)) != len(cleaned):
            raise GraphError("claim children must be unique")
        object.__setattr__(self, "children", cleaned)


Node = Evidence | Claim


@dataclass(frozen=True)
class AcquisitionPlan:
    status: str
    target: str
    required_new_evidence: tuple[str, ...]
    total_cost: int
    alternative_minimal_sets: tuple[tuple[str, ...], ...]
    fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "target": self.target,
            "required_new_evidence": list(self.required_new_evidence),
            "total_cost": self.total_cost,
            "alternative_minimal_sets": [list(x) for x in self.alternative_minimal_sets],
            "fingerprint": self.fingerprint,
        }


class EvidenceGraph:
    def __init__(self, nodes: Iterable[Node], *, max_frontier: int = 20_000) -> None:
        if not isinstance(max_frontier, int) or max_frontier < 1:
            raise GraphError("max_frontier must be >= 1")
        self.max_frontier = max_frontier
        self.nodes: dict[str, Node] = {}
        for node in nodes:
            if not isinstance(node, (Evidence, Claim)):
                raise GraphError("nodes must be Evidence or Claim")
            if node.node_id in self.nodes:
                raise GraphError(f"duplicate node id: {node.node_id}")
            self.nodes[node.node_id] = node
        if not self.nodes:
            raise GraphError("graph must contain at least one node")
        for node in self.nodes.values():
            if isinstance(node, Claim):
                missing = [child for child in node.children if child not in self.nodes]
                if missing:
                    raise GraphError(f"unknown child nodes for {node.node_id}: {sorted(missing)}")
        self._validate_acyclic()
        self._frontier_cache: dict[str, tuple[frozenset[str], ...]] = {}

    def _validate_acyclic(self) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise GraphError(f"cycle detected at {node_id}")
            if node_id in visited:
                return
            visiting.add(node_id)
            node = self.nodes[node_id]
            if isinstance(node, Claim):
                for child in node.children:
                    visit(child)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in sorted(self.nodes):
            visit(node_id)

    @staticmethod
    def _prune(sets: Iterable[frozenset[str]], max_frontier: int) -> tuple[frozenset[str], ...]:
        unique = sorted(set(sets), key=lambda s: (len(s), tuple(sorted(s))))
        kept: list[frozenset[str]] = []
        for candidate in unique:
            if any(existing <= candidate for existing in kept):
                continue
            kept.append(candidate)
            if len(kept) > max_frontier:
                raise PlanningLimitExceeded("proof frontier exceeded configured bound")
        return tuple(kept)

    def proof_frontier(self, node_id: str) -> tuple[frozenset[str], ...]:
        node_id = _id(node_id, "node_id")
        if node_id not in self.nodes:
            raise GraphError(f"unknown target node: {node_id}")
        if node_id in self._frontier_cache:
            return self._frontier_cache[node_id]
        node = self.nodes[node_id]
        if isinstance(node, Evidence):
            result = (frozenset({node.node_id}),)
        elif node.op == "OR":
            merged = []
            for child in node.children:
                merged.extend(self.proof_frontier(child))
            result = self._prune(merged, self.max_frontier)
        else:
            frontiers = [self.proof_frontier(child) for child in node.children]
            combos = []
            for combo in product(*frontiers):
                merged: frozenset[str] = frozenset().union(*combo)
                combos.append(merged)
                if len(combos) > self.max_frontier * max(2, len(frontiers)):
                    raise PlanningLimitExceeded("intermediate proof frontier exceeded configured bound")
            result = self._prune(combos, self.max_frontier)
        self._frontier_cache[node_id] = result
        return result

    def _costs(self) -> dict[str, int]:
        return {node_id: node.cost for node_id, node in self.nodes.items() if isinstance(node, Evidence)}

    def _canonical_graph(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for node_id in sorted(self.nodes):
            node = self.nodes[node_id]
            if isinstance(node, Evidence):
                rows.append({"id": node.node_id, "kind": "EVIDENCE", "cost": node.cost})
            else:
                rows.append({"id": node.node_id, "kind": "CLAIM", "op": node.op, "children": sorted(node.children)})
        return rows

    def _fingerprint(self, target: str, proven: frozenset[str]) -> str:
        payload = {"graph": self._canonical_graph(), "target": target, "proven": sorted(proven)}
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return sha256(raw).hexdigest()

    def plan_acquisition(self, target: str, proven_evidence: Iterable[str] = ()) -> AcquisitionPlan:
        target = _id(target, "target")
        costs = self._costs()
        proven = frozenset(_id(x, "proven_evidence") for x in proven_evidence)
        unknown_proven = proven - costs.keys()
        if unknown_proven:
            raise GraphError(f"proven_evidence contains non-evidence IDs: {sorted(unknown_proven)}")

        reduced = self._prune((proof - proven for proof in self.proof_frontier(target)), self.max_frontier)
        ranked = sorted(
            reduced,
            key=lambda s: (sum(costs[e] for e in s), len(s), tuple(sorted(s))),
        )
        best = ranked[0]
        return AcquisitionPlan(
            status="ALREADY_PROVEN" if not best else "PLAN",
            target=target,
            required_new_evidence=tuple(sorted(best)),
            total_cost=sum(costs[e] for e in best),
            alternative_minimal_sets=tuple(tuple(sorted(s)) for s in ranked),
            fingerprint=self._fingerprint(target, proven),
        )

    def minimal_cutsets(self, target: str, *, max_enumerations: int = 200_000) -> tuple[tuple[str, ...], ...]:
        if not isinstance(max_enumerations, int) or max_enumerations < 1:
            raise GraphError("max_enumerations must be >= 1")
        proofs = self.proof_frontier(target)
        universe = sorted(set().union(*proofs))
        enumerated = 0
        minimal: list[frozenset[str]] = []
        for size in range(1, len(universe) + 1):
            for combo in combinations(universe, size):
                enumerated += 1
                if enumerated > max_enumerations:
                    raise PlanningLimitExceeded("cutset enumeration exceeded configured bound")
                candidate = frozenset(combo)
                if any(existing <= candidate for existing in minimal):
                    continue
                if all(candidate & proof for proof in proofs):
                    minimal.append(candidate)
        return tuple(tuple(sorted(x)) for x in sorted(minimal, key=lambda s: (len(s), tuple(sorted(s)))))
