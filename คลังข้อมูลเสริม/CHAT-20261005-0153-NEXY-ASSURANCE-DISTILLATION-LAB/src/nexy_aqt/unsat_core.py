from __future__ import annotations

import itertools
from typing import Any

from .common import ContractError, fingerprint
from .predicates import evaluate_rule


def _validate_constraints(constraints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(constraints, list) or not constraints:
        raise ContractError("constraints must be a non-empty list")
    seen: set[str] = set()
    normalized = []
    for idx, c in enumerate(constraints):
        if not isinstance(c, dict):
            raise ContractError("constraint must be object")
        cid = c.get("id", f"constraint-{idx:04d}")
        if not isinstance(cid, str) or not cid:
            raise ContractError("constraint id must be non-empty string")
        if cid in seen:
            raise ContractError(f"duplicate constraint id: {cid}")
        seen.add(cid)
        cc = dict(c)
        cc["id"] = cid
        normalized.append(cc)
    return sorted(normalized, key=lambda x: x["id"])


def _feasible(candidates: list[dict[str, Any]], constraints: tuple[dict[str, Any], ...]) -> bool:
    return any(all(evaluate_rule(candidate, c) for c in constraints) for candidate in candidates)


def find_minimal_core(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ContractError("payload must be object")
    candidates = payload.get("candidates")
    constraints = _validate_constraints(payload.get("constraints"))
    max_constraints = payload.get("max_constraints", 16)
    if not isinstance(max_constraints, int) or not 1 <= max_constraints <= 20:
        raise ContractError("max_constraints must be an integer in [1, 20]")
    if len(constraints) > max_constraints:
        raise ContractError("constraint count exceeds max_constraints")
    if not isinstance(candidates, list) or not all(isinstance(x, dict) for x in candidates):
        raise ContractError("candidates must be a list of objects")
    if not candidates:
        raise ContractError("candidates must not be empty")
    if len(candidates) > 10000:
        raise ContractError("candidate count exceeds 10000")
    if _feasible(candidates, tuple(constraints)):
        matches = [i for i, cand in enumerate(candidates) if all(evaluate_rule(cand, c) for c in constraints)]
        return {
            "status": "PASS",
            "reason_codes": ["CONSTRAINT_SET_FEASIBLE"],
            "input_hash": fingerprint(payload),
            "matching_candidate_indexes": matches,
            "minimal_unsat_core": [],
        }

    for size in range(1, len(constraints) + 1):
        cores = []
        for combo in itertools.combinations(constraints, size):
            if not _feasible(candidates, combo):
                cores.append([c["id"] for c in combo])
        if cores:
            cores.sort()
            return {
                "status": "FREEZE",
                "reason_codes": ["NO_FEASIBLE_CANDIDATE", "MINIMAL_UNSAT_CORE_FOUND"],
                "input_hash": fingerprint(payload),
                "minimal_core_size": size,
                "minimal_unsat_core": cores[0],
                "alternate_minimal_cores": cores[1 : payload.get("max_alternates", 8) + 1],
            }
    raise AssertionError("full unsat set must contain an unsat subset")
