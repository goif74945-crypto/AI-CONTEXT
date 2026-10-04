from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .fixed import Q64


@dataclass(frozen=True, slots=True)
class LinearFeature:
    feature_id: str
    weight: Q64
    center: Q64
    radius: Q64

    def __post_init__(self) -> None:
        if not self.feature_id.strip():
            raise ValueError("feature_id must be non-empty")
        if not all(isinstance(getattr(self, name), Q64) for name in ("weight", "center", "radius")):
            raise TypeError("weight, center, radius must be Q64")
        if self.radius < Q64.zero():
            raise ValueError("radius must be non-negative")


@dataclass(frozen=True, slots=True)
class RobustnessDecision:
    status: str
    reason: str
    nominal: Q64
    lower_bound: Q64
    upper_bound: Q64
    robust_margin: Q64


class DecisionRobustnessEngine:
    """Certify that a linear threshold decision cannot flip inside a bounded input box."""

    def certify(
        self,
        features: Iterable[LinearFeature],
        *,
        bias: Q64,
        threshold: Q64,
    ) -> RobustnessDecision:
        items = tuple(sorted(features, key=lambda x: x.feature_id))
        if not items:
            raise ValueError("at least one feature is required")
        if len({x.feature_id for x in items}) != len(items):
            raise ValueError("duplicate feature_id")
        if not isinstance(bias, Q64) or not isinstance(threshold, Q64):
            raise TypeError("bias and threshold must be Q64")

        nominal = bias
        delta = Q64.zero()
        for item in items:
            nominal = nominal + item.weight * item.center
            delta = delta + abs(item.weight) * item.radius
        lower = nominal - delta
        upper = nominal + delta

        if lower >= threshold:
            return RobustnessDecision(
                "CERTIFY_ALLOW", "BOX_ENTIRELY_ABOVE_THRESHOLD", nominal, lower, upper, lower - threshold
            )
        if upper < threshold:
            return RobustnessDecision(
                "CERTIFY_DENY", "BOX_ENTIRELY_BELOW_THRESHOLD", nominal, lower, upper, threshold - upper
            )
        return RobustnessDecision(
            "FREEZE", "PERTURBATION_CAN_FLIP_DECISION", nominal, lower, upper, Q64.zero()
        )
