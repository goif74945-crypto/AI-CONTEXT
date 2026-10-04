from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Callable, Iterable, Mapping

class StabilityError(ValueError): pass
class DuplicateEvidenceError(StabilityError): pass

class Kind(str, Enum):
    SUPPORT="SUPPORT"
    BLOCK="BLOCK"
    CONTEXT="CONTEXT"

class Decision(str, Enum):
    REJECT="REJECT"
    FREEZE="FREEZE"
    RELEASE="RELEASE"
    @property
    def rank(self)->int:
        return {Decision.REJECT:0,Decision.FREEZE:1,Decision.RELEASE:2}[self]

def _norm(v:Any)->Any:
    if v is None or isinstance(v,(bool,int,str)): return v
    if isinstance(v,float):
        if v!=v or v in (float("inf"),float("-inf")): raise StabilityError("non-finite float")
        return v
    if isinstance(v,Mapping):
        if any(not isinstance(k,str) for k in v): raise StabilityError("mapping keys must be strings")
        return {k:_norm(v[k]) for k in sorted(v)}
    if isinstance(v,(list,tuple)): return [_norm(x) for x in v]
    raise StabilityError(f"unsupported value: {type(v).__name__}")

@dataclass(frozen=True,slots=True)
class Evidence:
    evidence_id:str
    kind:Kind
    claim:str
    value:Any=None
    source:str="unknown"
    tags:tuple[str,...]=()
    def __post_init__(self):
        if not self.evidence_id.strip() or not self.claim.strip() or not self.source.strip():
            raise StabilityError("empty identity field")
        if len(set(self.tags))!=len(self.tags): raise StabilityError("duplicate tag")
        _norm(self.value)
    def canonical(self)->dict[str,Any]:
        return {"claim":self.claim,"evidence_id":self.evidence_id,"kind":self.kind.value,
                "source":self.source,"tags":sorted(self.tags),"value":_norm(self.value)}

EvidenceSet=tuple[Evidence,...]
Oracle=Callable[[EvidenceSet],Decision]

def canonicalize(items:Iterable[Evidence])->EvidenceSet:
    out:dict[str,Evidence]={}
    for x in items:
        p=out.get(x.evidence_id)
        if p is None: out[x.evidence_id]=x
        elif p.canonical()!=x.canonical():
            raise DuplicateEvidenceError(f"conflicting payload for {x.evidence_id!r}")
    return tuple(out[k] for k in sorted(out))

def fingerprint(items:Iterable[Evidence])->str:
    raw=json.dumps([x.canonical() for x in canonicalize(items)],ensure_ascii=False,
                   sort_keys=True,separators=(",",":")).encode("utf-8")
    return sha256(raw).hexdigest()

def evaluate(oracle:Oracle,items:Iterable[Evidence])->Decision:
    r=oracle(canonicalize(items))
    if not isinstance(r,Decision): raise StabilityError("oracle returned non-Decision")
    return r
