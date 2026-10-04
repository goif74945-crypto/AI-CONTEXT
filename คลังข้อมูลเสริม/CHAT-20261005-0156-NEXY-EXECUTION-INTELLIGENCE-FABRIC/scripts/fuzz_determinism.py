from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from concepts.assurance_budget_planner.engine import plan_assurance
from concepts.unknown_closure_planner.engine import plan_unknown_closure


def main() -> int:
    rng = random.Random(20261005)
    assurance_checks = 0
    unknown_checks = 0

    validators = [
        {"id": "a", "domain": "d1", "covers": ["x", "y"], "cost": 2, "latency_ms": 4},
        {"id": "b", "domain": "d2", "covers": ["y"], "cost": 1, "latency_ms": 2},
        {"id": "c", "domain": "d3", "covers": ["x"], "cost": 1, "latency_ms": 3},
        {"id": "d", "domain": "d4", "covers": ["x", "y"], "cost": 5, "latency_ms": 1},
    ]
    assurance_payload = {"requirements": {"x": 2, "y": 2}, "max_cost": 20}
    baseline_assurance = plan_assurance({**assurance_payload, "validators": validators})

    probes = [
        {"id": "a", "cost": 1, "resolves": ["u1"], "question": "u1?"},
        {"id": "b", "cost": 1, "resolves": ["u2"], "question": "u2?"},
        {"id": "c", "cost": 3, "resolves": ["u1", "u2"], "question": "both?"},
    ]
    unknown_payload = {"requirements": [{"id": "r", "blocked_by": ["u1", "u2"]}], "known": []}
    baseline_unknown = plan_unknown_closure({**unknown_payload, "probes": probes})

    for _ in range(500):
        v = list(validators)
        rng.shuffle(v)
        current = plan_assurance({**assurance_payload, "validators": v})
        if current != baseline_assurance:
            raise AssertionError("assurance planner changed under input permutation")
        assurance_checks += 1

        p = list(probes)
        rng.shuffle(p)
        current_u = plan_unknown_closure({**unknown_payload, "probes": p})
        if current_u != baseline_unknown:
            raise AssertionError("unknown planner changed under input permutation")
        unknown_checks += 1

    print(json.dumps({
        "status": "PASS",
        "seed": 20261005,
        "assurance_permutation_checks": assurance_checks,
        "unknown_permutation_checks": unknown_checks,
        "total_checks": assurance_checks + unknown_checks,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
