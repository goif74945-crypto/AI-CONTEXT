#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from proof_capsule import Claim,Evidence,Policy,compile_capsule

def compile_mapping(m):
    claims=[Claim(x["id"],x["statement"],x["target"],x["version"],tuple(x["accepted"]),x.get("required",True),x.get("material",True)) for x in m["claims"]]
    evidence=[Evidence(x["id"],x["source"],x["status"],x["eclass"],x["target"],x["version"],tuple(x["supports"]),x["rank"],x["observed_at"],x.get("valid_until"),x.get("cost",1),x.get("digest")) for x in m["evidence"]]
    q=m.get("policy",{})
    policy=Policy(q.get("max_items",12),q.get("max_cost",48),q.get("strict_refs",True),q.get("disclose_dissent",True),q.get("require_digest",True))
    return compile_capsule(claims,evidence,as_of=m["as_of"],policy=policy).to_dict()

if __name__=="__main__":
    data=json.load(sys.stdin) if len(sys.argv)==1 else json.load(open(sys.argv[1],encoding="utf-8"))
    json.dump(compile_mapping(data),sys.stdout,ensure_ascii=False,sort_keys=True,separators=(",",":"));sys.stdout.write("\n")
