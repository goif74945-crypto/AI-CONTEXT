import json
import sys
from pathlib import Path

ROOT=Path(__file__).parents[1]
for rel in [
    "01_correlation_consensus_guard/src","02_schema_evolution_compiler/src","03_fault_containment_cut_planner/src",
    "04_critical_path_evidence_scheduler/src","05_cumulative_disclosure_accountant/src",
]:
    sys.path.insert(0,str(ROOT/rel))

from correlation_consensus import ConsensusPolicy,Vote,evaluate_consensus
from schema_evolution import ContractSchema,FieldSpec,compile_evolution
from fault_containment import Component,Dependency,plan_containment
from critical_path_scheduler import WorkItem,schedule_work
from disclosure_accountant import DisclosureEvent,DisclosureItem,DisclosurePolicy,LedgerState,evaluate_disclosure


def run():
    consensus=evaluate_consensus([
        Vote("worker-a","ADOPT",9000,("provider:a","model:a"),3),
        Vote("worker-b","ADOPT",8500,("provider:b","model:b"),3),
        Vote("worker-c","REJECT",2000,("provider:c",),3),
    ],ConsensusPolicy(quorum_bps=7000,min_independent_clusters=2,min_evidence_level=2))

    evolution=compile_evolution(
        ContractSchema("1.0",(FieldSpec("id","string",True),)),
        ContractSchema("2.0",(FieldSpec("id","string",True),FieldSpec("epoch","integer",True,has_default=True))),
    )

    containment=plan_containment(
        [Component("core",True),Component("search"),Component("view")],
        [Dependency("search","view","SOFT")],
        ["search"],
    )

    schedule=schedule_work([
        WorkItem("compile",4,"build",produces_evidence=1),
        WorkItem("unit",6,"test",("compile",),produces_evidence=2,requires_dependency_evidence=1),
        WorkItem("adversarial",8,"test",("compile",),produces_evidence=2,requires_dependency_evidence=1),
        WorkItem("audit",2,"agent",("unit","adversarial"),produces_evidence=2,requires_dependency_evidence=2),
    ],{"build":1,"test":2,"agent":1})

    disclosure=evaluate_disclosure(
        [DisclosureItem("spec_hash","provenance",1,"project")],
        LedgerState(),
        DisclosureEvent("evt-1","external-verifier","verification",("spec_hash",)),
        DisclosurePolicy(10,(("provenance",10),),9000),
    )

    result={
        "classification":"AI_PROPOSED_REFERENCE_PIPELINE_NOT_NEXY_AUTHORITY",
        "consensus":{"status":consensus.status,"winner":consensus.winner,"fingerprint":consensus.fingerprint},
        "schema_evolution":{"classification":evolution.classification,"fingerprint":evolution.fingerprint},
        "fault_containment":{"status":containment.status,"fingerprint":containment.fingerprint},
        "evidence_schedule":{"status":schedule.status,"makespan_ms":schedule.makespan_ms,"fingerprint":schedule.fingerprint},
        "disclosure":{"status":disclosure.status,"receipt_hash":disclosure.receipt_hash},
    }
    assert result["consensus"]["status"]=="CONSENSUS" and result["consensus"]["winner"]=="ADOPT"
    assert result["schema_evolution"]["classification"]=="MIGRATION_REQUIRED"
    assert result["fault_containment"]["status"]=="DEGRADED"
    assert result["evidence_schedule"]["status"]=="PLAN_READY"
    assert result["disclosure"]["status"]=="ALLOW"
    return result


if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True,indent=2))
