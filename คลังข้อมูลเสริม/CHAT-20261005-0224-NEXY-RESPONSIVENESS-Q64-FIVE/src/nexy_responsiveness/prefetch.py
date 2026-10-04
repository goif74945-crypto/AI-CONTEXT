from dataclasses import dataclass
from typing import Iterable, Tuple
from .q64 import Q64, require_non_negative, require_unit_interval

@dataclass(frozen=True)
class PrefetchCandidate:
    candidate_id: str; hit_probability: Q64; latency_saved: Q64; resource_cost: Q64; stale_risk: Q64
    read_only: bool = True; dependencies_ready: bool = True
    def validate(self) -> None:
        if not self.candidate_id: raise ValueError("candidate_id is required")
        require_unit_interval(self.hit_probability, "hit_probability")
        require_non_negative(self.latency_saved, "latency_saved")
        require_non_negative(self.resource_cost, "resource_cost")
        require_unit_interval(self.stale_risk, "stale_risk")

@dataclass(frozen=True)
class PrefetchDecision:
    selected: Tuple[str, ...]; rejected: Tuple[Tuple[str, str], ...]; total_cost: Q64; estimated_net_gain: Q64

def plan_prefetch(candidates: Iterable[PrefetchCandidate], resource_budget: Q64, stale_penalty: Q64) -> PrefetchDecision:
    require_non_negative(resource_budget, "resource_budget"); require_non_negative(stale_penalty, "stale_penalty")
    seen=set(); eligible=[]; rejected=[]
    for c in candidates:
        c.validate()
        if c.candidate_id in seen: raise ValueError(f"duplicate candidate_id: {c.candidate_id}")
        seen.add(c.candidate_id)
        if not c.read_only: rejected.append((c.candidate_id,"MUTATING_SPECULATION_FORBIDDEN")); continue
        if not c.dependencies_ready: rejected.append((c.candidate_id,"DEPENDENCIES_NOT_READY")); continue
        gain=(c.hit_probability*c.latency_saved)-(c.stale_risk*stale_penalty)
        if gain <= Q64.zero(): rejected.append((c.candidate_id,"NON_POSITIVE_NET_GAIN")); continue
        density=gain if c.resource_cost==Q64.zero() else gain/c.resource_cost
        eligible.append((c,gain,density))
    eligible.sort(key=lambda x:(-x[2].raw,-x[1].raw,x[0].candidate_id))
    selected=[]; cost=Q64.zero(); total_gain=Q64.zero()
    for c,gain,_ in eligible:
        if cost+c.resource_cost <= resource_budget:
            selected.append(c.candidate_id); cost=cost+c.resource_cost; total_gain=total_gain+gain
        else: rejected.append((c.candidate_id,"RESOURCE_BUDGET_EXCEEDED"))
    return PrefetchDecision(tuple(selected),tuple(sorted(rejected)),cost,total_gain)
