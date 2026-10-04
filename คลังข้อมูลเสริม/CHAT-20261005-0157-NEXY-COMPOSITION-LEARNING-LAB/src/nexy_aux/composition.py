from __future__ import annotations

from collections import defaultdict
from typing import Any

from .canonical import sha256


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    result["fingerprint"] = sha256(result)
    return result


def _literals(values: Any, field: str) -> set[str]:
    if values is None:
        return set()
    if not isinstance(values, list):
        raise ValueError(f"{field} must be a list")
    out: set[str] = set()
    for raw in values:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError(f"{field} contains an invalid literal")
        out.add(raw.strip())
    return out


def opposite(literal: str) -> str:
    return literal[1:] if literal.startswith("!") else f"!{literal}"


def _conflicts(facts: set[str]) -> list[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for lit in facts:
        opp = opposite(lit)
        if opp in facts:
            pairs.add(tuple(sorted((lit, opp))))
    return sorted(pairs)


def compose(components: list[dict[str, Any]], initial_facts: list[str] | None = None) -> dict[str, Any]:
    """Compose explicit assume/guarantee contracts with fail-closed semantics.

    Scheduling uses an inverted assumption index rather than repeatedly scanning all
    pending components. Components becoming ready during a wave are admitted in the
    next wave, preserving deterministic wave semantics.
    """
    if not isinstance(components, list):
        raise ValueError("components must be a list")

    facts = _literals(initial_facts or [], "initial_facts")
    initial_conflicts = _conflicts(facts)
    if initial_conflicts:
        return _finish({
            "status": "FREEZE",
            "reason": "CONTRADICTORY_INITIAL_FACTS",
            "conflicts": initial_conflicts,
            "admitted_order": [],
            "facts": sorted(facts),
        })

    parsed: dict[str, dict[str, Any]] = {}
    for raw in components:
        if not isinstance(raw, dict):
            raise ValueError("each component must be an object")
        cid = raw.get("id")
        if not isinstance(cid, str) or not cid.strip():
            raise ValueError("component.id must be a non-empty string")
        cid = cid.strip()
        if cid in parsed:
            raise ValueError(f"duplicate component id: {cid}")
        assumptions = _literals(raw.get("assumptions", []), f"{cid}.assumptions")
        guarantees = _literals(raw.get("guarantees", []), f"{cid}.guarantees")
        own_conflicts = _conflicts(guarantees)
        if own_conflicts:
            return _finish({
                "status": "FREEZE",
                "reason": "SELF_CONTRADICTORY_GUARANTEE",
                "component_id": cid,
                "conflicts": own_conflicts,
                "admitted_order": [],
                "facts": sorted(facts),
            })
        parsed[cid] = {"id": cid, "assumptions": assumptions, "guarantees": guarantees}

    pending = set(parsed)
    unmet: dict[str, set[str]] = {}
    waiters: dict[str, set[str]] = defaultdict(set)
    ready: list[str] = []

    for cid in sorted(parsed):
        missing = set(parsed[cid]["assumptions"]) - facts
        unmet[cid] = missing
        if not missing:
            ready.append(cid)
        else:
            for literal in missing:
                waiters[literal].add(cid)

    admitted: list[str] = []
    waves: list[list[str]] = []

    while ready:
        wave_ids = sorted(ready)
        wave: list[str] = []
        next_ready: set[str] = set()

        for cid in wave_ids:
            if cid not in pending:
                continue
            guarantees = parsed[cid]["guarantees"]
            conflicting = sorted(g for g in guarantees if opposite(g) in facts)
            if conflicting:
                return _finish({
                    "status": "FREEZE",
                    "reason": "CONTRADICTORY_GUARANTEE",
                    "component_id": cid,
                    "conflicting_guarantees": conflicting,
                    "admitted_order": admitted,
                    "waves": waves,
                    "facts": sorted(facts),
                })

            newly_established: list[str] = []
            for guarantee in sorted(guarantees):
                if guarantee not in facts:
                    facts.add(guarantee)
                    newly_established.append(guarantee)

            pending.remove(cid)
            admitted.append(cid)
            wave.append(cid)

            for guarantee in newly_established:
                for waiting_cid in sorted(waiters.pop(guarantee, set())):
                    if waiting_cid not in pending:
                        continue
                    unmet[waiting_cid].discard(guarantee)
                    if not unmet[waiting_cid]:
                        next_ready.add(waiting_cid)

        waves.append(wave)
        ready = sorted(next_ready)

    if pending:
        unresolved: dict[str, Any] = {}
        for cid in sorted(pending):
            missing = sorted(unmet[cid])
            contradicted = sorted(lit for lit in missing if opposite(lit) in facts)
            unresolved[cid] = {
                "missing_assumptions": missing,
                "contradicted_assumptions": contradicted,
            }
        return _finish({
            "status": "FREEZE",
            "reason": "UNSATISFIED_ASSUMPTIONS",
            "admitted_order": admitted,
            "waves": waves,
            "facts": sorted(facts),
            "unresolved": unresolved,
        })

    return _finish({
        "status": "PASS",
        "reason": "COMPOSABLE",
        "admitted_order": admitted,
        "waves": waves,
        "facts": sorted(facts),
    })
