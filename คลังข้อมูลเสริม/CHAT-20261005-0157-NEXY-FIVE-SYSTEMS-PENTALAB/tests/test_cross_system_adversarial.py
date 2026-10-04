import itertools
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).parents[1]
for rel in [
    "01_correlation_consensus_guard/src",
    "02_schema_evolution_compiler/src",
    "03_fault_containment_cut_planner/src",
    "04_critical_path_evidence_scheduler/src",
    "05_cumulative_disclosure_accountant/src",
]:
    sys.path.insert(0,str(ROOT/rel))

from correlation_consensus import ConsensusPolicy, Vote, evaluate_consensus
from schema_evolution import ContractSchema, FieldSpec, SchemaInputError, compile_evolution
from fault_containment import Component, Dependency, plan_containment
from critical_path_scheduler import WorkItem, schedule_work
from disclosure_accountant import DisclosureEvent, DisclosureItem, DisclosurePolicy, LedgerState, evaluate_disclosure


class CrossSystemAdversarialTests(unittest.TestCase):
    def test_cacg_720_permutations_are_byte_stable(self):
        votes=[
            Vote("a","X",9000,("p:a",),3),Vote("b","X",8000,("p:b",),3),Vote("c","X",7000,("p:c",),3),
            Vote("d","Y",3000,("p:d",),3),Vote("e","Y",2000,("p:e",),3),Vote("f","X",6000,("p:f",),3),
        ]
        self.assertEqual(len({evaluate_consensus(p).fingerprint for p in itertools.permutations(votes)}),1)

    def test_cacg_transitive_correlation_chain_counts_once(self):
        votes=[
            Vote("a","X",9000,("d1",),3),Vote("b","X",9000,("d1","d2"),3),Vote("c","X",9000,("d2",),3),
            Vote("z","Y",9000,("independent",),3),
        ]
        r=evaluate_consensus(votes,ConsensusPolicy(quorum_bps=5000,min_independent_clusters=2))
        self.assertEqual(r.status,"FREEZE"); self.assertIn("WEIGHT_TIE",r.reason_codes); self.assertEqual(r.participating_cluster_count,2)

    def test_csec_never_guesses_rename(self):
        old=ContractSchema("1",(FieldSpec("user_name","string",True),))
        new=ContractSchema("2",(FieldSpec("display_name","string",True),))
        self.assertEqual(compile_evolution(old,new).classification,"BREAKING")

    def test_csec_many_to_one_rename_is_rejected(self):
        old=ContractSchema("1",(FieldSpec("a","string"),FieldSpec("b","string")))
        new=ContractSchema("2",(FieldSpec("b","string"),))
        with self.assertRaises(SchemaInputError): compile_evolution(old,new,explicit_renames={"a":"b"})

    def test_fccp_failed_set_order_is_stable(self):
        comps=[Component("a"),Component("b"),Component("c"),Component("d")]
        deps=[Dependency("a","c","HARD"),Dependency("b","d","SOFT")]
        a=plan_containment(comps,deps,["a","b"]); b=plan_containment(reversed(comps),reversed(deps),["b","a"])
        self.assertEqual(a.fingerprint,b.fingerprint)

    def test_fccp_partition_is_disjoint_and_exhaustive(self):
        comps=[Component("a"),Component("b"),Component("c"),Component("d")]
        r=plan_containment(comps,[Dependency("a","b","HARD"),Dependency("a","c","SOFT")],["a"])
        sets=[set(r.quarantined),set(r.degraded),set(r.healthy)]
        self.assertFalse(sets[0]&sets[1]); self.assertFalse(sets[0]&sets[2]); self.assertFalse(sets[1]&sets[2])
        self.assertEqual(set.union(*sets),{"a","b","c","d"})

    def test_cpes_dependencies_and_slots_never_overlap(self):
        tasks=[
            WorkItem("a",7,"agent"),WorkItem("b",5,"agent"),WorkItem("c",3,"agent",("a",)),
            WorkItem("d",4,"test",("b",)),WorkItem("e",2,"agent",("c","d")),
        ]
        r=schedule_work(tasks,{"agent":2,"test":1}); by={s.task_id:s for s in r.schedule}
        for t in tasks:
            for dep in t.dependencies: self.assertGreaterEqual(by[t.task_id].start_ms,by[dep].end_ms)
        grouped={}
        for s in r.schedule: grouped.setdefault((s.resource,s.slot),[]).append(s)
        for seq in grouped.values():
            seq=sorted(seq,key=lambda x:x.start_ms)
            for left,right in zip(seq,seq[1:]): self.assertLessEqual(left.end_ms,right.start_ms)

    def test_cpes_120_permutations_are_stable(self):
        tasks=[WorkItem("a",2,"agent"),WorkItem("b",3,"agent"),WorkItem("c",4,"test"),WorkItem("d",2,"agent",("a","c")),WorkItem("e",1,"test",("b",))]
        self.assertEqual(len({schedule_work(p,{"agent":2,"test":1}).fingerprint for p in itertools.permutations(tasks)}),1)

    def test_cda_freeze_is_state_preserving(self):
        catalog=[DisclosureItem("a","cat",6,"g"),DisclosureItem("b","cat",6,"g")]
        policy=DisclosurePolicy(10,(("cat",10),),9000)
        state=LedgerState()
        r=evaluate_disclosure(catalog,state,DisclosureEvent("e","aud","purpose",("a","b")),policy)
        self.assertEqual(r.status,"FREEZE"); self.assertEqual(r.next_state,state)

    def test_cda_review_is_state_preserving(self):
        catalog=[DisclosureItem("a","cat",4,"g1"),DisclosureItem("b","cat",4,"g2")]
        policy=DisclosurePolicy(10,(("cat",10),),8000)
        state=LedgerState()
        r=evaluate_disclosure(catalog,state,DisclosureEvent("e","aud","purpose",("a","b")),policy)
        self.assertEqual(r.status,"REVIEW"); self.assertEqual(r.next_state,state)

    def test_cda_same_item_across_purposes_is_charged_once(self):
        catalog=[DisclosureItem("a","cat",2,"g")]
        policy=DisclosurePolicy(10,(("cat",10),),9000)
        r1=evaluate_disclosure(catalog,LedgerState(),DisclosureEvent("e1","aud","p1",("a",)),policy)
        r2=evaluate_disclosure(catalog,r1.next_state,DisclosureEvent("e2","aud","p2",("a",)),policy)
        self.assertEqual(r2.projected_audience_points,2); self.assertEqual(r2.newly_disclosed_items,())


if __name__=="__main__":
    unittest.main()
