from dataclasses import dataclass
from typing import Dict, Iterable, Tuple
from .q64 import Q64, require_non_negative

class ProofScheduleFreeze(ValueError): pass
@dataclass(frozen=True)
class ProofTask:
    task_id:str; duration:Q64; decisive_value:Q64; dependencies:Tuple[str,...]=tuple(); authority_critical:bool=False
@dataclass(frozen=True)
class ScheduledProof:
    task_id:str; lane:int; start:Q64; end:Q64
@dataclass(frozen=True)
class ProofSchedule:
    tasks:Tuple[ScheduledProof,...]; makespan:Q64

def schedule_proofs(tasks:Iterable[ProofTask],workers:int)->ProofSchedule:
    if workers<=0: raise ValueError("workers must be > 0")
    by:Dict[str,ProofTask]={}
    for t in tasks:
        if not t.task_id or t.task_id in by: raise ValueError("invalid/duplicate task_id")
        require_non_negative(t.duration,"duration"); require_non_negative(t.decisive_value,"decisive_value")
        if t.duration==Q64.zero(): raise ValueError("duration must be > 0")
        by[t.task_id]=t
    for t in by.values():
        for d in t.dependencies:
            if d not in by: raise ProofScheduleFreeze(f"UNKNOWN_DEPENDENCY:{t.task_id}:{d}")
            if d==t.task_id: raise ProofScheduleFreeze(f"SELF_DEPENDENCY:{t.task_id}")
    lane_free=[Q64.zero() for _ in range(workers)]; scheduled={}; remaining=set(by)
    while remaining:
        ready=[by[i] for i in remaining if all(d in scheduled for d in by[i].dependencies)]
        if not ready: raise ProofScheduleFreeze("CYCLIC_PROOF_DEPENDENCY_GRAPH")
        t=min(ready,key=lambda x:(0 if x.authority_critical else 1,-(x.decisive_value/x.duration).raw,x.duration.raw,x.task_id))
        dep_end=Q64.zero()
        for d in t.dependencies: dep_end=dep_end.max(scheduled[d].end)
        _,lane,start=min((lane_free[i].max(dep_end).raw,i,lane_free[i].max(dep_end)) for i in range(workers))
        item=ScheduledProof(t.task_id,lane,start,start+t.duration); scheduled[t.task_id]=item; lane_free[lane]=item.end; remaining.remove(t.task_id)
    ordered=tuple(sorted(scheduled.values(),key=lambda x:(x.start.raw,x.lane,x.task_id))); makespan=Q64.zero()
    for x in ordered: makespan=makespan.max(x.end)
    return ProofSchedule(ordered,makespan)
