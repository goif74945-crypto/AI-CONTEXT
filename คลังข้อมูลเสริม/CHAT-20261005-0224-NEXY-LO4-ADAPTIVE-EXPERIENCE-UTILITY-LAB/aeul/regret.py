from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Iterable

from .common import ContractError, fingerprint, require_text, require_unit
from .q64 import Q64


@dataclass(frozen=True, slots=True)
class UtilityInterval:
    low: Q64
    high: Q64

    def __post_init__(self) -> None:
        require_unit(self.low, "low")
        require_unit(self.high, "high")
        if self.low.raw > self.high.raw:
            raise ContractError("utility interval low exceeds high")


@dataclass(frozen=True, slots=True)
class ProposalCandidate:
    proposal_id: str
    utilities: Mapping[str, UtilityInterval]

    def __post_init__(self) -> None:
        require_text(self.proposal_id, "proposal_id")
        if not self.utilities:
            raise ContractError("utilities cannot be empty")
        for key, interval in self.utilities.items():
            require_text(key, "objective")
            if not isinstance(interval, UtilityInterval):
                raise ContractError("utility values must be UtilityInterval")


@dataclass(frozen=True, slots=True)
class RegretPolicy:
    weights: Mapping[str, Q64]
    protected_minima: Mapping[str, Q64]
    max_worst_case_regret: Q64

    def __post_init__(self) -> None:
        if not self.weights:
            raise ContractError("weights cannot be empty")
        total = Q64.zero()
        for key, weight in self.weights.items():
            require_text(key, "weight objective")
            require_unit(weight, "weight")
            total = total + weight
        if total != Q64.one():
            raise ContractError("weights must sum exactly to 1.0 in Q64.64")
        for key, minimum in self.protected_minima.items():
            require_text(key, "protected objective")
            require_unit(minimum, "protected minimum")
        require_unit(self.max_worst_case_regret, "max_worst_case_regret")


@dataclass(frozen=True, slots=True)
class ProposalScore:
    proposal_id: str
    worst_utility: Q64
    best_utility: Q64
    worst_case_regret: Q64
    protected_ok: bool
    protected_failures: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RegretDecision:
    status: str
    selected_id: str | None
    reason: str
    scores: tuple[ProposalScore, ...]
    ideal_best_utility: Q64
    fingerprint: str


def select_proposal(candidates: Iterable[ProposalCandidate], policy: RegretPolicy) -> RegretDecision:
    items = list(candidates)
    if not items:
        return _result("FREEZE", None, "NO_CANDIDATES", (), Q64.zero())
    ids = [c.proposal_id for c in items]
    if len(ids) != len(set(ids)):
        return _result("FREEZE", None, "DUPLICATE_PROPOSAL_ID", (), Q64.zero())
    required = set(policy.weights)
    if set(policy.protected_minima) - required:
        return _result("FREEZE", None, "PROTECTED_OBJECTIVE_WITHOUT_WEIGHT", (), Q64.zero())
    for c in items:
        if set(c.utilities) != required:
            return _result("FREEZE", None, "OBJECTIVE_SET_MISMATCH", (), Q64.zero())

    provisional: list[tuple[ProposalCandidate, Q64, Q64, bool, tuple[str, ...]]] = []
    ideal_best = Q64.zero()
    for c in items:
        worst = Q64.zero()
        best = Q64.zero()
        failures: list[str] = []
        for obj in sorted(required):
            interval = c.utilities[obj]
            weight = policy.weights[obj]
            worst = worst + weight * interval.low
            best = best + weight * interval.high
            if obj in policy.protected_minima and interval.low.raw < policy.protected_minima[obj].raw:
                failures.append(obj)
        if best.raw > ideal_best.raw:
            ideal_best = best
        provisional.append((c, worst, best, not failures, tuple(failures)))

    scores: list[ProposalScore] = []
    for c, worst, best, protected_ok, failures in provisional:
        regret = ideal_best - worst
        scores.append(ProposalScore(c.proposal_id, worst, best, regret, protected_ok, failures))
    scores.sort(key=lambda s: (not s.protected_ok, s.worst_case_regret.raw, -s.worst_utility.raw, s.proposal_id))
    admissible = [s for s in scores if s.protected_ok]
    if not admissible:
        return _result("FREEZE", None, "ALL_CANDIDATES_VIOLATE_PROTECTED_MINIMA", tuple(scores), ideal_best)
    best = admissible[0]
    if best.worst_case_regret.raw > policy.max_worst_case_regret.raw:
        return _result("HOLD", None, "WORST_CASE_REGRET_TOO_HIGH", tuple(scores), ideal_best)
    return _result("SELECT", best.proposal_id, "MINIMAX_REGRET_WITH_PROTECTED_MINIMA", tuple(scores), ideal_best)


def _result(status: str, selected_id: str | None, reason: str, scores: tuple[ProposalScore, ...], ideal: Q64) -> RegretDecision:
    core = {"status": status, "selected_id": selected_id, "reason": reason, "scores": scores, "ideal_best_utility": ideal}
    return RegretDecision(status, selected_id, reason, scores, ideal, fingerprint(core))
