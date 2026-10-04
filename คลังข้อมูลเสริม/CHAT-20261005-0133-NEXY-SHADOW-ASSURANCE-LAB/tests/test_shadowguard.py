from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from shadowguard.canonical import canonical_json, mapping_digest
from shadowguard.gate import evaluate_datasets
from shadowguard.io import load_jsonl
from shadowguard.models import DecisionRecord


def record(**overrides):
    base = {
        "case_id": "c1",
        "input_fingerprint": "input:aaa",
        "revision": "rev-2",
        "policy_fingerprint": "policy:p1",
        "authority_chain": ["USER_LAW", "NEXY_LAW", "JUDGE"],
        "outcome": "RELEASE",
        "action": "return:verified-result",
        "required_evidence_classes": ["E2", "E3"],
        "evidence": [
            {"class": "E2", "ref": "unit:1", "revision": "rev-2"},
            {"class": "E3", "ref": "integration:1", "revision": "rev-2"},
        ],
        "safety_labels": ["safe-output"],
    }
    base.update(overrides)
    return DecisionRecord.from_mapping(base)


class ShadowGuardTests(unittest.TestCase):
    def test_identical_pair_passes(self):
        r = record()
        report = evaluate_datasets([r], [r])
        self.assertEqual("PASS", report.status)
        self.assertEqual({"MATCH"}, {x.code for x in report.findings})

    def test_freeze_bypass_blocks(self):
        stable = record(outcome="FREEZE", action=None)
        candidate = record(outcome="RELEASE", action="do-it")
        report = evaluate_datasets([stable], [candidate])
        self.assertEqual("FAIL", report.status)
        self.assertIn("FREEZE_BYPASS", {x.code for x in report.findings})

    def test_authority_regression_blocks(self):
        candidate = record(authority_chain=["NEXY_LAW", "JUDGE"])
        report = evaluate_datasets([record()], [candidate])
        self.assertIn("AUTHORITY_REGRESSION", {x.code for x in report.findings})

    def test_authority_extension_is_allowed(self):
        candidate = record(authority_chain=["USER_LAW", "NEXY_LAW", "JUDGE", "WORKER"])
        report = evaluate_datasets([record()], [candidate])
        self.assertEqual("PASS", report.status)

    def test_required_evidence_missing_blocks(self):
        candidate = record(evidence=[{"class": "E2", "ref": "unit:1", "revision": "rev-2"}])
        report = evaluate_datasets([record()], [candidate])
        self.assertIn("MISSING_REQUIRED_EVIDENCE", {x.code for x in report.findings})

    def test_evidence_profile_downgrade_blocks(self):
        candidate = record(
            required_evidence_classes=["E2"],
            evidence=[{"class": "E2", "ref": "unit:1", "revision": "rev-2"}],
        )
        report = evaluate_datasets([record()], [candidate])
        self.assertIn("EVIDENCE_PROFILE_DOWNGRADE", {x.code for x in report.findings})

    def test_stale_evidence_blocks(self):
        candidate = record(
            evidence=[
                {"class": "E2", "ref": "unit:1", "revision": "rev-old"},
                {"class": "E3", "ref": "integration:1", "revision": "rev-2"},
            ]
        )
        report = evaluate_datasets([record()], [candidate])
        self.assertIn("STALE_EVIDENCE", {x.code for x in report.findings})

    def test_policy_drift_blocks_comparison(self):
        candidate = record(policy_fingerprint="policy:p2")
        report = evaluate_datasets([record()], [candidate])
        self.assertIn("POLICY_DRIFT", {x.code for x in report.findings})

    def test_input_mismatch_short_circuits(self):
        candidate = record(input_fingerprint="input:bbb")
        report = evaluate_datasets([record()], [candidate])
        codes = {x.code for x in report.findings}
        self.assertIn("INPUT_MISMATCH", codes)
        self.assertNotIn("ACTION_DIVERGENCE", codes)

    def test_action_divergence_blocks(self):
        candidate = record(action="return:different")
        report = evaluate_datasets([record()], [candidate])
        self.assertIn("ACTION_DIVERGENCE", {x.code for x in report.findings})

    def test_candidate_more_conservative_is_not_verified(self):
        candidate = record(outcome="FREEZE", action=None)
        report = evaluate_datasets([record()], [candidate])
        self.assertEqual("NOT_VERIFIED", report.status)
        self.assertIn("CONSERVATIVE_DIVERGENCE", {x.code for x in report.findings})

    def test_safety_label_regression_blocks(self):
        candidate = record(safety_labels=[])
        report = evaluate_datasets([record()], [candidate])
        self.assertIn("SAFETY_LABEL_REGRESSION", {x.code for x in report.findings})

    def test_missing_candidate_case_blocks(self):
        report = evaluate_datasets([record()], [])
        self.assertEqual("FAIL", report.status)
        self.assertIn("COVERAGE_GAP", {x.code for x in report.findings})

    def test_unbaselined_candidate_is_not_verified(self):
        report = evaluate_datasets([], [record()])
        self.assertEqual("NOT_VERIFIED", report.status)
        self.assertIn("UNBASELINED_CASE", {x.code for x in report.findings})

    def test_nondeterministic_duplicate_blocks(self):
        a = record()
        b = record(action="return:different")
        report = evaluate_datasets([a], [a, b])
        self.assertEqual("FAIL", report.status)
        self.assertIn("NONDETERMINISTIC_CANDIDATE", {x.code for x in report.findings})

    def test_identical_duplicate_is_not_verified(self):
        a = record()
        report = evaluate_datasets([a], [a, a])
        self.assertEqual("NOT_VERIFIED", report.status)
        self.assertIn("DUPLICATE_IDENTICAL_CANDIDATE", {x.code for x in report.findings})

    def test_record_validation_rejects_action_on_freeze(self):
        with self.assertRaises(ValueError):
            record(outcome="FREEZE", action="forbidden")

    def test_canonical_json_ignores_mapping_order(self):
        a = {"b": 2, "a": 1}
        b = {"a": 1, "b": 2}
        self.assertEqual(canonical_json(a), canonical_json(b))
        self.assertEqual(mapping_digest(a), mapping_digest(b))

    def test_jsonl_loader_reports_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.jsonl"
            path.write_text('{"case_id": "x"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r":1:"):
                load_jsonl(path)


if __name__ == "__main__":
    unittest.main()
