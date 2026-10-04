"""AI-PROPOSED: mutation testing for acceptance/evidence gates."""
from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class Mutator:
    name: str
    mutate: Callable[[Any], Any]


def evaluate_gate(
    baseline: Any,
    gate: Callable[[Any], bool],
    mutators: Iterable[Mutator],
) -> dict[str, Any]:
    """Measure whether a gate rejects intentionally-invalid variants.

    The baseline and every mutant are deep-copied so a malicious or careless mutator
    cannot change the caller's source object in place.
    """
    pristine = copy.deepcopy(baseline)
    try:
        baseline_accepted = bool(gate(copy.deepcopy(pristine)))
    except Exception as exc:
        return {
            "status": "GATE_ERROR",
            "baseline_accepted": False,
            "kill_rate": 0.0,
            "killed": [],
            "survivors": [],
            "errors": [{"name": "baseline", "error_type": type(exc).__name__}],
        }

    if not baseline_accepted:
        return {
            "status": "INVALID_BASELINE",
            "baseline_accepted": False,
            "kill_rate": 0.0,
            "killed": [],
            "survivors": [],
            "errors": [],
        }

    killed: list[str] = []
    survivors: list[str] = []
    errors: list[dict[str, str]] = []
    mutation_list = list(mutators)

    for mutator in mutation_list:
        try:
            mutant = mutator.mutate(copy.deepcopy(pristine))
            accepted = bool(gate(copy.deepcopy(mutant)))
        except Exception as exc:
            errors.append({"name": mutator.name, "error_type": type(exc).__name__})
            continue
        if accepted:
            survivors.append(mutator.name)
        else:
            killed.append(mutator.name)

    killed.sort()
    survivors.sort()
    errors.sort(key=lambda e: (e["name"], e["error_type"]))
    total = len(mutation_list)
    kill_rate = (len(killed) / total) if total else 1.0

    if not mutation_list:
        status = "NOT_VERIFIED"
    elif errors:
        status = "MUTATOR_ERROR"
    elif survivors:
        status = "WEAK_GATE"
    else:
        status = "PASS"

    return {
        "status": status,
        "baseline_accepted": True,
        "kill_rate": kill_rate,
        "killed": killed,
        "survivors": survivors,
        "errors": errors,
    }
