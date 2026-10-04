from __future__ import annotations

from dataclasses import dataclass

from .fixed import Q64


@dataclass(frozen=True, slots=True)
class ReversibilityPolicy:
    initial_reversibility: Q64
    retention_per_tick: Q64
    minimum_reversibility: Q64
    hard_deadline_tick: int

    def __post_init__(self) -> None:
        zero, one = Q64.zero(), Q64.one()
        if not all(isinstance(getattr(self, name), Q64) for name in (
            "initial_reversibility", "retention_per_tick", "minimum_reversibility"
        )):
            raise TypeError("reversibility values must be Q64")
        if not (zero <= self.initial_reversibility <= one):
            raise ValueError("initial_reversibility must be in [0,1]")
        if not (zero < self.retention_per_tick <= one):
            raise ValueError("retention_per_tick must be in (0,1]")
        if not (zero <= self.minimum_reversibility <= self.initial_reversibility):
            raise ValueError("minimum_reversibility must be in [0, initial]")
        if type(self.hard_deadline_tick) is not int or self.hard_deadline_tick < 0:
            raise ValueError("hard_deadline_tick must be a non-negative int")


@dataclass(frozen=True, slots=True)
class ReversibilityDecision:
    status: str
    reason: str
    current_reversibility: Q64
    latest_safe_tick: int


class ReversibilityHalfLifeScheduler:
    """Quantify rollback-quality decay and stop execution before reversibility collapses."""

    @staticmethod
    def _pow(base: Q64, exponent: int) -> Q64:
        if exponent < 0:
            raise ValueError("exponent must be non-negative")
        result = Q64.one()
        factor = base
        n = exponent
        while n:
            if n & 1:
                result = result * factor
            n >>= 1
            if n:
                factor = factor * factor
        return result

    def _at(self, policy: ReversibilityPolicy, tick: int) -> Q64:
        return policy.initial_reversibility * self._pow(policy.retention_per_tick, tick)

    def assess(
        self,
        policy: ReversibilityPolicy,
        *,
        current_tick: int,
        checkpoint_guard_ticks: int = 0,
    ) -> ReversibilityDecision:
        if type(current_tick) is not int or current_tick < 0:
            raise ValueError("current_tick must be a non-negative int")
        if type(checkpoint_guard_ticks) is not int or checkpoint_guard_ticks < 0:
            raise ValueError("checkpoint_guard_ticks must be a non-negative int")
        if current_tick > policy.hard_deadline_tick:
            return ReversibilityDecision("FREEZE", "HARD_DEADLINE_EXPIRED", Q64.zero(), policy.hard_deadline_tick)

        current = self._at(policy, current_tick)
        if current < policy.minimum_reversibility:
            return ReversibilityDecision("FREEZE", "REVERSIBILITY_BELOW_FLOOR", current, current_tick - 1)

        lo, hi = current_tick, policy.hard_deadline_tick
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._at(policy, mid) >= policy.minimum_reversibility:
                lo = mid
            else:
                hi = mid - 1
        latest = lo

        if latest - current_tick <= checkpoint_guard_ticks and current_tick < latest:
            return ReversibilityDecision("CHECKPOINT_REQUIRED", "SAFE_WINDOW_NEAR_EDGE", current, latest)
        if latest == current_tick and checkpoint_guard_ticks > 0:
            return ReversibilityDecision("CHECKPOINT_REQUIRED", "SAFE_WINDOW_AT_EDGE", current, latest)
        return ReversibilityDecision("PASS", "WITHIN_REVERSIBILITY_WINDOW", current, latest)
