from pathlib import Path
import json, random, sys, time
sys.path.insert(0,str(Path(__file__).parent/"code"))
from core import Decision, Evidence, Kind, fingerprint
import mono
from damp import Guard, Observation

def atom(eid,kind): return Evidence(eid,kind,eid,{"v":1},"stress")
def oracle(items):
    s=sum(x.kind is Kind.SUPPORT for x in items); b=sum(x.kind is Kind.BLOCK for x in items)
    if b>=2:return Decision.REJECT
    if b==1:return Decision.FREEZE
    return Decision.RELEASE if s>=2 else Decision.FREEZE

def main():
    rng=random.Random(202610050155); start=time.perf_counter()
    for case in range(5000):
        base=[atom(f"{case}:s:{i}",Kind.SUPPORT) for i in range(rng.randrange(6))]
        base += [atom(f"{case}:b:{i}",Kind.BLOCK) for i in range(rng.randrange(4))]
        if not mono.verify(base,[atom(f"{case}:sx",Kind.SUPPORT),atom(f"{case}:bx",Kind.BLOCK)],oracle,max_group_size=1)["passed"]:
            raise AssertionError(f"monotonicity:{case}")
    for case in range(5000):
        items=[atom(f"f{case}:a",Kind.SUPPORT),atom(f"f{case}:b",Kind.BLOCK),atom(f"f{case}:c",Kind.CONTEXT)]
        expected=fingerprint(items); rng.shuffle(items)
        if fingerprint(items)!=expected: raise AssertionError(f"fingerprint:{case}")
    g=Guard(promotion_dwell=3,require_stable_fingerprint=False); before=g.public; regressions=0
    for seq in range(50000):
        proposed=rng.choice(tuple(Decision)); r=g.observe(Observation(seq,proposed,f"fp:{seq//4}"))
        if proposed.rank<before.rank:
            regressions+=1
            if r["public"] is not proposed: raise AssertionError(f"delayed regression:{seq}")
        before=r["public"]
    print(json.dumps({"status":"PASS","seed":202610050155,"monotonic_cases":5000,"fingerprint_cases":5000,
        "temporal_transitions":50000,"safety_regressions_checked":regressions,
        "elapsed_seconds":round(time.perf_counter()-start,6)},sort_keys=True,separators=(",",":")))

if __name__=="__main__": main()
