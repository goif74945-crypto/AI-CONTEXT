from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .errors import ObservationValidationError
from .model import OutcomeContract
from .verifier import evaluate_criterion, verify_outcome


def _soft_vector(contract: OutcomeContract, observation: Mapping[str, Any]) -> tuple[float, ...]:
    vector: list[float] = []
    for criterion in contract.criteria:
        if criterion.hard:
            continue
        result = evaluate_criterion(criterion, observation)
        if result is None or result.margin is None:
            raise ObservationValidationError(f"cannot build frontier vector for {criterion.criterion_id}")
        vector.append(float(result.margin))
    return tuple(vector)


def _dominates(left: tuple[float, ...], right: tuple[float, ...]) -> bool:
    return all(a >= b for a, b in zip(left, right, strict=True)) and any(
        a > b for a, b in zip(left, right, strict=True)
    )


def satisfaction_frontier(
    contract: OutcomeContract,
    candidates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    seen: set[str] = set()
    admissible: list[tuple[str, Mapping[str, Any], tuple[float, ...], dict[str, Any]]] = []
    rejected: list[dict[str, Any]] = []

    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            raise ObservationValidationError(f"candidate[{index}] must be an object")
        candidate_id = candidate.get("candidate_id")
        observation = candidate.get("observation")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ObservationValidationError(f"candidate[{index}].candidate_id must be non-empty")
        if candidate_id in seen:
            raise ObservationValidationError(f"duplicate candidate_id: {candidate_id}")
        seen.add(candidate_id)
        if not isinstance(observation, Mapping):
            raise ObservationValidationError(f"candidate[{index}].observation must be an object")
        report = verify_outcome(contract, observation)
        if report["status"] in {"FAIL", "FREEZE"}:
            rejected.append({"candidate_id": candidate_id, "status": report["status"]})
            continue
        vector = _soft_vector(contract, observation)
        admissible.append((candidate_id, observation, vector, report))

    frontier_ids: list[str] = []
    dominated_by: dict[str, list[str]] = {}
    for candidate_id, _, vector, _ in admissible:
        dominators = [
            other_id
            for other_id, _, other_vector, _ in admissible
            if other_id != candidate_id and _dominates(other_vector, vector)
        ]
        if dominators:
            dominated_by[candidate_id] = sorted(dominators)
        else:
            frontier_ids.append(candidate_id)

    return {
        "status": "PASS" if frontier_ids else "FAIL",
        "frontier": sorted(frontier_ids),
        "dominated_by": {key: dominated_by[key] for key in sorted(dominated_by)},
        "rejected": sorted(rejected, key=lambda x: x["candidate_id"]),
        "admissible_count": len(admissible),
    }
