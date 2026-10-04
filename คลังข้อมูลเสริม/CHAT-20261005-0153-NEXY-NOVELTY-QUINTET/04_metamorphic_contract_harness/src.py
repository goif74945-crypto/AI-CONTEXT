"""AI-PROPOSED: oracle-light contract testing via metamorphic relations."""
from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence


@dataclass(frozen=True)
class Relation:
    name: str
    mutate: Callable[[Any], Any]
    holds: Callable[[Callable[[Any], Any], Any, Any], bool]


def evaluate(
    function_under_test: Callable[[Any], Any],
    seeds: Iterable[Any],
    relations: Sequence[Relation],
) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    seed_list = list(seeds)
    checks = 0

    for seed_index, original_seed in enumerate(seed_list):
        for relation in relations:
            checks += 1
            seed = copy.deepcopy(original_seed)
            try:
                mutated = relation.mutate(copy.deepcopy(seed))
            except Exception as exc:  # fail-closed capture, no hidden skip
                violations.append(
                    {
                        "seed_index": seed_index,
                        "relation": relation.name,
                        "reason": "MUTATION_ERROR",
                        "error_type": type(exc).__name__,
                    }
                )
                continue
            try:
                holds = bool(relation.holds(function_under_test, copy.deepcopy(seed), copy.deepcopy(mutated)))
            except Exception as exc:
                violations.append(
                    {
                        "seed_index": seed_index,
                        "relation": relation.name,
                        "reason": "RELATION_ERROR",
                        "error_type": type(exc).__name__,
                    }
                )
                continue
            if not holds:
                violations.append(
                    {
                        "seed_index": seed_index,
                        "relation": relation.name,
                        "reason": "RELATION_VIOLATION",
                    }
                )

    violations.sort(key=lambda v: (v["seed_index"], v["relation"], v["reason"]))
    status = "NOT_VERIFIED" if checks == 0 else ("PASS" if not violations else "FAIL")
    return {
        "status": status,
        "seed_count": len(seed_list),
        "relation_count": len(relations),
        "checks": checks,
        "violations": violations,
    }
