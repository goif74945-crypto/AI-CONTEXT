from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable, Sequence

from .common import FrontierInputError, require_text, stable_hash


@dataclass(frozen=True, slots=True)
class Capability:
    capability_id: str
    requires: frozenset[str]
    grants: frozenset[str]
    scope: str


@dataclass(frozen=True, slots=True)
class ForbiddenPrivilegeSet:
    rule_id: str
    tokens: frozenset[str]


@dataclass(frozen=True, slots=True)
class CompositionReport:
    status: str
    reached_tokens: tuple[str, ...]
    witness_capabilities: tuple[str, ...]
    violated_rules: tuple[str, ...]
    explored_states: int
    fingerprint: str


def _canon_cap(c: Capability) -> Capability:
    cid = require_text(c.capability_id, "capability_id")
    req = frozenset(require_text(x, f"{cid}.requires") for x in c.requires)
    grants = frozenset(require_text(x, f"{cid}.grants") for x in c.grants)
    if not grants:
        raise FrontierInputError(f"{cid}:NO_GRANTS")
    return Capability(cid, req, grants, require_text(c.scope, f"{cid}.scope"))


def _canon_rule(r: ForbiddenPrivilegeSet) -> ForbiddenPrivilegeSet:
    rid = require_text(r.rule_id, "rule_id")
    tokens = frozenset(require_text(x, f"{rid}.token") for x in r.tokens)
    if not tokens:
        raise FrontierInputError(f"{rid}:EMPTY_FORBIDDEN_SET")
    return ForbiddenPrivilegeSet(rid, tokens)


def analyze_capability_composition(
    capabilities: Iterable[Capability],
    initial_tokens: Iterable[str],
    forbidden_sets: Sequence[ForbiddenPrivilegeSet],
    *,
    allowed_scopes: frozenset[str],
    max_steps: int = 12,
) -> CompositionReport:
    if not isinstance(max_steps, int) or not 1 <= max_steps <= 64:
        raise FrontierInputError("MAX_STEPS_OUT_OF_RANGE")
    caps = tuple(sorted((_canon_cap(c) for c in capabilities), key=lambda c: c.capability_id))
    cap_ids = [c.capability_id for c in caps]
    if len(cap_ids) != len(set(cap_ids)):
        raise FrontierInputError("DUPLICATE_CAPABILITY_ID")
    rules = tuple(sorted((_canon_rule(r) for r in forbidden_sets), key=lambda r: r.rule_id))
    rule_ids = [r.rule_id for r in rules]
    if len(rule_ids) != len(set(rule_ids)):
        raise FrontierInputError("DUPLICATE_FORBIDDEN_RULE_ID")
    scopes = frozenset(require_text(x, "allowed_scope") for x in allowed_scopes)
    start = frozenset(require_text(x, "initial_token") for x in initial_tokens)

    def violated(tokens: frozenset[str]) -> tuple[str, ...]:
        return tuple(r.rule_id for r in rules if r.tokens.issubset(tokens))

    initial_violations = violated(start)
    if initial_violations:
        payload = {"status": "FREEZE", "start": sorted(start), "violations": initial_violations}
        return CompositionReport("FREEZE", tuple(sorted(start)), (), initial_violations, 1, stable_hash(payload))

    queue = deque([(start, tuple())])
    seen = {start}
    max_reached = start
    explored = 0
    while queue:
        tokens, path = queue.popleft()
        explored += 1
        if len(tokens) > len(max_reached) or (len(tokens) == len(max_reached) and tuple(sorted(tokens)) < tuple(sorted(max_reached))):
            max_reached = tokens
        if len(path) >= max_steps:
            continue
        for cap in caps:
            if cap.scope not in scopes or cap.capability_id in path:
                continue
            if not cap.requires.issubset(tokens):
                continue
            new_tokens = frozenset(set(tokens) | set(cap.grants))
            new_path = path + (cap.capability_id,)
            bad = violated(new_tokens)
            if bad:
                payload = {"status": "FREEZE", "tokens": sorted(new_tokens), "path": new_path, "violations": bad}
                return CompositionReport("FREEZE", tuple(sorted(new_tokens)), new_path, bad, explored, stable_hash(payload))
            if new_tokens not in seen:
                seen.add(new_tokens)
                queue.append((new_tokens, new_path))

    payload = {"status": "PASS", "tokens": sorted(max_reached), "explored": explored}
    return CompositionReport("PASS", tuple(sorted(max_reached)), (), (), explored, stable_hash(payload))
