from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import heapq
import json
from typing import Iterable, Mapping

class ScheduleInputError(ValueError): pass

@dataclass(frozen=True, slots=True)
class WorkItem:
    task_id: str
    duration_ms: int
    resource: str
    dependencies: tuple[str, ...] = ()
    produces_evidence: int = 0
    requires_dependency_evidence: int = 0

@dataclass(frozen=True, slots=True)
class ScheduledItem:
    task_id: str
    start_ms: int
    end_ms: int
    resource: str
    slot: int
    critical_path_ms: int

@dataclass(frozen=True, slots=True)
class ScheduleResult:
    status: str
    makespan_ms: int
    schedule: tuple[ScheduledItem, ...]
    reason_codes: tuple[str, ...]
    fingerprint: str

def _clean(value: str, field: str) -> str:
    if not isinstance(value, str): raise ScheduleInputError(f"{field}:NOT_STRING")
    value=value.strip()
    if not value: raise ScheduleInputError(f"{field}:EMPTY")
    return value

def _normalize(items: Iterable[WorkItem]) -> dict[str, WorkItem]:
    result={}
    for item in items:
        tid=_clean(item.task_id,"task_id")
        if tid in result: raise ScheduleInputError(f"DUPLICATE_TASK:{tid}")
        resource=_clean(item.resource,f"{tid}.resource")
        if not isinstance(item.duration_ms,int) or item.duration_ms<=0: raise ScheduleInputError(f"{tid}:INVALID_DURATION")
        if not isinstance(item.produces_evidence,int) or not 0<=item.produces_evidence<=7: raise ScheduleInputError(f"{tid}:INVALID_PRODUCED_EVIDENCE")
        if not isinstance(item.requires_dependency_evidence,int) or not 0<=item.requires_dependency_evidence<=7: raise ScheduleInputError(f"{tid}:INVALID_REQUIRED_EVIDENCE")
        deps=tuple(sorted({_clean(d,f"{tid}.dependency") for d in item.dependencies}))
        if tid in deps: raise ScheduleInputError(f"{tid}:SELF_DEPENDENCY")
        result[tid]=WorkItem(tid,item.duration_ms,resource,deps,item.produces_evidence,item.requires_dependency_evidence)
    if not result: raise ScheduleInputError("NO_TASKS")
    for item in result.values():
        missing=set(item.dependencies)-result.keys()
        if missing: raise ScheduleInputError(f"{item.task_id}:UNKNOWN_DEPENDENCY:{sorted(missing)}")
    return result

def _topological(items: Mapping[str,WorkItem]):
    successors={tid:[] for tid in items}; indegree={tid:0 for tid in items}
    for tid,item in items.items():
        for dep in item.dependencies: successors[dep].append(tid); indegree[tid]+=1
    for s in successors.values(): s.sort()
    ready=[tid for tid,deg in indegree.items() if deg==0]; heapq.heapify(ready); order=[]
    while ready:
        tid=heapq.heappop(ready); order.append(tid)
        for nxt in successors[tid]:
            indegree[nxt]-=1
            if indegree[nxt]==0: heapq.heappush(ready,nxt)
    if len(order)!=len(items): raise ScheduleInputError("DEPENDENCY_CYCLE")
    return order,successors

def _critical_paths(items,topo,successors):
    cp={}
    for tid in reversed(topo): cp[tid]=items[tid].duration_ms+max((cp[s] for s in successors[tid]),default=0)
    return cp

