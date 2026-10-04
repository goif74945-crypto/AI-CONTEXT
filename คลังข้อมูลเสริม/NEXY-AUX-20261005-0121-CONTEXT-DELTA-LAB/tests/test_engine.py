import copy
import unittest

from context_delta_lab.engine import DeltaEngine, ValidationError, sha256_json, validate_snapshot


def rec(record_id, authority="DOC_C", scope="CURRENT_BUILD", statement="x", evidence="E2", deps=None):
    return {
        "id": record_id,
        "authority": authority,
        "scope": scope,
        "statement": statement,
        "evidence_class": evidence,
        "depends_on": deps or [],
    }


def snap(snapshot_id, records):
    return {"snapshot_id": snapshot_id, "source_commit": snapshot_id * 4, "requirements": records}


class ValidationTests(unittest.TestCase):
    def test_duplicate_id_freezes(self):
        with self.assertRaisesRegex(ValidationError, "duplicate"):
            validate_snapshot(snap("a", [rec("R1"), rec("R1")]))

    def test_missing_dependency_freezes(self):
        with self.assertRaisesRegex(ValidationError, "missing dependency"):
            validate_snapshot(snap("a", [rec("R1", deps=["MISSING"])]))

    def test_cycle_freezes(self):
        with self.assertRaisesRegex(ValidationError, "dependency cycle"):
            validate_snapshot(snap("a", [rec("A", deps=["B"]), rec("B", deps=["A"])]))

    def test_unknown_authority_freezes(self):
        with self.assertRaisesRegex(ValidationError, "unknown authority"):
            validate_snapshot(snap("a", [rec("R", authority="MYSTERY")]))

    def test_whitespace_normalization_is_deterministic(self):
        a = snap("x", [rec("R", statement="one   two\nthree")])
        b = snap("x", [rec("R", statement="one two three")])
        self.assertEqual(validate_snapshot(a)["fingerprint"], validate_snapshot(b)["fingerprint"])


class DeltaTests(unittest.TestCase):
    def test_no_change_yields_empty_queue(self):
        base = snap("a", [rec("R1")])
        current = copy.deepcopy(base)
        report = DeltaEngine().compare(base, current)
        self.assertEqual(report["summary"]["change_count"], 0)
        self.assertEqual(report["revalidation_queue"], [])

    def test_statement_change_propagates_to_dependents(self):
        base = snap("a", [rec("LAW", authority="DOC_B", scope="CURRENT_GOVERNING_LAW"), rec("BUILD", deps=["LAW"]), rec("UI", authority="DOC_D", scope="SUPPORTED_PRODUCT_DESIGN", deps=["BUILD"])])
        current = copy.deepcopy(base)
        current["snapshot_id"] = "b"
        current["source_commit"] = "bbbb"
        current["requirements"][0]["statement"] = "changed"
        report = DeltaEngine().compare(base, current)
        ids = [q["record_id"] for q in report["revalidation_queue"]]
        self.assertEqual(set(ids), {"LAW", "BUILD", "UI"})
        self.assertEqual(report["revalidation_queue"][0]["record_id"], "LAW")
        self.assertTrue(all(q["status"] == "NOT_VERIFIED" for q in report["revalidation_queue"]))

    def test_authority_change_touching_doc_c_is_critical(self):
        base = snap("a", [rec("R", authority="DOC_D", scope="SUPPORTED_PRODUCT_DESIGN")])
        current = snap("b", [rec("R", authority="DOC_C", scope="CURRENT_BUILD")])
        report = DeltaEngine().compare(base, current)
        self.assertEqual(report["changes"][0]["severity"], "CRITICAL")
        self.assertIn("AUTHORITY_CHANGED", report["changes"][0]["reasons"])

    def test_removed_current_build_is_critical(self):
        base = snap("a", [rec("R")])
        current = snap("b", [])
        report = DeltaEngine().compare(base, current)
        self.assertEqual(report["changes"][0]["kind"], "REMOVED")
        self.assertEqual(report["changes"][0]["severity"], "CRITICAL")

    def test_added_deployment_evidence_is_high(self):
        base = snap("a", [])
        current = snap("b", [rec("D", authority="DOC_E", scope="DEPLOYMENT_EVIDENCE", evidence="E6")])
        report = DeltaEngine().compare(base, current)
        self.assertEqual(report["changes"][0]["severity"], "HIGH")

    def test_report_fingerprint_is_repeatable(self):
        base = snap("a", [rec("R")])
        current = snap("b", [rec("R", statement="changed")])
        first = DeltaEngine().compare(base, current)
        second = DeltaEngine().compare(base, current)
        self.assertEqual(first, second)
        self.assertEqual(first["report_fingerprint"], second["report_fingerprint"])

    def test_multiple_paths_do_not_duplicate_queue_record(self):
        base = snap("a", [rec("A"), rec("B", deps=["A"]), rec("C", deps=["A"]), rec("D", deps=["B", "C"])])
        current = copy.deepcopy(base)
        current["snapshot_id"] = "b"
        current["source_commit"] = "bbbb"
        current["requirements"][0]["statement"] = "changed"
        queue = DeltaEngine().compare(base, current)["revalidation_queue"]
        ids = [q["record_id"] for q in queue]
        self.assertEqual(ids.count("D"), 1)

    def test_fingerprint_changes_on_semantic_change(self):
        base = snap("a", [rec("R", statement="one")])
        changed = snap("a", [rec("R", statement="two")])
        self.assertNotEqual(validate_snapshot(base)["fingerprint"], validate_snapshot(changed)["fingerprint"])

    def test_union_graph_edge_reversal_terminates_deterministically(self):
        base = snap("a", [rec("A"), rec("B", deps=["A"])])
        current = snap("b", [rec("A", deps=["B"]), rec("B")])
        report = DeltaEngine().compare(base, current)
        ids = [q["record_id"] for q in report["revalidation_queue"]]
        self.assertEqual(set(ids), {"A", "B"})
        self.assertEqual(len(ids), 2)


if __name__ == "__main__":
    unittest.main()
