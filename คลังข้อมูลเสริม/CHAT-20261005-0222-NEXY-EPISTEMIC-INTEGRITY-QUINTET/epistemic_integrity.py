from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import isfinite
from typing import Any, Mapping, Sequence

@dataclass(frozen=True)
class ClaimNode:
    claim_id: str
    dependencies: tuple[str, ...]

@dataclass(frozen=True)
class CircularityAuditResult:
    status: str
    circular_claims: tuple[str, ...]
    unknown_dependencies: tuple[str, ...]
    grounded_claims: tuple[str, ...]

class EpistemicCircularityFirewall:
    def audit(self, claims: Sequence[ClaimNode], evidence_ids: set[str] | frozenset[str]) -> CircularityAuditResult:
        ids=[c.claim_id for c in claims]
        if any(not x for x in ids) or len(set(ids)) != len(ids):
            raise ValueError("claim IDs must be non-empty and unique")
        by_id={c.claim_id:c for c in claims}; unknown=set(); graph={}
        for c in claims:
            edges=[]
            for d in c.dependencies:
                if d.startswith("c:"):
                    t=d[2:]; edges.append(t) if t in by_id else unknown.add(d)
                elif d.startswith("e:"):
                    if d[2:] not in evidence_ids: unknown.add(d)
                else: unknown.add(d)
            graph[c.claim_id]=tuple(edges)
        circular=self._cycles(graph); grounded=set(); changed=True
        while changed:
            changed=False
            for c in claims:
                if c.claim_id in grounded or c.claim_id in circular: continue
                ok=True
                for d in c.dependencies:
                    if d in unknown: ok=False; break
                    if d.startswith("c:") and d[2:] not in grounded: ok=False; break
                    if d.startswith("e:") and d[2:] not in evidence_ids: ok=False; break
                    if not d.startswith(("c:","e:")): ok=False; break
                if ok: grounded.add(c.claim_id); changed=True
        status="PASS" if not circular and not unknown and len(grounded)==len(claims) else "FREEZE"
        return CircularityAuditResult(status,tuple(sorted(circular)),tuple(sorted(unknown)),tuple(sorted(grounded)))

    @staticmethod
    def _cycles(graph: Mapping[str, Sequence[str]]) -> set[str]:
        idx=0; stack=[]; indices={}; low={}; on=set(); cycles=set()
        def visit(v):
            nonlocal idx
            indices[v]=low[v]=idx; idx+=1; stack.append(v); on.add(v)
            for w in graph.get(v,()):
                if w not in indices: visit(w); low[v]=min(low[v],low[w])
                elif w in on: low[v]=min(low[v],indices[w])
            if low[v]==indices[v]:
                comp=[]
                while True:
                    w=stack.pop(); on.remove(w); comp.append(w)
                    if w==v: break
                if len(comp)>1 or (len(comp)==1 and v in graph.get(v,())): cycles.update(comp)
        for v in sorted(graph):
            if v not in indices: visit(v)
        return cycles

@dataclass(frozen=True)
class DecisionObservation:
    observation_id: str
    dimensions: Mapping[str,int|float]
    verdict: str

@dataclass(frozen=True)
class MonotonicityRule:
    dimension: str
    direction: str
    verdict_order: tuple[str,...]

@dataclass(frozen=True)
class MonotonicityAuditResult:
    status: str
    violations: tuple[tuple[str,str],...]
    conflicts: tuple[tuple[int|float,tuple[str,...]],...]

