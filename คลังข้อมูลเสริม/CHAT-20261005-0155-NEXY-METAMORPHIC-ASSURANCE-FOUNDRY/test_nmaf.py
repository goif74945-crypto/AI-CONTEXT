import math
import unittest

from nmaf import *


class NMAFTests(unittest.TestCase):
    def test_01_canonical_order(self):
        self.assertEqual(canonical_sha256({"b":2,"a":1}), canonical_sha256({"a":1,"b":2}))

    def test_02_nan_rejected(self):
        with self.assertRaises(CanonicalizationError): canonical_json({"x":math.nan})

    def test_03_nonstring_key_rejected(self):
        with self.assertRaises(CanonicalizationError): canonical_json({1:"x"})

    def test_04_relation_order_passes(self):
        r=MetamorphicRelation("MR-ORDER","order invariant",reorder_mapping_insertion,outputs_equal)
        out=run_relation(r,{"a":2,"b":3},lambda x:{"sum":x["a"]+x["b"]})
        self.assertTrue(out.passed)
        self.assertEqual(out.base_input_hash,out.mutated_input_hash)

    def test_05_relation_semantic_change(self):
        r=MetamorphicRelation("MR-SET","decisive change",lambda x:set_path(x,("v",),9),lambda a,b:a!=b)
        self.assertTrue(run_relation(r,{"v":1},lambda x:{"v":x["v"]}).passed)

    def test_06_missing_path_rejected(self):
        with self.assertRaises(KeyError): set_path({"a":1},("x",),2)

    def test_07_executor_error_not_masked(self):
        r=MetamorphicRelation("MR-X","runtime error",lambda x:x,outputs_equal)
        def boom(_): raise RuntimeError("boom")
        with self.assertRaises(RuntimeError): run_relation(r,{"a":1},boom)

    def test_08_shrinker_reduces(self):
        x={"noise":[1,2,3],"trigger":"boom","other":{"x":1}}
        result=minimize_counterexample(x,lambda y:isinstance(y,dict) and y.get("trigger")=="boom")
        self.assertEqual(result.minimized,{"trigger":"boom"})

    def test_09_shrinker_requires_failure(self):
        with self.assertRaises(ValueError): minimize_counterexample({"x":1},lambda _:False)

    def test_10_shrinker_budget(self):
        result=minimize_counterexample([1,2,3,4],lambda x:len(x)>=2,max_evaluations=2)
        self.assertLessEqual(result.evaluations,2)

    def test_11_oracle_independent(self):
        a=ArtifactDescriptor("sut",frozenset({"impl"}),"A")
        b=ArtifactDescriptor("oracle",frozenset({"spec"}),"B")
        self.assertTrue(audit_oracle_independence(a,b).independent)

    def test_12_oracle_shared_source(self):
        a=ArtifactDescriptor("sut",frozenset({"shared","impl"}),"A")
        b=ArtifactDescriptor("oracle",frozenset({"shared","spec"}),"B")
        self.assertIn("ORACLE_SHARED_SOURCE",audit_oracle_independence(a,b).reason_codes)

    def test_13_oracle_approved_shared_schema(self):
        a=ArtifactDescriptor("sut",frozenset({"schema","impl"}),"A")
        b=ArtifactDescriptor("oracle",frozenset({"schema","spec"}),"B")
        self.assertTrue(audit_oracle_independence(a,b,approved_shared_sources=frozenset({"schema"})).independent)

    def test_14_oracle_same_logic(self):
        a=ArtifactDescriptor("sut",frozenset({"a"}),"SAME")
        b=ArtifactDescriptor("oracle",frozenset({"b"}),"SAME")
        self.assertIn("ORACLE_IDENTICAL_LOGIC_FINGERPRINT",audit_oracle_independence(a,b).reason_codes)

    def test_15_mandatory_over_budget_freezes(self):
        r=schedule_tests([TestCandidate("must",1.0,frozenset({"law"}),5.0,mandatory=True)],4.0)
        self.assertTrue(r.freeze_required)
        self.assertEqual(r.selected_ids,())

    def test_16_mandatory_first(self):
        r=schedule_tests([TestCandidate("opt",1.0,frozenset({"x"}),1),TestCandidate("must",0.1,frozenset({"law"}),1,mandatory=True)],2)
        self.assertEqual(r.selected_ids[0],"must")

    def test_17_scheduler_deterministic(self):
        xs=[TestCandidate("A",.5,frozenset({"i1"}),1),TestCandidate("B",.5,frozenset({"i2"}),1),TestCandidate("C",.9,frozenset({"i1","i2"}),2)]
        self.assertEqual(schedule_tests(xs,2).selected_ids,schedule_tests(list(reversed(xs)),2).selected_ids)

    def test_18_duplicate_test_ids_rejected(self):
        with self.assertRaises(ValueError): schedule_tests([TestCandidate("A",.5,frozenset(),1),TestCandidate("A",.6,frozenset(),1)],2)

    def test_19_volatile_fingerprint(self):
        a=FailureRecord("INV","VERIFY","MR","MISMATCH",{"trace_id":"a","x":1})
        b=FailureRecord("INV","VERIFY","MR","MISMATCH",{"trace_id":"b","x":1})
        self.assertEqual(semantic_failure_fingerprint(a,volatile_paths=(("trace_id",),)),semantic_failure_fingerprint(b,volatile_paths=(("trace_id",),)))

    def test_20_meaningful_fingerprint_change(self):
        a=FailureRecord("INV","VERIFY","MR","MISMATCH",{"x":1})
        b=FailureRecord("INV","VERIFY","MR","MISMATCH",{"x":2})
        self.assertNotEqual(semantic_failure_fingerprint(a),semantic_failure_fingerprint(b))

    def test_21_truth_surface(self):
        x=extract_truth_surface({"status":"FREEZE","state":"FREEZE","data":None,"error":{"code":"EVIDENCE_MISSING"},"freeze_reason":"proof absent"})
        self.assertEqual(x.error_code,"EVIDENCE_MISSING")

    def test_22_truth_surface_missing_state(self):
        with self.assertRaises(ValueError): extract_truth_surface({"status":"OK"})


if __name__ == "__main__": unittest.main()
