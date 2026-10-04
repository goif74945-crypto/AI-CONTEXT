from __future__ import annotations

import importlib.util
import itertools
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("neik", ROOT / "src" / "neik.py")
neik = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["neik"] = neik
SPEC.loader.exec_module(neik)


def base_evidence(eid: str, *, source: str, producer: str | None = None, oracle: str | None = None):
    producer = producer or f"p-{eid}"
    oracle = oracle or f"o-{eid}"
    return {
        "id": eid, "claim_id": "claim.q", "target_revision": "r1", "evidence_class": "E2", "verdict": "PASS",
        "producer_id": producer, "subjects_under_test": ["system"], "external_oracle": True, "blind": True,
        "derived_from": [], "source_lineage": [source], "producer_lineage": [producer], "oracle_lineage": [oracle],
        "artifact_hash": f"h-{eid}",
    }


def envelope(evidence, *, quorum=2, dims=None, blind=False, budget=100000):
    return {
        "schema_version": "neik/0.1",
        "claim": {"id": "claim.q", "target_revision": "r1", "required_evidence_class": "E2", "required_independent_confirmations": quorum},
        "policy": {
            "independence_dimensions": dims or ["source_lineage", "producer_lineage", "oracle_lineage"],
            "require_blind": blind,
            "forbid_self_verification_without_external_oracle": True,
            "max_evidence_nodes": 64,
            "max_solver_states": budget,
        },
        "evidence": evidence,
    }


def decision(x):
    return neik.evaluate(neik.parse_envelope(x))


