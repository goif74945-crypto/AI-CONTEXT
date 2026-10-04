import unittest

from assurance_harness import generate_boundary_corpus, run_assurance
from human_agency_lab import AgencyPolicy


class AssuranceHarnessTests(unittest.TestCase):
    def test_boundary_corpus_is_deterministic(self):
        a = generate_boundary_corpus()
        b = generate_boundary_corpus()
        self.assertEqual(a, b)

    def test_boundary_corpus_is_unique_by_full_request(self):
        corpus = generate_boundary_corpus()
        serialized = [str(request.canonical_dict()) for request in corpus]
        self.assertEqual(len(serialized), len(set(serialized)))

    def test_default_assurance_passes(self):
        report = run_assurance()
        self.assertTrue(report.passed, report.failures)
        self.assertGreater(report.corpus_size, 100)
        self.assertGreater(report.total_checks, report.corpus_size)
        self.assertEqual(report.failures, tuple())

    def test_report_digest_repeatability(self):
        digests = {run_assurance().digest() for _ in range(10)}
        self.assertEqual(len(digests), 1)

    def test_custom_policy_assurance_passes(self):
        policy = AgencyPolicy(
            preview_ambiguity=0.2,
            confirm_ambiguity=0.55,
            freeze_ambiguity=0.85,
            low_reversibility=0.25,
            broad_scope=0.65,
            sensitive_data=0.6,
            material_cost=0.45,
            low_confidence=0.6,
            high_impact_scope=0.55,
        )
        report = run_assurance(policy)
        self.assertTrue(report.passed, report.failures)

    def test_check_denominators_are_nonzero(self):
        report = run_assurance()
        self.assertGreater(report.determinism_checks, 0)
        self.assertGreater(report.hard_gate_budget_checks, 0)
        self.assertGreater(report.monotonicity_checks, 0)
        self.assertGreater(report.authority_removal_checks, 0)
        self.assertGreater(report.destructive_rollback_checks, 0)


if __name__ == "__main__":
    unittest.main()
