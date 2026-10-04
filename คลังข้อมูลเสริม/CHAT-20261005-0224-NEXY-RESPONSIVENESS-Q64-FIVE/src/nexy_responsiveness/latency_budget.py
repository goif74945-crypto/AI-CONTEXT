from dataclasses import dataclass
from typing import Iterable, Tuple
from .q64 import Q64, require_non_negative

class LatencyBudgetFreeze(ValueError): pass

@dataclass(frozen=True)
class StageRequirement:
    stage_id:str; minimum:Q64; weight:Q64
@dataclass(frozen=True)
class StageAllocation:
    stage_id:str; minimum:Q64; allocated:Q64
@dataclass(frozen=True)
class LatencyBudgetPlan:
    total_budget:Q64; allocations:Tuple[StageAllocation,...]; slack:Q64

def compile_latency_budget(total_budget:Q64, stages:Iterable[StageRequirement])->LatencyBudgetPlan:
    require_non_negative(total_budget,"total_budget"); ss=sorted(tuple(stages),key=lambda s:s.stage_id)
    if not ss: return LatencyBudgetPlan(total_budget,tuple(),total_budget)
    if len({s.stage_id for s in ss})!=len(ss): raise ValueError("duplicate stage_id")
    for s in ss:
        require_non_negative(s.minimum,"minimum"); require_non_negative(s.weight,"weight")
    min_sum=Q64.zero(); weight_sum=Q64.zero()
    for s in ss: min_sum=min_sum+s.minimum; weight_sum=weight_sum+s.weight
    if min_sum>total_budget: raise LatencyBudgetFreeze("MINIMUM_VERIFICATION_LATENCY_EXCEEDS_SLO")
    extra=total_budget.raw-min_sum.raw
    if weight_sum==Q64.zero():
        return LatencyBudgetPlan(total_budget,tuple(StageAllocation(s.stage_id,s.minimum,s.minimum) for s in ss),Q64.from_raw(extra))
    weighted=[s for s in ss if s.weight>Q64.zero()]; shares={}; used=0
    for s in weighted[:-1]:
        sr=(extra*s.weight.raw)//weight_sum.raw; shares[s.stage_id]=sr; used+=sr
    shares[weighted[-1].stage_id]=extra-used
    alloc=tuple(StageAllocation(s.stage_id,s.minimum,s.minimum+Q64.from_raw(shares.get(s.stage_id,0))) for s in ss)
    if sum(a.allocated.raw for a in alloc)!=total_budget.raw: raise AssertionError("budget conservation")
    return LatencyBudgetPlan(total_budget,alloc,Q64.zero())
