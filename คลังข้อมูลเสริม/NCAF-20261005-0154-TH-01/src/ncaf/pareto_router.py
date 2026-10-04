from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .common import ContractError, require_nonempty


@dataclass(frozen=True)
class RouteCandidate:
    route_id: str
    quality: int
    latency_ms: int
    cost_units: int
    risk: int
    capabilities: frozenset[str]

    def __post_init__(self) -> None:
        require_nonempty(self.route_id, "route_id")
        if not 0 <= self.quality <= 100:
            raise ContractError("quality must be in [0, 100]")
        if self.latency_ms <= 0 or self.cost_units < 0 or not 0 <= self.risk <= 100:
            raise ContractError("invalid route metrics")


@dataclass(frozen=True)
class RouteDecision:
    selected: str
    frontier: tuple[str, ...]
    eligible: tuple[str, ...]


class ParetoRoutePlanner:
    """Chooses a nondominated route satisfying hard quality/risk/capability constraints."""

    @staticmethod
    def _dominates(a: RouteCandidate, b: RouteCandidate) -> bool:
        no_worse = (
            a.quality >= b.quality
            and a.latency_ms <= b.latency_ms
            and a.cost_units <= b.cost_units
            and a.risk <= b.risk
        )
        strictly_better = (
            a.quality > b.quality
            or a.latency_ms < b.latency_ms
            or a.cost_units < b.cost_units
            or a.risk < b.risk
        )
        return no_worse and strictly_better

    def choose(
        self,
        candidates: Iterable[RouteCandidate],
        *,
        required_capabilities: frozenset[str] = frozenset(),
        min_quality: int = 0,
        max_risk: int = 100,
    ) -> RouteDecision:
        candidates = tuple(candidates)
        if not candidates:
            raise ContractError("at least one route candidate is required")
        ids = [c.route_id for c in candidates]
        if len(ids) != len(set(ids)):
            raise ContractError("route ids must be unique")
        eligible = tuple(
            c for c in candidates
            if c.quality >= min_quality
            and c.risk <= max_risk
            and required_capabilities.issubset(c.capabilities)
        )
        if not eligible:
            raise ContractError("no route satisfies hard constraints")

        frontier = tuple(
            c for c in eligible if not any(self._dominates(other, c) for other in eligible if other != c)
        )
        # Weighted tie-break only inside the Pareto frontier. Integer arithmetic keeps decisions reproducible.
        selected = min(
            frontier,
            key=lambda c: (
                -(c.quality * 1000 - c.risk * 600 - c.cost_units * 20 - c.latency_ms // 10),
                c.cost_units,
                c.latency_ms,
                c.route_id,
            ),
        )
        return RouteDecision(
            selected=selected.route_id,
            frontier=tuple(sorted(c.route_id for c in frontier)),
            eligible=tuple(sorted(c.route_id for c in eligible)),
        )
