import json
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

ROOT=Path(__file__).parents[1]
for rel in [
    "01_correlation_consensus_guard/src","02_schema_evolution_compiler/src","03_fault_containment_cut_planner/src",
    "04_critical_path_evidence_scheduler/src","05_cumulative_disclosure_accountant/src",
]:
    sys.path.insert(0,str(ROOT/rel))

from correlation_consensus import Vote,evaluate_consensus
from schema_evolution import ContractSchema,FieldSpec,compile_evolution
from fault_containment import Component,Dependency,plan_containment
from critical_path_scheduler import WorkItem,schedule_work
from disclosure_accountant import DisclosureEvent,DisclosureItem,DisclosurePolicy,LedgerState,evaluate_disclosure


def measure(name,fn,repeats=3):
    times=[]; peaks=[]
    for _ in range(repeats):
        tracemalloc.start(); t0=time.perf_counter(); fn(); elapsed=(time.perf_counter()-t0)*1000
        _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
        times.append(elapsed); peaks.append(peak/1024)
    return {"name":name,"median_ms":round(statistics.median(times),3),"max_ms":round(max(times),3),"peak_kib":round(max(peaks),1),"repeats":repeats}


def main():
    votes=[Vote(f"a{i}","X",5000,(f"p{i}",),3) for i in range(1000)]
    old=ContractSchema("1",tuple(FieldSpec(f"f{i}","string") for i in range(1000)))
    new=ContractSchema("2",tuple(FieldSpec(f"f{i}","string") for i in range(1200)))
    components=[Component(f"c{i}") for i in range(5000)]
    deps=[Dependency(f"c{i}",f"c{i+1}","HARD") for i in range(4999)]
    work=[WorkItem(f"t{i}",1+(i%5),"agent") for i in range(1000)]
    catalog=[DisclosureItem(f"i{i}","cat",1,f"g{i}") for i in range(2000)]
    event=DisclosureEvent("e","A","p",tuple(f"i{i}" for i in range(2000)))
    policy=DisclosurePolicy(5000,(("cat",5000),),9000)
    results=[
        measure("CACG_1000_independent_votes",lambda:evaluate_consensus(votes)),
        measure("CSEC_1000_to_1200_fields",lambda:compile_evolution(old,new)),
        measure("FCCP_5000_hard_chain",lambda:plan_containment(components,deps,["c0"])),
        measure("CPES_1000_independent_tasks_8_slots",lambda:schedule_work(work,{"agent":8})),
        measure("CDA_2000_item_event",lambda:evaluate_disclosure(catalog,LedgerState(),event,policy)),
    ]
    print(json.dumps({"classification":"LOCAL_REFERENCE_BENCHMARK_NOT_PRODUCTION_SLA","python":sys.version.split()[0],"results":results},sort_keys=True,indent=2))


if __name__=="__main__":
    main()
