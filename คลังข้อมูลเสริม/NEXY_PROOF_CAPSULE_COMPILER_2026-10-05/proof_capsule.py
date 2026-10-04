# PROPOSAL ONLY: reference research for AI-CONTEXT, not NEXY.AI production authority.
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, heapq, json, re
from typing import Literal, Mapping, Sequence

Status = Literal["PASS", "FAIL", "CONFLICT", "NOT_VERIFIED"]
EClass = Literal["E0","E1","E2","E3","E4","E5","E6","E7"]
VALID_STATUS={"PASS","FAIL","CONFLICT","NOT_VERIFIED"}; VALID_CLASS={f"E{i}" for i in range(8)}

@dataclass(frozen=True, slots=True)
class Claim:
    id:str; statement:str; target:str; version:str; accepted:tuple[EClass,...]; required:bool=True; material:bool=True

@dataclass(frozen=True, slots=True)
class Evidence:
    id:str; source:str; status:Status; eclass:EClass; target:str; version:str; supports:tuple[str,...]
    rank:int; observed_at:str; valid_until:str|None=None; cost:int=1; digest:str|None=None

@dataclass(frozen=True, slots=True)
class Policy:
    max_items:int=12; max_cost:int=48; strict_refs:bool=True; disclose_dissent:bool=True; require_digest:bool=True

@dataclass(frozen=True, slots=True)
class Capsule:
    status:Literal["PASS","FREEZE"]; capsule_id:str; as_of:str; claims:tuple[str,...]; evidence:tuple[str,...]
    coverage:Mapping[str,tuple[str,...]]; dissent:Mapping[str,tuple[str,...]]; reasons:tuple[str,...]; cost:int
    metadata:Mapping[str,object]=field(default_factory=dict)
    def to_dict(self)->dict[str,object]:
        return {"status":self.status,"capsule_id":self.capsule_id,"as_of":self.as_of,"claims":list(self.claims),
                "evidence":list(self.evidence),"coverage":{k:list(v) for k,v in sorted(self.coverage.items())},
                "dissent":{k:list(v) for k,v in sorted(self.dissent.items())},"reasons":list(self.reasons),
                "cost":self.cost,"metadata":dict(self.metadata)}

class ContractError(ValueError): pass

def _time(s:str)->datetime:
    try: d=datetime.fromisoformat(s[:-1]+"+00:00" if s.endswith("Z") else s)
    except ValueError as e: raise ContractError(f"invalid timestamp:{s}") from e
    if d.tzinfo is None: raise ContractError(f"naive timestamp:{s}")
    return d.astimezone(timezone.utc)

def _canon(x:object)->str: return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def _hash(x:object,prefix:str)->str: return f"{prefix}:"+hashlib.sha256(_canon(x).encode()).hexdigest()

def _validate(claims:Sequence[Claim], evidence:Sequence[Evidence], as_of:str, p:Policy)->None:
    _time(as_of)
    if p.max_items<1 or p.max_cost<1: raise ContractError("invalid budget")
    if not any(c.required for c in claims): raise ContractError("no required claim")
    if len({c.id for c in claims})!=len(claims): raise ContractError("duplicate claim id")
    if len({e.id for e in evidence})!=len(evidence): raise ContractError("duplicate evidence id")
    for c in claims:
        if not all((c.id.strip(),c.statement.strip(),c.target.strip(),c.version.strip())) or not c.accepted or any(x not in VALID_CLASS for x in c.accepted):
            raise ContractError(f"invalid claim:{c.id!r}")
    for e in evidence:
        if len(set(e.supports))!=len(e.supports): raise ContractError(f"duplicate support:{e.id}")
        if not all((e.id.strip(),e.source.strip(),e.target.strip(),e.version.strip())) or e.status not in VALID_STATUS or e.eclass not in VALID_CLASS or e.rank<0 or e.cost<1:
            raise ContractError(f"invalid evidence:{e.id!r}")
        if p.require_digest and (e.digest is None or re.fullmatch(r"sha256:[0-9a-f]{64}",e.digest) is None): raise ContractError(f"invalid digest:{e.id}")
        obs=_time(e.observed_at)
        if e.valid_until is not None and _time(e.valid_until)<obs: raise ContractError(f"invalid validity:{e.id}")

def _commitment(claims:Sequence[Claim], evidence:Sequence[Evidence], as_of:str, p:Policy)->str:
    cs=[{"id":c.id,"statement":c.statement,"target":c.target,"version":c.version,"accepted":sorted(c.accepted),"required":c.required,"material":c.material} for c in sorted(claims,key=lambda x:x.id)]
    es=[{"id":e.id,"source":e.source,"status":e.status,"eclass":e.eclass,"target":e.target,"version":e.version,"supports":sorted(e.supports),"rank":e.rank,"observed_at":e.observed_at,"valid_until":e.valid_until,"cost":e.cost,"digest":e.digest} for e in sorted(evidence,key=lambda x:x.id)]
    return _hash({"schema":"proof-input/v1-proposal","as_of":as_of,"claims":cs,"evidence":es,"policy":p.__dict__ if hasattr(p,"__dict__") else {"max_items":p.max_items,"max_cost":p.max_cost,"strict_refs":p.strict_refs,"disclose_dissent":p.disclose_dissent,"require_digest":p.require_digest}},"pci1")