class DecisionMonotonicityAuditor:
    def audit(self, obs: Sequence[DecisionObservation], rule: MonotonicityRule) -> MonotonicityAuditResult:
        if rule.direction not in {"NONINCREASING","NONDECREASING","EQUAL"}: raise ValueError("invalid direction")
        if len(set(rule.verdict_order))!=len(rule.verdict_order): raise ValueError("duplicate verdict order")
        ids=[o.observation_id for o in obs]
        if len(set(ids))!=len(ids): raise ValueError("duplicate observation_id")
        rank={v:i for i,v in enumerate(rule.verdict_order)}; grouped={}
        for o in obs:
            if rule.dimension not in o.dimensions or o.verdict not in rank: raise ValueError("invalid observation")
            x=o.dimensions[rule.dimension]
            if isinstance(x,bool) or not isinstance(x,(int,float)) or not isfinite(x): raise ValueError("dimension must be finite numeric")
            grouped.setdefault(x,[]).append(o)
        conflicts=[]; canon=[]
        for x in sorted(grouped):
            b=sorted(grouped[x],key=lambda o:o.observation_id); vs=tuple(sorted({o.verdict for o in b}))
            conflicts.append((x,vs)) if len(vs)>1 else canon.append(b[0])
        bad=[]
        for i,a in enumerate(canon):
            for b in canon[i+1:]:
                ar,br=rank[a.verdict],rank[b.verdict]
                illegal=(rule.direction=="NONINCREASING" and br>ar) or (rule.direction=="NONDECREASING" and br<ar) or (rule.direction=="EQUAL" and br!=ar)
                if illegal: bad.append((a.observation_id,b.observation_id))
        return MonotonicityAuditResult("PASS" if not conflicts and not bad else "FREEZE",tuple(bad),tuple(conflicts))

@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    priority: int
    conditions: Mapping[str,Any]
    effect: str

@dataclass(frozen=True)
class PolicyDeadZoneResult:
    status: str
    reason: str|None
    unreachable_rules: tuple[str,...]
    shadowed_rules: tuple[str,...]
    redundant_rules: tuple[str,...]
    live_rules: tuple[str,...]

class PolicyDeadZoneAnalyzer:
    def __init__(self,max_combinations:int=100_000): self.max=max_combinations
    def analyze(self,domains:Mapping[str,Sequence[Any]],rules:Sequence[PolicyRule],default_effect:str)->PolicyDeadZoneResult:
        if len({r.rule_id for r in rules})!=len(rules): raise ValueError("duplicate rule_id")
        names=tuple(sorted(domains)); total=1
        for n in names:
            if not domains[n]: raise ValueError("empty domain")
            total*=len(domains[n])
            if total>self.max: return PolicyDeadZoneResult("FREEZE","COMBINATION_BUDGET_EXCEEDED",(),(),(),())
        states=[dict(zip(names,v,strict=True)) for v in product(*(domains[n] for n in names))] if names else [{}]
        ordered=sorted(rules,key=lambda r:(-r.priority,r.rule_id)); matched={r.rule_id:0 for r in ordered}; selected={r.rule_id:0 for r in ordered}
        def match(r,s): return all(k in domains and v in domains[k] and s.get(k)==v for k,v in r.conditions.items())
        def decide(s,rs):
            for r in rs:
                if match(r,s): return r.effect
            return default_effect
        for s in states:
            ms=[r for r in ordered if match(r,s)]
            for r in ms: matched[r.rule_id]+=1
            if ms: selected[ms[0].rule_id]+=1
        base=[decide(s,ordered) for s in states]
        redundant=tuple(sorted(r.rule_id for r in ordered if [decide(s,[x for x in ordered if x.rule_id!=r.rule_id]) for s in states]==base))
        unreachable=tuple(sorted(k for k,v in matched.items() if v==0)); shadowed=tuple(sorted(k for k,v in matched.items() if v>0 and selected[k]==0))
        live=tuple(sorted(r.rule_id for r in ordered if selected[r.rule_id]>0 and r.rule_id not in redundant))
        return PolicyDeadZoneResult("PASS",None,unreachable,shadowed,redundant,live)

@dataclass(frozen=True)
class RefutationEntry:
    hypothesis_id:str; scope:str; premise_digest:str; authority_epoch:str; counterexample:str; evidence_ids:tuple[str,...]; expires_at:int|float; revoked:bool=False

@dataclass(frozen=True)
class RefutationLookupResult:
    status:str; reason:str|None; counterexample:str|None=None; evidence_ids:tuple[str,...]=()

