import unittest

from negative_space_coverage_analyzer.engine import Evidence, Requirement, analyze_negative_space


class NegativeSpaceCoverageAnalyzerTests(unittest.TestCase):
    def test_positive_test_does_not_cover_prohibition(self):
        reqs = [Requirement("R1", "MUST_NOT", "must not emit unverified output")]
        evs = [Evidence("T-positive", frozenset({"R1"}), "positive", "PASS", "E2")]
        report = analyze_negative_space(reqs, evs)
        self.assertEqual(report.missing, 1)
        self.assertEqual(report.findings[0].misleading_positive_ids, ("T-positive",))

    def test_passing_negative_behavior_test_covers_requirement(self):
        reqs = [Requirement("R1", "FREEZE_ON", "freeze on missing authority")]
        evs = [Evidence("T-deny", frozenset({"R1"}), "negative", "PASS", "E2")]
        report = analyze_negative_space(reqs, evs)
        self.assertEqual(report.covered, 1)
        self.assertEqual(report.coverage_ratio, 1.0)

    def test_failed_or_static_negative_evidence_does_not_count_by_default(self):
        reqs = [Requirement("R1", "DENY")]
        evs = [
            Evidence("T-fail", frozenset({"R1"}), "negative", "FAIL", "E2"),
            Evidence("T-static", frozenset({"R1"}), "negative", "PASS", "E1"),
        ]
        report = analyze_negative_space(reqs, evs)
        self.assertEqual(report.missing, 1)
        self.assertEqual(set(report.findings[0].failed_negative_ids), {"T-fail", "T-static"})

    def test_positive_obligations_are_out_of_scope(self):
        reqs = [Requirement("R1", "MUST")]
        report = analyze_negative_space(reqs, [])
        self.assertEqual(report.negative_requirements, 0)
        self.assertEqual(report.coverage_ratio, 1.0)

    def test_custom_evidence_class_policy_is_explicit(self):
        reqs = [Requirement("R1", "FORBID")]
        evs = [Evidence("T-static", frozenset({"R1"}), "negative", "PASS", "E1")]
        default = analyze_negative_space(reqs, evs)
        custom = analyze_negative_space(reqs, evs, accepted_evidence_classes=frozenset({"E1"}))
        self.assertEqual(default.missing, 1)
        self.assertEqual(custom.covered, 1)

    def test_duplicate_evidence_ids_are_rejected(self):
        reqs = [Requirement("R1", "DENY")]
        evs = [
            Evidence("T", frozenset({"R1"}), "negative", "PASS", "E2"),
            Evidence("T", frozenset({"R1"}), "negative", "PASS", "E2"),
        ]
        with self.assertRaisesRegex(ValueError, "evidence_id"):
            analyze_negative_space(reqs, evs)


if __name__ == "__main__":
    unittest.main()
