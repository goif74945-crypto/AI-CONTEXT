from dataclasses import dataclass
from typing import Iterable, Tuple
from .q64 import Q64, require_non_negative, require_unit_interval

class WarmsetFreeze(ValueError): pass
@dataclass(frozen=True)
class ContextChunk:
    chunk_id:str; tokens:int; authority_rank:int; freshness:Q64; reuse_probability:Q64; dependency_distance:Q64; counterevidence:bool=False
@dataclass(frozen=True)
class WarmsetPlan:
    resident:Tuple[str,...]; evicted:Tuple[str,...]; used_tokens:int; pinned_tokens:int

def plan_warmset(chunks:Iterable[ContextChunk],token_budget:int,authority_pin_rank:int=2)->WarmsetPlan:
    if token_budget<0 or authority_pin_rank<=0: raise ValueError("invalid budget/rank")
    seen=set(); pinned=[]; optional=[]
    for c in chunks:
        if not c.chunk_id or c.chunk_id in seen or c.tokens<=0 or c.authority_rank<=0: raise ValueError("invalid/duplicate chunk")
        seen.add(c.chunk_id); require_unit_interval(c.freshness,"freshness"); require_unit_interval(c.reuse_probability,"reuse_probability"); require_non_negative(c.dependency_distance,"dependency_distance")
        if c.authority_rank<=authority_pin_rank or c.counterevidence: pinned.append(c)
        else:
            utility=(c.reuse_probability*c.freshness)/(Q64.one()+c.dependency_distance)
            optional.append((c,utility,utility/Q64.from_int(c.tokens)))
    pinned.sort(key=lambda c:(c.authority_rank,c.chunk_id)); used=sum(c.tokens for c in pinned)
    if used>token_budget: raise WarmsetFreeze("AUTHORITY_AND_COUNTEREVIDENCE_EXCEED_CONTEXT_BUDGET")
    optional.sort(key=lambda x:(-x[2].raw,-x[1].raw,x[0].chunk_id)); resident=[c.chunk_id for c in pinned]; evicted=[]
    for c,_,_ in optional:
        if used+c.tokens<=token_budget: resident.append(c.chunk_id); used+=c.tokens
        else: evicted.append(c.chunk_id)
    return WarmsetPlan(tuple(resident),tuple(sorted(evicted)),used,sum(c.tokens for c in pinned))
