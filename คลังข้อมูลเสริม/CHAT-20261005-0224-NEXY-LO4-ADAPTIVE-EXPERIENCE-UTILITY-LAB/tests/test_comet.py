import unittest

from aeul.comet import OverlapEvidence, evaluate_marginal_value
from aeul.q64 import Q64

q = Q64.from_decimal


class CometTests(unittest.TestCase):
    def test_marginal_value_uses_max_overlap(self):
        evidence = [
            OverlapEvidence("new", "a", q("0.25"), "audit:a"),
            OverlapEvidence("new", "b", q("0.5"), "audit:b"),
        ]
        r = evaluate_marginal_value(candidate_id="new", base_value=q("0.8"), selected_ids=["a", "b"], evidence=evidence, max_allowed_overlap=q("0.6"))
        self.assertEqual(r.status, "VALUE")
        self.assertEqual(r.max_overlap, q("0.5"))
        self.assertEqual(r.retention, q("0.5"))
        self.assertEqual(r.marginal_value, q("0.4"))

    def test_high_overlap_is_collision(self):
        e = [OverlapEvidence("new", "a", q("0.9"), "audit")]
        r = evaluate_marginal_value(candidate_id="new", base_value=q("1"), selected_ids=["a"], evidence=e, max_allowed_overlap=q("0.8"))
        self.assertEqual(r.status, "COLLISION")

    def test_missing_overlap_evidence_freezes(self):
        r = evaluate_marginal_value(candidate_id="new", base_value=q("1"), selected_ids=["a"], evidence=[], max_allowed_overlap=q("0.8"))
        self.assertEqual(r.status, "FREEZE")
        self.assertTrue(r.reason.startswith("MISSING_OVERLAP_EVIDENCE"))

    def test_conflicting_duplicate_evidence_freezes(self):
        e = [
            OverlapEvidence("new", "a", q("0.2"), "audit-1"),
            OverlapEvidence("a", "new", q("0.3"), "audit-2"),
        ]
        r = evaluate_marginal_value(candidate_id="new", base_value=q("1"), selected_ids=["a"], evidence=e, max_allowed_overlap=q("0.8"))
        self.assertEqual(r.status, "FREEZE")
        self.assertEqual(r.reason, "CONFLICTING_OVERLAP_EVIDENCE")

    def test_no_selected_baseline_retains_full_value(self):
        r = evaluate_marginal_value(candidate_id="new", base_value=q("0.7"), selected_ids=[], evidence=[], max_allowed_overlap=q("0.8"))
        self.assertEqual(r.status, "VALUE")
        self.assertEqual(r.marginal_value, q("0.7"))

    def test_input_order_deterministic(self):
        e = [OverlapEvidence("new", "a", q("0.2"), "a"), OverlapEvidence("new", "b", q("0.4"), "b")]
        x = evaluate_marginal_value(candidate_id="new", base_value=q("0.7"), selected_ids=["a", "b"], evidence=e, max_allowed_overlap=q("0.8"))
        y = evaluate_marginal_value(candidate_id="new", base_value=q("0.7"), selected_ids=["b", "a"], evidence=list(reversed(e)), max_allowed_overlap=q("0.8"))
        self.assertEqual(x.fingerprint, y.fingerprint)