class KernelTests(unittest.TestCase):
    def test_three_independent_pass(self):
        xs=[base_evidence("a",source="s1"),base_evidence("b",source="s2"),base_evidence("c",source="s3")]
        out=decision(envelope(xs,quorum=3))
        self.assertEqual(out["status"],"PASS")
        self.assertEqual(out["witness"],["a","b","c"])

    def test_shared_source_not_verified(self):
        xs=[base_evidence("a",source="same"),base_evidence("b",source="same")]
        out=decision(envelope(xs,quorum=2,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")
        self.assertEqual(out["maximum_independent_confirmations"],1)

    def test_derived_inherits_parent_lineage(self):
        a=base_evidence("a",source="s1"); b=base_evidence("b",source="s2"); b["derived_from"]=["a"]
        out=decision(envelope([a,b],quorum=2,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")
        self.assertEqual(out["lineage_closure"]["b"]["source_lineage"],["s1","s2"])

    def test_cycle_freezes(self):
        a=base_evidence("a",source="s1"); b=base_evidence("b",source="s2"); a["derived_from"]=["b"]; b["derived_from"]=["a"]
        out=decision(envelope([a,b],quorum=1,dims=["source_lineage"]))
        self.assertEqual((out["status"],out["reason"]),("FREEZE","EVIDENCE_DEPENDENCY_CYCLE"))

    def test_pass_fail_conflict_freezes(self):
        a=base_evidence("a",source="s1"); b=base_evidence("b",source="s2"); b["verdict"]="FAIL"
        out=decision(envelope([a,b],quorum=1,dims=["source_lineage"]))
        self.assertEqual((out["status"],out["reason"]),("FREEZE","CURRENT_PASS_FAIL_CONFLICT"))

    def test_stale_excluded(self):
        a=base_evidence("a",source="s1"); b=base_evidence("b",source="s2"); b["target_revision"]="old"
        out=decision(envelope([a,b],quorum=2,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")
        self.assertTrue(any(f["code"]=="STALE_TARGET_REVISION" for f in out["findings"]))

    def test_lower_class_excluded(self):
        a=base_evidence("a",source="s1"); a["evidence_class"]="E1"
        out=decision(envelope([a],quorum=1,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")

    def test_blind_policy(self):
        a=base_evidence("a",source="s1"); a["blind"]=False
        out=decision(envelope([a],quorum=1,dims=["source_lineage"],blind=True))
        self.assertEqual(out["status"],"NOT_VERIFIED")
        self.assertTrue(any(f["code"]=="NOT_BLIND" for f in out["findings"]))

    def test_self_verification_without_external_oracle(self):
        a=base_evidence("a",source="s1",producer="system"); a["external_oracle"]=False
        out=decision(envelope([a],quorum=1,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")

    def test_self_verification_empty_oracle_lineage(self):
        a=base_evidence("a",source="s1",producer="system"); a["oracle_lineage"]=[]
        out=decision(envelope([a],quorum=1,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")

    def test_missing_configured_lineage_excluded(self):
        a=base_evidence("a",source="s1"); a["source_lineage"]=[]
        out=decision(envelope([a],quorum=1,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")
        self.assertTrue(any(f["code"]=="MISSING_INDEPENDENCE_LINEAGE" for f in out["findings"]))

    def test_duplicate_artifact_intrinsic_conflict(self):
        a=base_evidence("a",source="s1"); b=base_evidence("b",source="s2"); b["artifact_hash"]=a["artifact_hash"]
        out=decision(envelope([a,b],quorum=2,dims=["source_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")
        self.assertTrue(any("artifact_identity" in c["overlap"] for c in out["conflicts"]))

    def test_producer_correlation(self):
        a=base_evidence("a",source="s1",producer="p"); b=base_evidence("b",source="s2",producer="p")
        out=decision(envelope([a,b],quorum=2,dims=["producer_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")

    def test_oracle_correlation(self):
        a=base_evidence("a",source="s1",oracle="o"); b=base_evidence("b",source="s2",oracle="o")
        out=decision(envelope([a,b],quorum=2,dims=["oracle_lineage"]))
        self.assertEqual(out["status"],"NOT_VERIFIED")

    def test_exact_chain_witness(self):
        a=base_evidence("a",source="x"); b=base_evidence("b",source="x"); b["source_lineage"]=["x","y"]; c=base_evidence("c",source="y")
        out=decision(envelope([a,b,c],quorum=2,dims=["source_lineage"]))
        self.assertEqual(out["witness"],["a","c"])
        self.assertEqual(out["status"],"PASS")

    def test_order_invariant_hash(self):
        xs=[base_evidence("a",source="s1"),base_evidence("b",source="s2"),base_evidence("c",source="s3")]
        self.assertEqual(decision(envelope(xs)),decision(envelope(list(reversed(xs)))))

    def test_solver_budget_freezes(self):
        xs=[base_evidence(f"e{i}",source=f"s{i}") for i in range(6)]
        out=decision(envelope(xs,quorum=2,dims=["source_lineage"],budget=1))
        self.assertEqual((out["status"],out["reason"]),("FREEZE","SOLVER_BUDGET_EXCEEDED"))
        self.assertIsNone(out["maximum_independent_confirmations"])

    def test_unknown_dependency_rejected(self):
        a=base_evidence("a",source="s1"); a["derived_from"]=["missing"]
        with self.assertRaises(neik.ContractError): neik.parse_envelope(envelope([a],quorum=1))

    def test_unknown_field_rejected(self):
        x=envelope([base_evidence("a",source="s1")],quorum=1); x["policy"]["mystery"]=True
        with self.assertRaises(neik.ContractError): neik.parse_envelope(x)

    def test_duplicate_lineage_rejected(self):
        a=base_evidence("a",source="s1"); a["source_lineage"]=["s1","s1"]
        with self.assertRaises(neik.ContractError): neik.parse_envelope(envelope([a],quorum=1))

    def test_producer_id_must_be_in_lineage(self):
        a=base_evidence("a",source="s1"); a["producer_lineage"]=["other"]
        with self.assertRaises(neik.ContractError): neik.parse_envelope(envelope([a],quorum=1))

    def test_count_limit(self):
        xs=[base_evidence(f"e{i}",source=f"s{i}") for i in range(3)]
        x=envelope(xs,quorum=1); x["policy"]["max_evidence_nodes"]=2
        with self.assertRaises(neik.ContractError): neik.parse_envelope(x)


class SolverExhaustiveTests(unittest.TestCase):
    def _node(self,i,edges):
        tags=[f"edge:{a}:{b}" for a,b in sorted(edges) if i in (a,b)]
        e=neik.Evidence(id=f"e{i}",claim_id="c",target_revision="r",evidence_class=neik.EvidenceClass.E2,verdict="PASS",producer_id=f"p{i}",subjects_under_test=(),external_oracle=True,blind=True,derived_from=(),source_lineage=tuple(tags),producer_lineage=(f"p{i}",),oracle_lineage=(f"o{i}",),artifact_hash=f"h{i}")
        return neik.ClosedEvidence(e,{"source_lineage":tuple(tags),"producer_lineage":(f"p{i}",),"oracle_lineage":(f"o{i}",),"artifact_identity":(f"h{i}",)})

    def _brute(self,n,edges):
        best=()
        for mask in range(1<<n):
            ids=tuple(f"e{i}" for i in range(n) if mask&(1<<i))
            if len(ids)<len(best): continue
            chosen=[i for i in range(n) if mask&(1<<i)]
            if any((min(a,b),max(a,b)) in edges for a,b in itertools.combinations(chosen,2)): continue
            if len(ids)>len(best) or not best or ids<best: best=ids
        return best

    def test_all_graphs_up_to_five_vertices(self):
        for n in range(1,6):
            possible=list(itertools.combinations(range(n),2))
            for bits in range(1<<len(possible)):
                edges={e for j,e in enumerate(possible) if bits&(1<<j)}
                got=neik.maximum_independent_witness([self._node(i,edges) for i in range(n)],("source_lineage","artifact_identity"),max_states=100000)
                self.assertEqual(got.ids,self._brute(n,edges),(n,edges,got))


class CliTests(unittest.TestCase):
    def test_cli_pass_and_nonpass_exit_codes(self):
        good=envelope([base_evidence("a",source="s1")],quorum=1,dims=["source_lineage"])
        bad=envelope([base_evidence("a",source="same"),base_evidence("b",source="same")],quorum=2,dims=["source_lineage"])
        for payload,rc,status in ((good,0,"PASS"),(bad,1,"NOT_VERIFIED")):
            p=ROOT/"tests"/"_tmp.json"; p.write_text(json.dumps(payload),encoding="utf-8")
            try:
                cp=subprocess.run([sys.executable,str(ROOT/"src"/"neik.py"),str(p)],text=True,capture_output=True,check=False)
            finally:
                p.unlink(missing_ok=True)
            self.assertEqual(cp.returncode,rc,cp.stderr)
            self.assertEqual(json.loads(cp.stdout)["status"],status)


if __name__ == "__main__":
    unittest.main()
