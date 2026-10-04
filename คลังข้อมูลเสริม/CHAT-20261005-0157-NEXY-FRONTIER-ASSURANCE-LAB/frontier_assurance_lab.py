"""NEXY Frontier Assurance Lab canonical single-file reference.
AI-PROPOSED / EXPERIMENTAL / NOT CANON.
"""

# ===== errors.py =====
class FreezeError(ValueError):
    """Raised when the lab cannot safely produce a decision."""

# ===== canonical.py =====
import dataclasses, hashlib, json
from collections.abc import Mapping
from typing import Any

def _normalize(value: Any) -> Any:
    if dataclasses.is_dataclass(value): return _normalize(dataclasses.asdict(value))
    if isinstance(value, Mapping): return {str(k): _normalize(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (set, frozenset)): return [_normalize(v) for v in sorted(value, key=repr)]
    if isinstance(value, tuple): return [_normalize(v) for v in value]
    if isinstance(value, list): return [_normalize(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None: return value
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")

def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

# ===== muscle.py =====
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Mapping
_ALLOWED_OPS = {"ALLOW", "DENY", "EQ", "NEQ"}

@dataclass(frozen=True)
class Constraint:
    cid: str; variable: str; op: str; values: tuple[str, ...]
    def __post_init__(self) -> None:
        if not self.cid.strip() or not self.variable.strip(): raise FreezeError("constraint id/variable must be non-empty")
        if self.op not in _ALLOWED_OPS: raise FreezeError(f"unsupported constraint op: {self.op}")
        if not self.values: raise FreezeError(f"constraint {self.cid} has no values")
        if self.op in {"EQ", "NEQ"} and len(self.values) != 1: raise FreezeError(f"{self.op} requires one value")

class ConstraintEngine:
    def __init__(self, domains: Mapping[str, Iterable[str]], *, max_constraints_per_variable: int = 22) -> None:
        if max_constraints_per_variable < 1: raise FreezeError("max_constraints_per_variable must be positive")
        self.domains = {n: tuple(sorted(set(v))) for n, v in domains.items()}
        if not self.domains or any((not n.strip() or not vals) for n, vals in self.domains.items()): raise FreezeError("invalid domain")
        self.max_constraints_per_variable = max_constraints_per_variable
    def _remaining(self, variable: str, constraints: Iterable[Constraint]) -> tuple[str, ...]:
        if variable not in self.domains: raise FreezeError(f"unknown variable: {variable}")
        remaining = set(self.domains[variable])
        for c in sorted(constraints, key=lambda x: x.cid):
            if c.variable != variable: continue
            vals = set(c.values)
            if c.op in {"ALLOW", "EQ"}: remaining.intersection_update(vals)
            elif c.op in {"DENY", "NEQ"}: remaining.difference_update(vals)
        return tuple(sorted(remaining))
    def solve(self, constraints: Iterable[Constraint]) -> dict:
        cs = tuple(sorted(constraints, key=lambda x: x.cid))
        if len({c.cid for c in cs}) != len(cs): raise FreezeError("constraint ids must be unique")
        for c in cs:
            if c.variable not in self.domains: raise FreezeError(f"unknown variable: {c.variable}")
        final_domains = {v: self._remaining(v, cs) for v in sorted(self.domains)}
        unsat_vars = [v for v, vals in final_domains.items() if not vals]
        if not unsat_vars:
            r = {"status":"SAT","final_domains":{k:list(v) for k,v in final_domains.items()},"core_ids":[],"variable":None}
            r["result_hash"] = stable_hash(r); return r
        cores=[]
        for variable in unsat_vars:
            vcs=tuple(c for c in cs if c.variable==variable)
            if len(vcs)>self.max_constraints_per_variable: raise FreezeError(f"exact core search bound exceeded for {variable}")
            found=None
            for size in range(1,len(vcs)+1):
                for subset in combinations(vcs,size):
                    if not self._remaining(variable,subset): found=tuple(c.cid for c in subset); break
                if found is not None: break
            if found is None: raise FreezeError("unable to locate unsat core")
            cores.append((len(found),found,variable))
        _, core_ids, variable=min(cores,key=lambda x:(x[0],x[1],x[2]))
        r={"status":"UNSAT","final_domains":{k:list(v) for k,v in final_domains.items()},"core_ids":list(core_ids),"variable":variable}
        r["result_hash"]=stable_hash(r); return r

# ===== parex.py =====
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Plan:
    pid:str; benefit:int; evidence:int; cost:int; latency:int; risk:int; hard_eligible:bool=True
    def __post_init__(self)->None:
        if not self.pid.strip(): raise FreezeError("plan id must be non-empty")
        for f in ("benefit","evidence","cost","latency","risk"):
            if getattr(self,f)<0: raise FreezeError(f"{f} must be non-negative")

class ParetoPruner:
    @staticmethod
    def dominates(a:Plan,b:Plan)->bool:
        no_worse=(a.benefit>=b.benefit and a.evidence>=b.evidence and a.cost<=b.cost and a.latency<=b.latency and a.risk<=b.risk)
        strict=(a.benefit>b.benefit or a.evidence>b.evidence or a.cost<b.cost or a.latency<b.latency or a.risk<b.risk)
        return no_worse and strict
    def prune(self, plans:Iterable[Plan])->dict:
        ps=tuple(sorted(plans,key=lambda p:p.pid))
        if not ps: raise FreezeError("at least one plan is required")
        if len({p.pid for p in ps})!=len(ps): raise FreezeError("plan ids must be unique")
        eligible=[p for p in ps if p.hard_eligible]
        pruned={p.pid:{"reason":"HARD_INELIGIBLE","dominated_by":[]} for p in ps if not p.hard_eligible}
        frontier=[]
        for c in eligible:
            ds=[p.pid for p in eligible if p.pid!=c.pid and self.dominates(p,c)]
            if ds: pruned[c.pid]={"reason":"PARETO_DOMINATED","dominated_by":sorted(ds)}
            else: frontier.append(c.pid)
        r={"status":"PASS" if frontier else "FREEZE","frontier":sorted(frontier),"pruned":{k:pruned[k] for k in sorted(pruned)}}
        r["result_hash"]=stable_hash(r); return r

# ===== ghostedge.py =====
from dataclasses import dataclass
from typing import Iterable, Mapping

@dataclass(frozen=True)
class PerturbationExperiment:
    eid:str; perturbed:str; observed:tuple[str,...]; failed:tuple[str,...]
    def __post_init__(self)->None:
        if not self.eid.strip() or not self.perturbed.strip(): raise FreezeError("experiment id/source required")
        if self.perturbed in self.failed: raise FreezeError("failed set must be downstream only")
        if not set(self.failed).issubset(set(self.observed)): raise FreezeError("failed must be observed")

class HiddenDependencyDetector:
    def __init__(self,*,min_hits:int=2,min_ratio_milli:int=750)->None:
        if min_hits<1 or not 0<=min_ratio_milli<=1000: raise FreezeError("invalid thresholds")
        self.min_hits=min_hits; self.min_ratio_milli=min_ratio_milli
    def detect(self,experiments:Iterable[PerturbationExperiment],declared_dependencies:Mapping[str,Iterable[str]])->dict:
        exps=tuple(sorted(experiments,key=lambda e:e.eid))
        if len({e.eid for e in exps})!=len(exps): raise FreezeError("experiment ids must be unique")
        declared={child:set(parents) for child,parents in declared_dependencies.items()}
        stats={}
        for exp in exps:
            failed=set(exp.failed)
            for child in sorted(set(exp.observed)):
                if child==exp.perturbed: continue
                edge=(exp.perturbed,child); counts=stats.setdefault(edge,[0,0]); counts[1]+=1
                if child in failed: counts[0]+=1
        candidates=[]
        for (parent,child),(hits,opportunities) in sorted(stats.items()):
            if parent in declared.get(child,set()): continue
            ratio=(hits*1000)//opportunities if opportunities else 0
            if hits>=self.min_hits and ratio>=self.min_ratio_milli:
                candidates.append({"parent":parent,"child":child,"hits":hits,"opportunities":opportunities,"ratio_milli":ratio,"reason":"CONTROLLED_PERTURBATION_FAILURE_CORRELATION"})
        r={"status":"CANDIDATES_FOUND" if candidates else "CLEAN","candidates":candidates}; r["result_hash"]=stable_hash(r); return r

# ===== recert.py =====
from dataclasses import dataclass, field
from numbers import Real
from typing import Any, Mapping
_MISSING=object(); _ALLOWED={"EXACT","NONDECREASING","PRESENT","ABSENT","ANY"}

def _flatten(value:Any,prefix:str="")->dict[str,Any]:
    if isinstance(value,Mapping):
        out={}
        for key in sorted(value,key=str): out.update(_flatten(value[key],f"{prefix}.{key}" if prefix else str(key)))
        if not value and prefix: out[prefix]={}
        return out
    return {prefix:value}

@dataclass(frozen=True)
class RecoveryPolicy:
    modes:Mapping[str,str]=field(default_factory=dict); ignore_prefixes:tuple[str,...]=()
    def __post_init__(self)->None:
        for path,mode in self.modes.items():
            if not path.strip() or mode not in _ALLOWED: raise FreezeError("invalid recovery policy")

class RecoveryCertifier:
    @staticmethod
    def _ignored(path:str,prefixes:tuple[str,...])->bool: return any(path==p or path.startswith(p+".") for p in prefixes)
    def certify(self,before:Mapping[str,Any],after:Mapping[str,Any],policy:RecoveryPolicy)->dict:
        pre,post=_flatten(before),_flatten(after); mismatches=[]
        for path in sorted(set(pre)|set(post)|set(policy.modes)):
            if self._ignored(path,policy.ignore_prefixes): continue
            mode=policy.modes.get(path,"EXACT"); a=pre.get(path,_MISSING); b=post.get(path,_MISSING); ok=False
            if mode=="ANY": ok=True
            elif mode=="EXACT": ok=a is not _MISSING and b is not _MISSING and a==b
            elif mode=="PRESENT": ok=b is not _MISSING
            elif mode=="ABSENT": ok=b is _MISSING
            elif mode=="NONDECREASING": ok=a is not _MISSING and b is not _MISSING and isinstance(a,Real) and isinstance(b,Real) and b>=a
            if not ok: mismatches.append({"path":path,"mode":mode,"before":"<MISSING>" if a is _MISSING else a,"after":"<MISSING>" if b is _MISSING else b})
        r={"status":"CERTIFIED" if not mismatches else "FREEZE","mismatches":mismatches}; r["result_hash"]=stable_hash(r); return r

# ===== obsure.py =====
from dataclasses import dataclass
from typing import Iterable
_BASE_PHASES=("INTENT","START","SUCCESS","FAILURE")
_BASE_FIELDS=frozenset({"trace_id","action_id","effect_id","timestamp"})
_HIGH_FIELDS=frozenset({"authority_ref","evidence_ref"}); _CRITICAL_FIELDS=frozenset({"state_digest"})

@dataclass(frozen=True)
class EffectSpec:
    effect_id:str; risk:str; reversible:bool
    def __post_init__(self)->None:
        if not self.effect_id.strip() or self.risk not in {"LOW","MEDIUM","HIGH","CRITICAL"}: raise FreezeError("invalid effect")

@dataclass(frozen=True)
class TelemetryEventSpec:
    name:str; effect_id:str; phase:str; fields:tuple[str,...]
    def __post_init__(self)->None:
        if not self.name.strip() or not self.effect_id.strip() or not self.phase.strip(): raise FreezeError("invalid telemetry")

class ObservabilityGate:
    def evaluate(self,effects:Iterable[EffectSpec],events:Iterable[TelemetryEventSpec])->dict:
        es=tuple(sorted(effects,key=lambda e:e.effect_id)); evs=tuple(sorted(events,key=lambda e:(e.effect_id,e.phase,e.name)))
        if not es: raise FreezeError("at least one effect required")
        if len({e.effect_id for e in es})!=len(es): raise FreezeError("effect ids must be unique")
        known={e.effect_id for e in es}; unknown=sorted({e.effect_id for e in evs if e.effect_id not in known})
        if unknown: raise FreezeError(f"telemetry references unknown effects: {unknown}")
        by={eid:[] for eid in known}
        for ev in evs: by[ev.effect_id].append(ev)
        gaps=[]
        for effect in es:
            phases=list(_BASE_PHASES)+(["COMPENSATION_START","COMPENSATION_RESULT"] if effect.reversible else [])
            fields=set(_BASE_FIELDS)
            if effect.risk in {"HIGH","CRITICAL"}: fields.update(_HIGH_FIELDS)
            if effect.risk=="CRITICAL": fields.update(_CRITICAL_FIELDS)
            present={e.phase for e in by[effect.effect_id]}
            for phase in phases:
                if phase not in present: gaps.append({"effect_id":effect.effect_id,"gap":"MISSING_PHASE","phase":phase})
            for ev in by[effect.effect_id]:
                if ev.phase in phases:
                    missing=sorted(fields-set(ev.fields))
                    if missing: gaps.append({"effect_id":effect.effect_id,"gap":"MISSING_FIELDS","event":ev.name,"phase":ev.phase,"fields":missing})
        gaps=sorted(gaps,key=lambda g:(g["effect_id"],g["gap"],g.get("phase",""),g.get("event","")))
        r={"status":"PASS" if not gaps else "FREEZE","gaps":gaps}; r["result_hash"]=stable_hash(r); return r

# ===== pipeline.py =====
from typing import Iterable, Mapping, Any

class FrontierAssurancePipeline:
    def __init__(self,domains:Mapping[str,Iterable[str]])->None:
        self.constraint_engine=ConstraintEngine(domains); self.pruner=ParetoPruner(); self.hidden=HiddenDependencyDetector(); self.recovery=RecoveryCertifier(); self.observability=ObservabilityGate()
    def assess(self,*,constraints:Iterable[Constraint],plans:Iterable[Plan],experiments:Iterable[PerturbationExperiment],declared_dependencies:Mapping[str,Iterable[str]],before_state:Mapping[str,Any],after_state:Mapping[str,Any],recovery_policy:RecoveryPolicy,effects:Iterable[EffectSpec],telemetry:Iterable[TelemetryEventSpec],freeze_on_hidden_dependencies:bool=True)->dict:
        muscle=self.constraint_engine.solve(constraints); parex=self.pruner.prune(plans); ghostedge=self.hidden.detect(experiments,declared_dependencies); recert=self.recovery.certify(before_state,after_state,recovery_policy); obsure=self.observability.evaluate(effects,telemetry)
        reasons=[]
        if muscle["status"]=="UNSAT": reasons.append("UNSAT_CONSTRAINTS")
        if parex["status"]!="PASS": reasons.append("NO_ELIGIBLE_PLAN")
        if freeze_on_hidden_dependencies and ghostedge["status"]=="CANDIDATES_FOUND": reasons.append("UNDECLARED_DEPENDENCY")
        if recert["status"]!="CERTIFIED": reasons.append("RECOVERY_NOT_EQUIVALENT")
        if obsure["status"]!="PASS": reasons.append("OBSERVABILITY_INSUFFICIENT")
        r={"status":"READY" if not reasons else "FREEZE","reasons":reasons,"muscle":muscle,"parex":parex,"ghostedge":ghostedge,"recert":recert,"obsure":obsure}; r["result_hash"]=stable_hash(r); return r