def schedule_work(items: Iterable[WorkItem], resource_capacity: Mapping[str,int]) -> ScheduleResult:
    tasks=_normalize(items); topo,successors=_topological(tasks); cp=_critical_paths(tasks,topo,successors)
    capacities={}
    for resource,count in sorted(resource_capacity.items()):
        resource=_clean(resource,"resource_capacity.key")
        if not isinstance(count,int) or count<=0: raise ScheduleInputError(f"INVALID_CAPACITY:{resource}")
        capacities[resource]=count
    missing=sorted({t.resource for t in tasks.values()}-capacities.keys())
    if missing: raise ScheduleInputError(f"MISSING_RESOURCE_CAPACITY:{missing}")
    gaps=[]
    for task in tasks.values():
        if task.dependencies and task.requires_dependency_evidence:
            weak=[d for d in task.dependencies if tasks[d].produces_evidence<task.requires_dependency_evidence]
            if weak: gaps.append(f"{task.task_id}<-{','.join(sorted(weak))}")
    if gaps: return _finalize("FREEZE",0,(),("PLANNED_EVIDENCE_GAP",*sorted(gaps)),tasks,capacities)

    indegree={tid:len(t.dependencies) for tid,t in tasks.items()}
    pending={r:[] for r in capacities}; runnable={r:[] for r in capacities}
    slots={r:[0]*count for r,count in capacities.items()}; end_time={}; scheduled=[]
    def push_ready(tid):
        task=tasks[tid]; release=max((end_time[d] for d in task.dependencies),default=0)
        heapq.heappush(pending[task.resource],(release,-cp[tid],-task.produces_evidence,tid))
    for tid,degree in indegree.items():
        if degree==0: push_ready(tid)
    remaining=len(tasks)
    while remaining:
        candidates=[]
        for resource in sorted(capacities):
            rs=slots[resource]; slot=min(range(len(rs)),key=lambda i:(rs[i],i)); slot_ready=rs[slot]
            pheap=pending[resource]; rheap=runnable[resource]
            while pheap and pheap[0][0]<=slot_ready:
                release,negcp,negev,tid=heapq.heappop(pheap); heapq.heappush(rheap,(negcp,negev,tid,release))
            if rheap:
                negcp,negev,tid,release=rheap[0]; candidates.append((slot_ready,negcp,negev,tid,resource,slot,"RUNNABLE"))
            elif pheap:
                release,negcp,negev,tid=pheap[0]; candidates.append((max(slot_ready,release),negcp,negev,tid,resource,slot,"PENDING"))
        if not candidates: raise ScheduleInputError("INTERNAL_SCHEDULER_STALL")
        start,_,_,tid,resource,slot,source=min(candidates)
        if source=="RUNNABLE": _,_,popped,_=heapq.heappop(runnable[resource])
        else: _,_,_,popped=heapq.heappop(pending[resource])
        if popped!=tid: raise ScheduleInputError("INTERNAL_SCHEDULER_HEAP_MISMATCH")
        task=tasks[tid]; end=start+task.duration_ms; slots[resource][slot]=end; end_time[tid]=end
        scheduled.append(ScheduledItem(tid,start,end,resource,slot,cp[tid])); remaining-=1
        for nxt in successors[tid]:
            indegree[nxt]-=1
            if indegree[nxt]==0: push_ready(nxt)
    makespan=max(end_time.values(),default=0); scheduled.sort(key=lambda x:(x.start_ms,x.end_ms,x.resource,x.slot,x.task_id))
    return _finalize("PLAN_READY",makespan,tuple(scheduled),(),tasks,capacities)

def _finalize(status,makespan,schedule,reasons,tasks,capacities):
    payload={"status":status,"makespan_ms":makespan,"schedule":[{"task_id":s.task_id,"start_ms":s.start_ms,"end_ms":s.end_ms,"resource":s.resource,"slot":s.slot,"critical_path_ms":s.critical_path_ms} for s in schedule],"reason_codes":list(reasons),"tasks":[{"task_id":t.task_id,"duration_ms":t.duration_ms,"resource":t.resource,"dependencies":list(t.dependencies),"produces_evidence":t.produces_evidence,"requires_dependency_evidence":t.requires_dependency_evidence} for t in sorted(tasks.values(),key=lambda x:x.task_id)],"capacities":dict(sorted(capacities.items()))}
    fingerprint=sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return ScheduleResult(status,makespan,schedule,tuple(reasons),fingerprint)
