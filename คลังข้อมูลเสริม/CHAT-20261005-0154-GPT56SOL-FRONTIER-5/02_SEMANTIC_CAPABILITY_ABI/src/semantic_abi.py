from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable

EVIDENCE_ORDER={"E0":0,"E1":1,"E2":2,"E3":3,"E4":4,"E5":5,"E6":6,"E7":7}
DETERMINISM_ORDER={"none":0,"best_effort":1,"structural":2,"strict":3}

def _canon(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def schema_hash(schema: dict) -> str:
    return sha256(_canon(schema).encode()).hexdigest()

@dataclass(frozen=True)
class CapabilityContract:
    name:str; abi_major:int; input_schema_hash:str; output_schema_hash:str; determinism:str; evidence_floor:str

@dataclass(frozen=True)
class ProviderCapability:
    name:str; native_name:str; abi_major:int; input_schema_hash:str; output_schema_hash:str; determinism:str; evidence_level:str


def compile_bindings(required: Iterable[CapabilityContract], offered: Iterable[ProviderCapability]) -> dict:
    req=list(required); off=list(offered)
    if len({x.name for x in req}) != len(req): raise ValueError("duplicate required capability")
    if len({x.name for x in off}) != len(off): raise ValueError("duplicate offered capability")
    offered_by={x.name:x for x in off}
    errors=[]; bindings=[]
    for c in sorted(req,key=lambda x:x.name):
        p=offered_by.get(c.name)
        if not p:
            errors.append({"capability":c.name,"reason":"missing"}); continue
        checks=[
          (p.abi_major==c.abi_major,"abi_major_mismatch"),
          (p.input_schema_hash==c.input_schema_hash,"input_schema_mismatch"),
          (p.output_schema_hash==c.output_schema_hash,"output_schema_mismatch"),
          (DETERMINISM_ORDER.get(p.determinism,-1)>=DETERMINISM_ORDER.get(c.determinism,99),"determinism_too_weak"),
          (EVIDENCE_ORDER.get(p.evidence_level,-1)>=EVIDENCE_ORDER.get(c.evidence_floor,99),"evidence_floor_not_met"),
        ]
        failed=[reason for ok,reason in checks if not ok]
        if failed: errors.append({"capability":c.name,"reason":failed})
        else: bindings.append({"capability":c.name,"native_name":p.native_name})
    status="FREEZE" if errors else "PASS"
    digest=sha256(_canon(bindings).encode()).hexdigest()
    return {"status":status,"bindings":bindings,"errors":errors,"binding_digest":digest}
