"""Workflow liveness analysis with deterministic deadlock classification."""
from __future__ import annotations

from collections.abc import Iterable

_ALLOWED_STATES = frozenset({"READY", "RUNNING", "WAITING", "PASS", "FAIL", "BLOCKED"})
_TERMINAL_STATES = frozenset({"PASS", "FAIL"})


def _scc_cycles(graph: dict[str, tuple[str, ...]]) -> tuple[tuple[str, ...], ...]:
    """Return cyclic SCCs using iterative Kosaraju traversal.

    Iterative traversal avoids coupling workflow size to the Python recursion
    limit, which is critical for large orchestration graphs.
    """
    visited: set[str] = set()
    finish_order: list[str] = []

    for root in sorted(graph):
        if root in visited:
            continue
        stack: list[tuple[str, bool]] = [(root, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                finish_order.append(node)
                continue
            if node in visited:
                continue
            visited.add(node)
            stack.append((node, True))
            for nxt in reversed(graph[node]):
                if nxt not in visited:
                    stack.append((nxt, False))

    reverse_graph: dict[str, list[str]] = {node: [] for node in graph}
    for source, targets in graph.items():
        for target in targets:
            reverse_graph[target].append(source)
    for node in reverse_graph:
        reverse_graph[node].sort()

    assigned: set[str] = set()
    cycles: list[tuple[str, ...]] = []
    for root in reversed(finish_order):
        if root in assigned:
            continue
        component: list[str] = []
        stack = [root]
        assigned.add(root)
        while stack:
            node = stack.pop()
            component.append(node)
            for nxt in reversed(reverse_graph[node]):
                if nxt not in assigned:
                    assigned.add(nxt)
                    stack.append(nxt)
        members = tuple(sorted(component))
        if len(members) > 1 or (members and members[0] in graph[members[0]]):
            cycles.append(members)

    return tuple(sorted(cycles))


def analyze_liveness(items: Iterable[dict]) -> dict:
    """Classify a bounded workflow snapshot.

    DEADLOCK means a non-terminal dependency cycle is present.
    PROGRESSABLE means at least one READY/RUNNING item exists and no deadlock.
    QUIESCENT means every item is terminal.
    STARVATION_RISK is a non-terminal acyclic stall with no runnable item.
    """
    materialized = list(items)
    if not materialized:
        raise ValueError("at least one work item is required")

    by_id: dict[str, dict] = {}
    for item in materialized:
        if not isinstance(item, dict):
            raise ValueError("each item must be a mapping")
        item_id = item.get("id")
        state = item.get("state")
        waits_for = item.get("waits_for", [])
        if not isinstance(item_id, str) or not item_id:
            raise ValueError("item id must be a non-empty string")
        if item_id in by_id:
            raise ValueError(f"duplicate item id: {item_id}")
        if state not in _ALLOWED_STATES:
            raise ValueError(f"unknown state for {item_id}: {state!r}")
        if not isinstance(waits_for, list) or any(not isinstance(x, str) or not x for x in waits_for):
            raise ValueError(f"waits_for for {item_id} must be a list of non-empty ids")
        by_id[item_id] = {"state": state, "waits_for": tuple(sorted(set(waits_for)))}

    known = frozenset(by_id)
    for item_id, item in by_id.items():
        unknown = set(item["waits_for"]) - known
        if unknown:
            raise ValueError(f"{item_id} waits for unknown ids: {sorted(unknown)!r}")

    graph: dict[str, tuple[str, ...]] = {}
    for item_id, item in by_id.items():
        if item["state"] in _TERMINAL_STATES:
            graph[item_id] = ()
        else:
            graph[item_id] = tuple(
                dep for dep in item["waits_for"] if by_id[dep]["state"] not in _TERMINAL_STATES
            )

    cycles = _scc_cycles(graph)
    if cycles:
        status = "DEADLOCK"
    elif all(item["state"] in _TERMINAL_STATES for item in by_id.values()):
        status = "QUIESCENT"
    elif any(item["state"] in {"READY", "RUNNING"} for item in by_id.values()):
        status = "PROGRESSABLE"
    else:
        status = "STARVATION_RISK"

    stalled_ids = tuple(
        sorted(
            item_id
            for item_id, item in by_id.items()
            if item["state"] not in _TERMINAL_STATES and item["state"] not in {"READY", "RUNNING"}
        )
    )
    return {
        "status": status,
        "cycles": cycles,
        "stalled_ids": stalled_ids,
        "promotion_permitted": False,
    }
