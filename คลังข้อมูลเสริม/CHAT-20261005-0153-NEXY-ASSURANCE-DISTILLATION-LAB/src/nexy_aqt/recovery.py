from __future__ import annotations

from collections import deque
from typing import Any

from .common import ContractError, fingerprint


def plan_recovery(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ContractError("payload must be object")
    states = payload.get("states")
    transitions = payload.get("transitions")
    current = payload.get("current_state")
    safe_states = payload.get("safe_states")
    evidence = payload.get("available_evidence", [])
    max_steps = payload.get("max_steps", 16)
    if not isinstance(states, list) or not states or not all(isinstance(x, str) for x in states):
        raise ContractError("states must be non-empty list[str]")
    if len(states) != len(set(states)):
        raise ContractError("duplicate states")
    if len(states) > 5000:
        raise ContractError("state count exceeds 5000")
    state_set = set(states)
    if current not in state_set:
        raise ContractError("current_state must exist in states")
    if not isinstance(safe_states, list) or not safe_states or not set(safe_states) <= state_set:
        raise ContractError("safe_states must be non-empty subset of states")
    if not isinstance(evidence, list) or not all(isinstance(x, str) for x in evidence):
        raise ContractError("available_evidence must be list[str]")
    evidence_set = set(evidence)
    if not isinstance(max_steps, int) or not 0 <= max_steps <= 64:
        raise ContractError("max_steps must be an integer in [0, 64]")
    if current in set(safe_states):
        return {"status": "PASS", "reason_codes": ["ALREADY_SAFE"], "input_hash": fingerprint(payload), "chosen_path": [], "alternate_shortest_paths": []}
    if not isinstance(transitions, list):
        raise ContractError("transitions must be list")
    if len(transitions) > 20000:
        raise ContractError("transition count exceeds 20000")

    edges: dict[str, list[tuple[str, str]]] = {s: [] for s in states}
    seen_ids: set[str] = set()
    blocked: list[str] = []
    for idx, t in enumerate(transitions):
        if not isinstance(t, dict):
            raise ContractError("transition must be object")
        tid = t.get("id", f"transition-{idx:04d}")
        if not isinstance(tid, str) or not tid or tid in seen_ids:
            raise ContractError(f"invalid/duplicate transition id: {tid!r}")
        seen_ids.add(tid)
        src, dst = t.get("from"), t.get("to")
        if src not in state_set or dst not in state_set:
            raise ContractError(f"transition {tid} references unknown state")
        req = t.get("requires_evidence", [])
        if not isinstance(req, list) or not all(isinstance(x, str) for x in req):
            raise ContractError("requires_evidence must be list[str]")
        if not set(req) <= evidence_set:
            blocked.append(tid)
            continue
        edges[src].append((tid, dst))
    for src in edges:
        edges[src].sort()

    queue = deque([(current, [])])
    best_depth: dict[str, int] = {current: 0}
    found: list[list[str]] = []
    found_depth: int | None = None
    safe_set = set(safe_states)
    while queue:
        state, path = queue.popleft()
        depth = len(path)
        if found_depth is not None and depth >= found_depth:
            continue
        if depth >= max_steps:
            continue
        for tid, dst in edges[state]:
            new_path = path + [tid]
            nd = len(new_path)
            if dst in safe_set:
                if found_depth is None:
                    found_depth = nd
                if nd == found_depth:
                    found.append(new_path)
                continue
            previous = best_depth.get(dst)
            if previous is None or nd <= previous:
                best_depth[dst] = nd
                queue.append((dst, new_path))

    if not found:
        return {
            "status": "FREEZE",
            "reason_codes": ["NO_PROVABLE_SAFE_RECOVERY_PATH"],
            "input_hash": fingerprint(payload),
            "blocked_transition_ids": sorted(blocked),
            "chosen_path": [],
            "alternate_shortest_paths": [],
        }
    found.sort()
    reasons = ["SAFE_RECOVERY_PATH_FOUND"]
    if len(found) > 1:
        reasons.append("MULTIPLE_SHORTEST_PATHS_DETERMINISTICALLY_TIE_BROKEN")
    return {
        "status": "PASS",
        "reason_codes": reasons,
        "input_hash": fingerprint(payload),
        "chosen_path": found[0],
        "alternate_shortest_paths": found[1:],
        "blocked_transition_ids": sorted(blocked),
    }
