from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Claim:
    claim_id: str
    accepted_evidence_classes: frozenset[str]


@dataclass(frozen=True)
class Check:
    check_id: str
    cost_units: int
    evidence: Mapping[str, str]


@dataclass(frozen=True)
class Portfolio:
    checks: tuple[str, ...]
    total_cost_units: int
    coverage: tuple[tuple[str, str, str], ...]  # claim, evidence_class, check_id


class NoValidPortfolio(ValueError):
    pass


class PortfolioTooLarge(ValueError):
    pass


def _validate(claims: tuple[Claim, ...], checks: tuple[Check, ...]) -> None:
    claim_ids = [c.claim_id for c in claims]
    if len(claim_ids) != len(set(claim_ids)):
        raise ValueError("claim_id values must be unique")
    check_ids = [c.check_id for c in checks]
    if len(check_ids) != len(set(check_ids)):
        raise ValueError("check_id values must be unique")
    for claim in claims:
        if not claim.accepted_evidence_classes:
            raise ValueError(f"claim {claim.claim_id} has no accepted evidence class")
    for check in checks:
        if check.cost_units < 0:
            raise ValueError(f"check {check.check_id} has negative cost")


def optimize_portfolio(
    claims: Iterable[Claim],
    checks: Iterable[Check],
    *,
    max_exact_claims: int = 20,
) -> Portfolio:
    """
    Find an exact minimum-cost evidence portfolio using dynamic programming over claim coverage.

    Complexity is O(number_of_checks * reachable_coverage_states), bounded by 2^claims rather
    than 2^checks. Evidence classes are matched by explicit membership; E1 is never silently
    accepted for an E2-only claim merely because the labels look ordinal.
    """
    claim_tuple = tuple(sorted(claims, key=lambda c: c.claim_id))
    check_tuple = tuple(sorted(checks, key=lambda c: c.check_id))
    _validate(claim_tuple, check_tuple)
    if len(claim_tuple) > max_exact_claims:
        raise PortfolioTooLarge(
            f"exact optimizer limited to {max_exact_claims} claims; got {len(claim_tuple)}"
        )
    if not claim_tuple:
        return Portfolio(checks=(), total_cost_units=0, coverage=())

    claim_index = {claim.claim_id: i for i, claim in enumerate(claim_tuple)}
    check_masks: dict[str, int] = {}
    for check in check_tuple:
        mask = 0
        for claim_id, evidence_class in check.evidence.items():
            idx = claim_index.get(claim_id)
            if idx is None:
                continue
            if evidence_class in claim_tuple[idx].accepted_evidence_classes:
                mask |= 1 << idx
        check_masks[check.check_id] = mask

    # mask -> (total_cost, check_count, sorted_ids)
    dp: dict[int, tuple[int, int, tuple[str, ...]]] = {0: (0, 0, ())}
    for check in check_tuple:
        check_mask = check_masks[check.check_id]
        if check_mask == 0:
            continue
        snapshot = tuple(dp.items())
        for mask, (cost, count, ids) in snapshot:
            new_mask = mask | check_mask
            if new_mask == mask:
                continue
            candidate = (cost + check.cost_units, count + 1, ids + (check.check_id,))
            incumbent = dp.get(new_mask)
            if incumbent is None or candidate < incumbent:
                dp[new_mask] = candidate

    full_mask = (1 << len(claim_tuple)) - 1
    best = dp.get(full_mask)
    if best is None:
        missing = []
        for claim in claim_tuple:
            if not any(
                check.evidence.get(claim.claim_id) in claim.accepted_evidence_classes
                for check in check_tuple
            ):
                missing.append(claim.claim_id)
        suffix = f"; uncovered claims: {', '.join(missing)}" if missing else ""
        raise NoValidPortfolio("no portfolio satisfies all evidence obligations" + suffix)

    total_cost, _count, selected_ids = best
    selected = {c.check_id: c for c in check_tuple if c.check_id in set(selected_ids)}
    coverage = []
    for claim in claim_tuple:
        matches = sorted(
            (check_id, selected[check_id].evidence[claim.claim_id])
            for check_id in selected_ids
            if selected[check_id].evidence.get(claim.claim_id) in claim.accepted_evidence_classes
        )
        check_id, evidence_class = matches[0]
        coverage.append((claim.claim_id, evidence_class, check_id))

    return Portfolio(
        checks=selected_ids,
        total_cost_units=total_cost,
        coverage=tuple(coverage),
    )
