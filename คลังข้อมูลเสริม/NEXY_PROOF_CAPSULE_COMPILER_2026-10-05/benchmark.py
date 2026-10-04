from __future__ import annotations
from time import perf_counter
from proof_capsule import Claim,Evidence,Policy,compile_capsule
A="2026-10-05T01:30:00+07:00";V="sha256:v1";D="sha256:"+"b"*64
for n in (1000,5000,10000):
    claims=[Claim(f"C{i}",f"claim {i}","bench",V,("E2",)) for i in range(n)]
    evidence=[]
    for j,start in enumerate(range(0,n,10)):
        evidence.append(Evidence(f"E{j}",f"bench/{j}","PASS","E2","bench",V,tuple(f"C{i}" for i in range(start,min(start+10,n))),1,"2026-10-05T01:00:00+07:00",None,1,D))
    t=perf_counter(); r=compile_capsule(claims,evidence,as_of=A,policy=Policy(max_items=n,max_cost=n)); dt=perf_counter()-t
    assert r.status=="PASS" and len(r.coverage)==n
    print(f"{n} claims / {len(evidence)} evidence: {dt:.6f}s")
