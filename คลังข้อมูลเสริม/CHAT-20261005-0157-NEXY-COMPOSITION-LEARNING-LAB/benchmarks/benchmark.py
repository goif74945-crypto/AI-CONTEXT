from __future__ import annotations

import json
import platform
import statistics
import time

from nexy_aux.composition import compose
from nexy_aux.corrections import compile_corrections
from nexy_aux.distiller import distill
from nexy_aux.emergence import analyze_plan
from nexy_aux.portability import assess_portability


def measure(fn, repeats=5):
    samples=[]
    for _ in range(repeats):
        start=time.perf_counter()
        fn()
        samples.append(time.perf_counter()-start)
    return {"median_seconds": statistics.median(samples), "min_seconds": min(samples), "max_seconds": max(samples)}


def main():
    n=5000
    components=[]
    for i in range(n):
        need="root" if i == 0 else f"f{i-1}"
        components.append({"id":f"c{i:05d}","assumptions":[need],"guarantees":[f"f{i}"]})

    steps=[]
    for i in range(n):
        source="root" if i == 0 else f"a{i-1}"
        steps.append({"id":f"s{i:05d}","consumes":[source],"produces":[f"a{i}"],"capabilities":[]})

    dims={f"d{i}":i for i in range(n)}
    policy={f"d{i}":"MUST_EQUAL" for i in range(n)}
    evidence={"claim_id":"C","evidence_class":"E2","source_context":dims}
    target={"claim_id":"C","required_evidence_classes":["E2"],"target_context":dict(dims)}

    corrections=[
        {"id":f"r{i}","authority":"USER_DIRECTIVE","scope_mode":"BOUNDED",
         "selector":{"project":f"p{i}","operation":"report"},
         "assertions":[{"field":"mode","op":"eq","value":"strict"}]}
        for i in range(n)
    ]

    distill_items=list(range(200))
    core={7,91,177}
    def oracle(xs):
        return "CORE" if core.issubset(set(xs)) else None

    result={
        "python": platform.python_version(),
        "platform": platform.platform(),
        "repeats": 5,
        "workloads": {
            "c1_chain_5000": measure(lambda: compose(components,["root"])),
            "c2_linear_plan_5000": measure(lambda: analyze_plan({"artifacts":{"root":[]},"steps":steps})),
            "c3_equal_dimensions_5000": measure(lambda: assess_portability(evidence,target,policy)),
            "c4_distinct_scopes_5000": measure(lambda: compile_corrections(corrections)),
            "c5_ddmin_200_core3": measure(lambda: distill(distill_items,oracle,"CORE")),
        },
    }
    print(json.dumps(result,sort_keys=True,separators=(",", ":")))


if __name__ == "__main__":
    main()