def _cover(required:Sequence[Claim], winners:dict[str,list[Evidence]])->tuple[Evidence,...]:
    uncovered={c.id for c in required}; items={}; cov=defaultdict(set); adj=defaultdict(set)
    for cid,evs in winners.items():
        for e in evs: items[e.id]=e; cov[e.id].add(cid); adj[cid].add(e.id)
    score={eid:len(v) for eid,v in cov.items()}; gen={eid:0 for eid in items}; active=set(items)
    heap=[(-score[eid],items[eid].cost,eid,0) for eid in items]; heapq.heapify(heap); selected=[]
    while uncovered:
        winner=None
        while heap:
            neg,_,eid,g=heapq.heappop(heap)
            if eid in active and g==gen[eid] and -neg==score[eid] and score[eid]>0: winner=eid; break
        if winner is None: raise ContractError("coverage invariant")
        selected.append(items[winner]); active.remove(winner); newly=cov[winner]&uncovered
        for cid in sorted(newly):
            uncovered.remove(cid)
            for eid in sorted(adj[cid]):
                if eid in active:
                    score[eid]-=1; gen[eid]+=1
                    if score[eid]>0: heapq.heappush(heap,(-score[eid],items[eid].cost,eid,gen[eid]))
    return tuple(sorted(selected,key=lambda x:x.id))

def compile_capsule(claims:Sequence[Claim], evidence:Sequence[Evidence], *, as_of:str, policy:Policy|None=None)->Capsule:
    p=policy or Policy(); _validate(claims,evidence,as_of,p); now=_time(as_of); commit=_commitment(claims,evidence,as_of,p)
    by=defaultdict(list); known={c.id for c in claims}; unknown=[]
    for e in evidence:
        for cid in e.supports: (by[cid].append(e) if cid in known else unknown.append(f"{e.id}->{cid}"))
    reasons=[]; dissent={}; winners={}; required=tuple(sorted((c for c in claims if c.required),key=lambda x:x.id))
    if unknown and p.strict_refs: reasons.append("UNKNOWN_REF:"+",".join(sorted(unknown)))
    for c in required:
        app=[e for e in by[c.id] if e.eclass in c.accepted and e.target==c.target and e.version==c.version and _time(e.observed_at)<=now and (e.valid_until is None or _time(e.valid_until)>=now)]
        if not app: reasons.append(f"NO_EVIDENCE:{c.id}"); continue
        rank=min(e.rank for e in app); top=sorted((e for e in app if e.rank==rank),key=lambda x:x.id); states={e.status for e in top}
        if c.material and ("CONFLICT" in states or ("PASS" in states and "FAIL" in states)): reasons.append(f"CONFLICT:{c.id}"); continue
        if "FAIL" in states and "PASS" not in states: reasons.append(f"FAIL:{c.id}"); continue
        if "PASS" not in states: reasons.append(f"NOT_VERIFIED:{c.id}"); continue
        winners[c.id]=[e for e in top if e.status=="PASS"]
        if p.disclose_dissent:
            ds=sorted(e.id for e in app if e.status in {"FAIL","CONFLICT"} and (e.rank>rank or (not c.material and e.rank==rank)))
            if ds: dissent[c.id]=tuple(ds)
    def freeze(rs:Sequence[str])->Capsule:
        rr=tuple(sorted(set(rs))); payload={"schema":"proof-capsule/v1-proposal","status":"FREEZE","input":commit,"as_of":as_of,"claims":[c.id for c in required],"reasons":rr,"dissent":dissent}
        return Capsule("FREEZE",_hash(payload,"pc1"),as_of,tuple(c.id for c in required),(),{},dissent,rr,0,{"input_commitment":commit})
    if reasons: return freeze(reasons)
    selected=_cover(required,winners); cost=sum(e.cost for e in selected)
    if len(selected)>p.max_items: reasons.append(f"ITEM_BUDGET:{len(selected)}>{p.max_items}")
    if cost>p.max_cost: reasons.append(f"COST_BUDGET:{cost}>{p.max_cost}")
    if reasons: return freeze(reasons)
    ids={e.id for e in selected}; coverage={c.id:tuple(sorted(e.id for e in winners[c.id] if e.id in ids)) for c in required}
    payload={"schema":"proof-capsule/v1-proposal","status":"PASS","input":commit,"as_of":as_of,"claims":[c.id for c in required],"evidence":[e.id for e in selected],"coverage":coverage,"dissent":dissent,"cost":cost}
    return Capsule("PASS",_hash(payload,"pc1"),as_of,tuple(c.id for c in required),tuple(e.id for e in selected),coverage,dissent,(),cost,{"input_commitment":commit,"algorithm":"authority-first incremental greedy cover"})
