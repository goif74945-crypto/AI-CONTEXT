from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Iterable, Mapping

from .common import Verdict, allow, freeze

EVIDENCE_LEVEL = {f"E{i}": i for i in range(8)}


@dataclass(frozen=True)
class Claim:
    claim_id: str
    required_level: int
    prerequisites: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvidenceAction:
    action_id: str
    effects: tuple[tuple[str, int], ...]
    cost: int
    risk: int = 0
    requires: tuple[tuple[str, int], ...] = ()


def _validate_claims(claims: Mapping[str, Claim]) -> tuple[bool, str | None]:
    for cid, claim in claims.items():
        if cid != claim.claim_id or not (0 <= claim.required_level <= 7):
            return False, "INVALID_CLAIM"
        if any(p not in claims for p in claim.prerequisites):
            return False, "UNKNOWN_PREREQUISITE"
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(cid: str) -> bool:
        if cid in visiting:
            return False
        if cid in visited:
            return True
        visiting.add(cid)
        if not all(visit(p) for p in claims[cid].prerequisites):
            return False
        visiting.remove(cid)
        visited.add(cid)
        return True

    return (True, None) if all(visit(cid) for cid in claims) else (False, "CLAIM_CYCLE")


def _closure(targets: Iterable[str], claims: Mapping[str, Claim]) -> tuple[str, ...] | None:
    seen: set[str] = set()
    stack = list(targets)
    while stack:
        cid = stack.pop()
        if cid not in claims:
            return None
        if cid in seen:
            continue
        seen.add(cid)
        stack.extend(claims[cid].prerequisites)
    return tuple(sorted(seen))


def plan_evidence_closure(
    *,
    claims: Mapping[str, Claim],
    targets: Iterable[str],
    existing: Mapping[str, int],
    actions: Iterable[EvidenceAction],
    max_states: int = 10000,
) -> Verdict:
    ok, error = _validate_claims(claims)
    if not ok:
        return freeze(error or "INVALID_CLAIMS")
    needed = _closure(targets, claims)
    if needed is None:
        return freeze("UNKNOWN_TARGET")
    if max_states <= 0:
        return freeze("STATE_LIMIT_EXCEEDED")

    action_list = sorted(actions, key=lambda a: a.action_id)
    for action in action_list:
        if action.cost < 0 or action.risk < 0:
            return freeze("INVALID_ACTION_COST")
        for cid, level in (*action.effects, *action.requires):
            if cid not in claims or not (0 <= level <= 7):
                return freeze("INVALID_ACTION_REFERENCE")

    ids = tuple(sorted(claims))
    pos = {cid: i for i, cid in enumerate(ids)}
    start = tuple(max(-1, min(7, int(existing.get(cid, -1)))) for cid in ids)

    def goal(state: tuple[int, ...]) -> bool:
        return all(state[pos[cid]] >= claims[cid].required_level for cid in needed)

    if goal(start):
        return allow({"actions": [], "cost": 0, "risk": 0, "targets": list(needed)})

    # priority = total cost, total risk, action count, lexical path, state
    pq: list[tuple[int, int, int, tuple[str, ...], tuple[int, ...]]] = []
    heappush(pq, (0, 0, 0, tuple(), start))
    best: dict[tuple[int, ...], tuple[int, int, int, tuple[str, ...]]] = {
        start: (0, 0, 0, tuple())
    }
    explored = 0

    while pq:
        cost, risk, count, path, state = heappop(pq)
        score = (cost, risk, count, path)
        if best.get(state) != score:
            continue
        explored += 1
        if explored > max_states:
            return freeze("STATE_LIMIT_EXCEEDED", payload={"explored_states": explored - 1})
        if goal(state):
            return allow({
                "actions": list(path),
                "cost": cost,
                "explored_states": explored,
                "risk": risk,
                "targets": list(needed),
            })
        for action in action_list:
            if action.action_id in path:
                continue
            if any(state[pos[cid]] < level for cid, level in action.requires):
                continue
            new = list(state)
            changed = False
            for cid, level in action.effects:
                idx = pos[cid]
                if level > new[idx]:
                    new[idx] = level
                    changed = True
            if not changed:
                continue
            new_state = tuple(new)
            new_path = path + (action.action_id,)
            new_score = (cost + action.cost, risk + action.risk, count + 1, new_path)
            if new_state not in best or new_score < best[new_state]:
                best[new_state] = new_score
                heappush(pq, (*new_score, new_state))

    deficits = [cid for cid in needed if start[pos[cid]] < claims[cid].required_level]
    return freeze("NO_EVIDENCE_CLOSURE", payload={"unclosed_claims": deficits})
