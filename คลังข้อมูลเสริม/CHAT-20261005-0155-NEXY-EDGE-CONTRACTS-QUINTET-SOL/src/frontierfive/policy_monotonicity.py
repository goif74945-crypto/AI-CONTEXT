from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Mapping

from .common import Verdict, allow, freeze


@dataclass(frozen=True)
class PolicyPoint:
    point_id: str
    coords: tuple[int, ...]
    decision: str


def audit_monotonicity(
    points: Iterable[PolicyPoint],
    *,
    directions: tuple[int, ...],
    decision_rank: Mapping[str, int],
) -> Verdict:
    if not directions or any(d not in (-1, 1) for d in directions):
        return freeze("INVALID_DIRECTIONS")
    pts = sorted(points, key=lambda p: p.point_id)
    if len({p.point_id for p in pts}) != len(pts):
        return freeze("DUPLICATE_POINT_ID")
    for p in pts:
        if len(p.coords) != len(directions) or p.decision not in decision_rank:
            return freeze("INVALID_POLICY_POINT")

    violations: list[dict[str, object]] = []

    def at_least_as_risky(a: PolicyPoint, b: PolicyPoint) -> bool:
        # direction +1 => larger coordinate is riskier; -1 => smaller is riskier
        comps = [a.coords[i] >= b.coords[i] if d == 1 else a.coords[i] <= b.coords[i] for i, d in enumerate(directions)]
        strict = [a.coords[i] != b.coords[i] for i in range(len(directions))]
        return all(comps) and any(strict)

    for a, b in combinations(pts, 2):
        pairs = ((a, b), (b, a))
        for riskier, safer in pairs:
            if at_least_as_risky(riskier, safer) and decision_rank[riskier.decision] < decision_rank[safer.decision]:
                violations.append({
                    "riskier": riskier.point_id,
                    "riskier_decision": riskier.decision,
                    "safer": safer.point_id,
                    "safer_decision": safer.decision,
                })
    if violations:
        violations.sort(key=lambda v: (str(v["riskier"]), str(v["safer"])))
        return freeze("NON_MONOTONIC_POLICY", payload={"violations": violations})
    return allow({"checked_points": len(pts), "pair_count": len(pts) * (len(pts) - 1) // 2})
