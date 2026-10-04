import unittest

from lo4lab.contract_drift import ContractDriftPolicy, analyze_contract_drift


BASE = {
    "authorized_scope": ["read-context", "build-prototype"],
    "success_invariants": ["no-nexy-write", "tests-pass"],
    "forbidden_actions": ["mutate-nexy", "store-secret"],
    "assumptions": [],
    "required_evidence": ["unit-tests", "readback"],
}


class ContractDriftTests(unittest.TestCase):
    def test_identical_contract_passes(self):
        report = analyze_contract_drift(BASE, dict(BASE))
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.total_cost, 0)

    def test_scope_expansion_freezes(self):
        after = {**BASE, "authorized_scope": [*BASE["authorized_scope"], "deploy-production"]}
        report = analyze_contract_drift(BASE, after)
        self.assertEqual(report.status, "FREEZE")
        self.assertTrue(any(r.startswith("scope_expansion:") for r in report.reasons))

    def test_invariant_and_evidence_weakening_freezes(self):
        after = {
            **BASE,
            "success_invariants": ["no-nexy-write"],
            "required_evidence": ["unit-tests"],
        }
        report = analyze_contract_drift(BASE, after)
        self.assertEqual(report.status, "FREEZE")
        self.assertTrue(any(r.startswith("invariant_removed:") for r in report.reasons))
        self.assertTrue(any(r.startswith("required_evidence_removed:") for r in report.reasons))

    def test_explicit_approval_can_allow_targeted_change(self):
        after = {**BASE, "authorized_scope": [*BASE["authorized_scope"], "extra-read"]}
        report = analyze_contract_drift(
            BASE,
            after,
            approved_event_ids=["scope_expansion:extra-read"],
        )
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.total_cost, 0)

    def test_small_scope_narrowing_has_budget_cost(self):
        after = {**BASE, "authorized_scope": ["read-context"]}
        report = analyze_contract_drift(BASE, after, policy=ContractDriftPolicy(max_total_cost=1))
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.total_cost, 1)


if __name__ == "__main__":
    unittest.main()