class RefutationKnowledgeMemory:
    def __init__(self): self._entries={}
    def add(self,e:RefutationEntry):
        b=self._entries.setdefault(e.hypothesis_id,[]); ident=(e.scope,e.premise_digest,e.authority_epoch)
        if any((x.scope,x.premise_digest,x.authority_epoch)==ident for x in b): raise ValueError("duplicate refutation identity")
        b.append(e)
    def lookup(self,hypothesis_id,scope,premise_digest,authority_epoch,now)->RefutationLookupResult:
        c=self._entries.get(hypothesis_id,[])
        if not c:return RefutationLookupResult("MISS","ABSENT")
        c=[x for x in c if x.scope==scope and not x.revoked]
        if not c:return RefutationLookupResult("MISS","SCOPE_MISMATCH")
        c=[x for x in c if x.premise_digest==premise_digest]
        if not c:return RefutationLookupResult("MISS","PREMISE_DRIFT")
        c=[x for x in c if x.authority_epoch==authority_epoch]
        if not c:return RefutationLookupResult("MISS","AUTHORITY_DRIFT")
        c=[x for x in c if now<=x.expires_at]
        if not c:return RefutationLookupResult("MISS","STALE_REFUTATION")
        x=max(c,key=lambda x:x.expires_at); return RefutationLookupResult("REFUTED",None,x.counterexample,tuple(sorted(x.evidence_ids)))

@dataclass(frozen=True)
class AssumptionClosureResult:
    status:str
    assumptions_by_claim:Mapping[str,tuple[str,...]]
    unknowns_by_claim:Mapping[str,tuple[str,...]]

class AssumptionClosureEngine:
    def audit(self,claims:Mapping[str,Sequence[str]],facts:set[str],assumptions:set[str],unknowns:set[str],targets:Sequence[str])->AssumptionClosureResult:
        memo={}
        def resolve(cid,active):
            if cid in memo:return set(memo[cid][0]),set(memo[cid][1])
            if cid in active:return set(),{"cycle:"+"->".join(active+(cid,))}
            if cid not in claims:return set(),{"claim:"+cid}
            aa=set(); uu=set()
            for d in claims[cid]:
                if d.startswith("fact:"):
                    if d[5:] not in facts: uu.add(d)
                elif d.startswith("assume:"):
                    aa.add(d[7:]) if d[7:] in assumptions else uu.add(d)
                elif d.startswith("unknown:"): uu.add(d[8:] if d[8:] in unknowns else d)
                elif d.startswith("claim:"):
                    a,u=resolve(d[6:],active+(cid,)); aa|=a; uu|=u
                else: uu.add(d)
            memo[cid]=(aa,uu); return aa,uu
        amap={}; umap={}
        for t in targets:
            a,u=resolve(t,()); amap[t]=tuple(sorted(a)); umap[t]=tuple(sorted(u))
        return AssumptionClosureResult("BLOCKED" if any(amap[t] or umap[t] for t in targets) else "PASS",dict(sorted(amap.items())),dict(sorted(umap.items())))

@dataclass(frozen=True)
class AdvisoryIntegrityGateResult:
    status:str
    reasons:tuple[str,...]

class AdvisoryIntegrityGate:
    def evaluate(self,circularity,monotonicity,policy,closure,refutation,critical_policy_rule_ids=frozenset()):
        r=set()
        if circularity.status!="PASS":r.add("EPISTEMIC_CIRCULARITY_OR_UNGROUNDED_CLAIM")
        if monotonicity.status!="PASS":r.add("DECISION_MONOTONICITY_VIOLATION")
        if policy.status!="PASS":r.add("POLICY_ANALYSIS_INCOMPLETE")
        if closure.status!="PASS":r.add("ASSUMPTION_CLOSURE_INCOMPLETE")
        if refutation.status=="REFUTED":r.add("HYPOTHESIS_ALREADY_REFUTED")
        dead=set(policy.unreachable_rules)|set(policy.shadowed_rules)|set(policy.redundant_rules)
        for x in set(critical_policy_rule_ids)&dead:r.add("CRITICAL_POLICY_DEAD_ZONE:"+x)
        reasons=tuple(sorted(r)); return AdvisoryIntegrityGateResult("READY" if not reasons else "FREEZE",reasons)
