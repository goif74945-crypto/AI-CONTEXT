"""Deterministic graph dominator analysis for architectural chokepoints."""
from __future__ import annotations

from collections.abc import Mapping, Sequence


def _normalize_graph(graph: Mapping[str, Sequence[str]]) -> dict[str, tuple[str, ...]]:
    if not isinstance(graph, Mapping) or not graph:
        raise ValueError("graph must be a non-empty mapping")
    nodes: set[str] = set()
    normalized: dict[str, tuple[str, ...]] = {}
    for node, raw_children in graph.items():
        if not isinstance(node, str) or not node:
            raise ValueError("node ids must be non-empty strings")
        if isinstance(raw_children, (str, bytes)):
            raise ValueError("children must be a sequence of node ids")
        children = tuple(sorted(set(raw_children)))
        if any(not isinstance(child, str) or not child for child in children):
            raise ValueError("child ids must be non-empty strings")
        nodes.add(node)
        nodes.update(children)
        normalized[node] = children
    for node in nodes:
        normalized.setdefault(node, ())
    return normalized


def _reachable(graph: dict[str, tuple[str, ...]], start: str) -> frozenset[str]:
    seen: set[str] = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(reversed(graph[node]))
    return frozenset(seen)


def compute_dominators(graph: Mapping[str, Sequence[str]], start: str) -> dict[str, frozenset[str]]:
    """Compute classic graph dominators for nodes reachable from ``start``."""
    normalized = _normalize_graph(graph)
    if start not in normalized:
        raise ValueError("start node is not present in graph")
    reachable = _reachable(normalized, start)
    predecessors: dict[str, set[str]] = {node: set() for node in reachable}
    for source in reachable:
        for target in normalized[source]:
            if target in reachable:
                predecessors[target].add(source)

    dom: dict[str, set[str]] = {
        node: ({start} if node == start else set(reachable)) for node in reachable
    }
    changed = True
    while changed:
        changed = False
        for node in sorted(reachable - {start}):
            preds = predecessors[node]
            if not preds:
                candidate = {node}
            else:
                intersection = set(reachable)
                for pred in sorted(preds):
                    intersection &= dom[pred]
                candidate = {node} | intersection
            if candidate != dom[node]:
                dom[node] = candidate
                changed = True
    return {node: frozenset(dom[node]) for node in sorted(dom)}


def critical_dominators(
    graph: Mapping[str, Sequence[str]], start: str, targets: Sequence[str]
) -> tuple[str, ...]:
    """Return non-trivial nodes that dominate every requested reachable target."""
    if isinstance(targets, (str, bytes)) or not targets:
        raise ValueError("targets must be a non-empty sequence")
    dom = compute_dominators(graph, start)
    unique_targets = tuple(sorted(set(targets)))
    missing = [target for target in unique_targets if target not in dom]
    if missing:
        raise ValueError(f"targets are unreachable or unknown: {missing!r}")
    shared = set(dom[unique_targets[0]])
    for target in unique_targets[1:]:
        shared &= dom[target]
    shared.discard(start)
    shared.difference_update(unique_targets)
    return tuple(sorted(shared))
