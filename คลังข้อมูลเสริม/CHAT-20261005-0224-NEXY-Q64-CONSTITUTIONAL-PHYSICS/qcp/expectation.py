from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .fixed import Q64


@dataclass(frozen=True, slots=True)
class Consequence:
    consequence_id: str
    impact: Q64
    importance: Q64

    def __post_init__(self) -> None:
        if not self.consequence_id.strip():
            raise ValueError("consequence_id must be non-empty")
        if not isinstance(self.impact, Q64) or not isinstance(self.importance, Q64):
            raise TypeError("impact and importance must be Q64")
        if not (Q64.zero() <= self.impact <= Q64.one()):
            raise ValueError("impact must be in [0,1]")
        if self.importance <= Q64.zero():
            raise ValueError("importance must be > 0")


@dataclass(frozen=True, slots=True)
class ExpectationDecision:
    status: str
    reason: str
    divergence: Q64
    harmful_surprise: Q64
    worst_dimension: str | None


class ExpectationDivergenceBarrier:
    """Block execution when the executable consequence model materially diverges from its preview."""

    @staticmethod
    def _map(items: Iterable[Consequence]) -> dict[str, Consequence]:
        materialized = tuple(items)
        ids = [x.consequence_id for x in materialized]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate consequence_id")
        return {x.consequence_id: x for x in materialized}

    def compare(
        self,
        preview: Iterable[Consequence],
        actual: Iterable[Consequence],
        *,
        tolerance: Q64,
    ) -> ExpectationDecision:
        if not isinstance(tolerance, Q64):
            raise TypeError("tolerance must be Q64")
        if tolerance < Q64.zero():
            raise ValueError("tolerance must be non-negative")
        p = self._map(preview)
        a = self._map(actual)
        if not p:
            return ExpectationDecision("FREEZE", "EMPTY_PREVIEW", Q64.zero(), Q64.zero(), None)

        undeclared = sorted(set(a) - set(p))
        if undeclared:
            return ExpectationDecision("FREEZE", "UNDECLARED_CONSEQUENCE", Q64.zero(), Q64.zero(), undeclared[0])
        missing = sorted(set(p) - set(a))
        if missing:
            return ExpectationDecision("FREEZE", "MISSING_EXECUTION_CONSEQUENCE", Q64.zero(), Q64.zero(), missing[0])

        weighted = Q64.zero()
        harmful = Q64.zero()
        weight_sum = Q64.zero()
        worst_dimension: str | None = None
        worst_weighted = Q64.zero()
        for cid in sorted(p):
            before, after = p[cid], a[cid]
            if before.importance != after.importance:
                return ExpectationDecision("FREEZE", "IMPORTANCE_MODEL_CHANGED", Q64.zero(), Q64.zero(), cid)
            delta = abs(after.impact - before.impact)
            term = delta * before.importance
            weighted = weighted + term
            weight_sum = weight_sum + before.importance
            if after.impact > before.impact:
                harmful = harmful + (after.impact - before.impact) * before.importance
            if worst_dimension is None or term > worst_weighted or (term == worst_weighted and cid < worst_dimension):
                worst_dimension = cid
                worst_weighted = term

        divergence = weighted / weight_sum
        harmful_surprise = harmful / weight_sum
        if divergence > tolerance:
            return ExpectationDecision("FREEZE", "PREVIEW_DIVERGENCE", divergence, harmful_surprise, worst_dimension)
        return ExpectationDecision("PASS", "PREVIEW_ALIGNED", divergence, harmful_surprise, worst_dimension)
