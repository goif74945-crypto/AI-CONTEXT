from dataclasses import dataclass
from typing import Iterable, Tuple
from .q64 import Q64, require_non_negative, require_unit_interval

@dataclass(frozen=True)
class Notice:
    notice_id:str; severity:Q64; urgency:Q64; user_value:Q64; interruption_cost:Q64
    blocker:bool=False; security:bool=False; authority_conflict:bool=False
    @property
    def mandatory(self)->bool: return self.blocker or self.security or self.authority_conflict
@dataclass(frozen=True)
class AttentionPlan:
    surface_now:Tuple[str,...]; deferred:Tuple[str,...]; mandatory:Tuple[str,...]; optional_cost:Q64; mandatory_cost:Q64; mandatory_budget_overrun:Q64

def plan_attention(notices:Iterable[Notice],optional_budget:Q64,max_optional:int)->AttentionPlan:
    require_non_negative(optional_budget,"optional_budget")
    if max_optional<0: raise ValueError("max_optional")
    seen=set(); mandatory=[]; optional=[]
    for n in notices:
        if not n.notice_id or n.notice_id in seen: raise ValueError("invalid/duplicate notice")
        seen.add(n.notice_id); require_unit_interval(n.severity,"severity"); require_unit_interval(n.urgency,"urgency"); require_unit_interval(n.user_value,"user_value"); require_non_negative(n.interruption_cost,"interruption_cost")
        if n.mandatory: mandatory.append(n)
        else: optional.append((n,(n.severity*n.urgency)+n.user_value-n.interruption_cost))
    mandatory.sort(key=lambda n:(-n.severity.raw,-n.urgency.raw,n.notice_id)); optional.sort(key=lambda x:(-x[1].raw,x[0].notice_id))
    mandatory_cost=Q64.zero()
    for n in mandatory: mandatory_cost=mandatory_cost+n.interruption_cost
    selected=[]; deferred=[]; cost=Q64.zero()
    for n,score in optional:
        if score<=Q64.zero() or len(selected)>=max_optional or cost+n.interruption_cost>optional_budget: deferred.append(n.notice_id)
        else: selected.append(n.notice_id); cost=cost+n.interruption_cost
    mids=tuple(n.notice_id for n in mandatory); over=mandatory_cost-optional_budget if mandatory_cost>optional_budget else Q64.zero()
    return AttentionPlan(mids+tuple(selected),tuple(sorted(deferred)),mids,cost,mandatory_cost,over)
