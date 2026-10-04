from __future__ import annotations

import json
import statistics
import time

from nexy_outcome.compiler import compile_contract
from nexy_outcome.frontier import satisfaction_frontier
from nexy_outcome.recovery import plan_recovery
from nexy_outcome.verifier import verify_outcome


def spec():
    return {
        "objective_id": "bench",
        "objective": "benchmark deterministic outcome evaluation",
        "criteria": [
            {"id": "hard", "path": "m.h", "op": "min", "value": 1, "hard": True, "weight": 0},
            {"id": "s1", "path": "m.a", "op": "max", "value": 100, "hard": False, "weight": 1},
            {"id": "s2", "path": "m.b", "op": "min", "value": 50, "hard": False, "weight": 1},
            {"id": "s3", "path": "m.c", "op": "range", "value": [0, 10], "hard": False, "weight": 1},
        ],
        "forbidden_effects": [{"id": "f", "path": "e.bad", "op": "eq", "value": True}],
    }


def main() -> None:
    contract, _ = compile_contract(spec())
    obs = {"m": {"h": 2, "a": 90, "b": 60, "c": 5}, "e": {"bad": False}}

    start = time.perf_counter()
    for _ in range(20_000):
        verify_outcome(contract, obs)
    verify_s = time.perf_counter() - start

    candidates = []
    for i in range(120):
        candidates.append(
            {
                "candidate_id": f"c{i:03d}",
                "observation": {
                    "m": {"h": 2, "a": 60 + (i % 40), "b": 50 + (i % 30), "c": i % 11},
                    "e": {"bad": False},
                },
            }
        )
    frontier_times = []
    for _ in range(10):
        start = time.perf_counter()
        satisfaction_frontier(contract, candidates)
        frontier_times.append(time.perf_counter() - start)

    broken = {"m": {"h": 0, "a": 90, "b": 60, "c": 5}, "e": {"bad": False}}
    actions = [
        {
            "action_id": f"a{i:02d}",
            "cost": float(i + 1),
            "risk": 0.001 * i,
            "reversible": True,
            "effects": {"m.h": 2 if i == 0 else 0, f"x.v{i}": i},
        }
        for i in range(10)
    ]
    recovery_times = []
    for _ in range(5):
        start = time.perf_counter()
        plan_recovery(contract, broken, actions, max_cost=1000, max_risk=1.0)
        recovery_times.append(time.perf_counter() - start)

    print(
        json.dumps(
            {
                "environment_note": "local sandbox; timings are informational, not a production SLA",
                "verify_20000_seconds": verify_s,
                "verify_ops_per_second": 20_000 / verify_s,
                "frontier_120_candidates_median_seconds": statistics.median(frontier_times),
                "recovery_10_actions_exact_search_median_seconds": statistics.median(recovery_times),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
