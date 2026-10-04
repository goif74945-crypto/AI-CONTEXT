from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class WitnessError(ValueError):
    """Raised when proof-witness inputs are malformed or ambiguous."""


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    covers: frozenset[str]
    cost: int = 1


@dataclass(frozen=True)
class WitnessResult:
    selected_ids: tuple[str, ...]
    total_cost: int
    covered: frozenset[str]
    uncovered: frozenset[str]
    exact: bool


def _is_better(candidate: tuple[int, int, tuple[str, ...]], current: tuple[int, int, tuple[str, ...]] | None) -> bool:
    if current is None:
        return True
    return candidate < current


def extract_minimal_witness(
    requirements: Iterable[str],
    evidence: Iterable[EvidenceItem],
) -> WitnessResult:
    reqs = tuple(sorted(set(requirements)))
    if not reqs:
        raise WitnessError("requirements must be non-empty")
    if any(not req.strip() for req in reqs):
        raise WitnessError("requirement IDs must be non-empty")

    req_index = {req: idx for idx, req in enumerate(reqs)}
    items = tuple(sorted(evidence, key=lambda item: item.evidence_id))
    ids = [item.evidence_id for item in items]
    if len(ids) != len(set(ids)):
        raise WitnessError("evidence IDs must be unique")

    normalized: list[tuple[EvidenceItem, int]] = []
    union_mask = 0
    for item in items:
        if not item.evidence_id.strip():
            raise WitnessError("evidence ID must be non-empty")
        if isinstance(item.cost, bool) or not isinstance(item.cost, int) or item.cost < 0:
            raise WitnessError(f"evidence {item.evidence_id} cost must be a non-negative integer")
        unknown = sorted(set(item.covers) - set(reqs))
        if unknown:
            raise WitnessError(
                f"evidence {item.evidence_id} covers unknown requirements: {', '.join(unknown)}"
            )
        mask = 0
        for req in item.covers:
            mask |= 1 << req_index[req]
        union_mask |= mask
        normalized.append((item, mask))

    full_mask = (1 << len(reqs)) - 1
    dp: dict[int, tuple[int, int, tuple[str, ...]]] = {0: (0, 0, ())}
    for item, item_mask in normalized:
        snapshot = list(dp.items())
        for mask, score in snapshot:
            new_mask = mask | item_mask
            ids_tuple = tuple(sorted(score[2] + (item.evidence_id,)))
            candidate = (score[0] + item.cost, score[1] + 1, ids_tuple)
            if _is_better(candidate, dp.get(new_mask)):
                dp[new_mask] = candidate

    best = dp.get(full_mask)
    if best is None:
        covered_reqs = frozenset(reqs[idx] for idx in range(len(reqs)) if union_mask & (1 << idx))
        uncovered = frozenset(set(reqs) - set(covered_reqs))
        return WitnessResult(
            selected_ids=(),
            total_cost=0,
            covered=covered_reqs,
            uncovered=uncovered,
            exact=False,
        )

    return WitnessResult(
        selected_ids=best[2],
        total_cost=best[0],
        covered=frozenset(reqs),
        uncovered=frozenset(),
        exact=True,
    )
