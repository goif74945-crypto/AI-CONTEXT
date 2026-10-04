from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .comet import OverlapEvidence, build_overlap_index
from .common import ContractError, fingerprint, require_text, require_unit
from .q64 import Q64


@dataclass(frozen=True, slots=True)
class PortfolioCandidate:
    candidate_id: str
    conservative_value: Q64
    implementation_cost: Q64
    complexity_tax: Q64
    domains: frozenset[str]
    requires: frozenset[str] = frozenset()
    conflicts: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        require_text(self.candidate_id, "candidate_id")
        require_unit(self.conservative_value, "conservative_value")
        if not isinstance(self.implementation_cost, Q64) or self.implementation_cost.raw < 0:
            raise ContractError("implementation_cost must be non-negative Q64.64")
        if not isinstance(self.complexity_tax, Q64) or self.complexity_tax.raw < 0:
            raise ContractError("complexity_tax must be non-negative Q64.64")
        if not self.domains or any(not isinstance(x, str) or not x.strip() for x in self.domains):
            raise ContractError("domains must contain non-empty strings")
        if self.candidate_id in self.requires or self.candidate_id in self.conflicts:
            raise ContractError("candidate cannot require/conflict with itself")


@dataclass(frozen=True, slots=True)
class PortfolioPolicy:
    budget: Q64
    complexity_budget: Q64
    max_items: int
    minimum_distinct_domains: int
    pair_overlap_penalty_weight: Q64

    def __post_init__(self) -> None:
        for field in ("budget", "complexity_budget"):
            value = getattr(self, field)
            if not isinstance(value, Q64) or value.raw < 0:
                raise ContractError(f"{field} must be non-negative Q64.64")
        if not isinstance(self.max_items, int) or isinstance(self.max_items, bool) or self.max_items <= 0:
            raise ContractError("max_items must be positive int")
        if not isinstance(self.minimum_distinct_domains, int) or isinstance(self.minimum_distinct_domains, bool) or self.minimum_distinct_domains <= 0:
            raise ContractError("minimum_distinct_domains must be positive int")
        require_unit(self.pair_overlap_penalty_weight, "pair_overlap_penalty_weight")


@dataclass(frozen=True, slots=True)
class PortfolioDecision:
    status: str
    selected_ids: tuple[str, ...]
    score: Q64 | None
    total_cost: Q64
    total_complexity: Q64
    distinct_domains: tuple[str, ...]
    evaluated_subsets: int
    reason: str
    fingerprint: str


def compose_portfolio(
    candidates: Iterable[PortfolioCandidate],
    *,
    overlap_evidence: Iterable[OverlapEvidence],
    policy: PortfolioPolicy,
    available_capabilities: frozenset[str] = frozenset(),
) -> PortfolioDecision:
    items = sorted(candidates, key=lambda c: c.candidate_id)
    if not items:
        return _result("FREEZE", (), None, Q64.zero(), Q64.zero(), (), 0, "NO_CANDIDATES")
    if len(items) > 18:
        return _result("FREEZE", (), None, Q64.zero(), Q64.zero(), (), 0, "REFERENCE_ENUMERATION_LIMIT_EXCEEDED")
    ids = [c.candidate_id for c in items]
    if len(ids) != len(set(ids)):
        return _result("FREEZE", (), None, Q64.zero(), Q64.zero(), (), 0, "DUPLICATE_CANDIDATE_ID")
    known = set(ids) | set(available_capabilities)
    for c in items:
        if not c.requires.issubset(known):
            return _result("FREEZE", (), None, Q64.zero(), Q64.zero(), (), 0, f"UNKNOWN_REQUIREMENT:{c.candidate_id}")
        if not c.conflicts.issubset(set(ids)):
            return _result("FREEZE", (), None, Q64.zero(), Q64.zero(), (), 0, f"UNKNOWN_CONFLICT:{c.candidate_id}")

    overlap_index, error = build_overlap_index(overlap_evidence)
    if error:
        return _result("FREEZE", (), None, Q64.zero(), Q64.zero(), (), 0, error)
    # Complete pairwise evidence is mandatory because missing overlap data can bias portfolio score.
    for a, b in combinations(ids, 2):
        if tuple(sorted((a, b))) not in overlap_index:
            return _result("FREEZE", (), None, Q64.zero(), Q64.zero(), (), 0, f"MISSING_PAIRWISE_OVERLAP:{a}:{b}")

    evaluated = 0
    best: tuple[Q64, Q64, Q64, tuple[str, ...], tuple[str, ...]] | None = None
    item_by_id = {c.candidate_id: c for c in items}
    max_size = min(policy.max_items, len(items))
    for size in range(1, max_size + 1):
        for subset in combinations(items, size):
            evaluated += 1
            subset_ids = tuple(c.candidate_id for c in subset)
            subset_set = set(subset_ids)
            if any(c.conflicts & subset_set for c in subset):
                continue
            if any(not c.requires.issubset(subset_set | set(available_capabilities)) for c in subset):
                continue
            cost = Q64.zero()
            complexity = Q64.zero()
            value = Q64.zero()
            domains: set[str] = set()
            for c in subset:
                cost = cost + c.implementation_cost
                complexity = complexity + c.complexity_tax
                value = value + c.conservative_value
                domains.update(c.domains)
            if cost.raw > policy.budget.raw or complexity.raw > policy.complexity_budget.raw:
                continue
            if len(domains) < policy.minimum_distinct_domains:
                continue
            penalty = Q64.zero()
            for a, b in combinations(subset_ids, 2):
                ca, cb = item_by_id[a], item_by_id[b]
                overlap = overlap_index[tuple(sorted((a, b)))].overlap
                smaller = ca.conservative_value.min(cb.conservative_value)
                penalty = penalty + policy.pair_overlap_penalty_weight * overlap * smaller
            score = value - penalty
            # Highest score; then lower cost; then lower complexity; then lexicographically smaller IDs.
            if best is None:
                best = (score, cost, complexity, subset_ids, tuple(sorted(domains)))
            else:
                bscore, bcost, bcomplexity, bids, _ = best
                if (
                    score.raw > bscore.raw
                    or (score.raw == bscore.raw and cost.raw < bcost.raw)
                    or (score.raw == bscore.raw and cost.raw == bcost.raw and complexity.raw < bcomplexity.raw)
                    or (score.raw == bscore.raw and cost.raw == bcost.raw and complexity.raw == bcomplexity.raw and subset_ids < bids)
                ):
                    best = (score, cost, complexity, subset_ids, tuple(sorted(domains)))
    if best is None:
        return _result("HOLD", (), None, Q64.zero(), Q64.zero(), (), evaluated, "NO_FEASIBLE_PORTFOLIO")
    score, cost, complexity, selected, domains = best
    return _result("SELECT", selected, score, cost, complexity, domains, evaluated, "MAX_CONSERVATIVE_PORTFOLIO_VALUE")


def _result(status: str, selected: tuple[str, ...], score: Q64 | None, cost: Q64, complexity: Q64, domains: tuple[str, ...], evaluated: int, reason: str) -> PortfolioDecision:
    core = {
        "status": status,
        "selected_ids": selected,
        "score": score,
        "total_cost": cost,
        "total_complexity": complexity,
        "distinct_domains": domains,
        "evaluated_subsets": evaluated,
        "reason": reason,
    }
    return PortfolioDecision(status, selected, score, cost, complexity, domains, evaluated, reason, fingerprint(core))
