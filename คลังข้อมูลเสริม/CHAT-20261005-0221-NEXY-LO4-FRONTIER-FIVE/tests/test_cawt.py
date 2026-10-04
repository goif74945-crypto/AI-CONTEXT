import unittest

from nexy_lo4_frontier import AuthorityRule, DecisionCase, FrontierInputError, evaluate_policy, simulate_authority_change


class CounterfactualAuthorityWindTunnelTests(unittest.TestCase):
    def setUp(self):
        self.cases = [
            DecisionCase("admin-read", "admin", "read", "vault/alpha", (("role", "admin"),)),
            DecisionCase("user-read", "user", "read", "vault/alpha", (("role", "user"),)),
            DecisionCase("user-delete", "user", "delete", "vault/alpha", (("role", "user"),)),
        ]
        self.baseline = [
            AuthorityRule("deny-delete", 100, "DENY", "delete", "vault/*"),
            AuthorityRule("allow-admin-read", 90, "ALLOW", "read", "vault/*", (("role", "admin"),)),
            AuthorityRule("deny-user-read", 80, "DENY", "read", "vault/*", (("role", "user"),)),
        ]

    def test_dangerous_authority_expansion_freezes(self):
        candidate = [
            AuthorityRule("deny-delete", 100, "DENY", "delete", "vault/*"),
            AuthorityRule("allow-all-read", 95, "ALLOW", "read", "vault/*"),
        ]
        report = simulate_authority_change(self.baseline, candidate, self.cases)
        self.assertEqual(report.status, "FREEZE")
        self.assertEqual(report.dangerous_divergence_count, 1)
        self.assertEqual(report.minimal_witness.case_id, "user-read")
        self.assertEqual(report.minimal_witness.category, "AUTHORITY_EXPANSION")

    def test_safe_no_change_passes(self):
        report = simulate_authority_change(self.baseline, list(reversed(self.baseline)), reversed(self.cases))
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.divergence_count, 0)
        self.assertEqual(report.blast_radius_bps, 0)

    def test_top_priority_conflict_freezes_decision(self):
        rules = [
            AuthorityRule("a", 10, "ALLOW", "read", "*"),
            AuthorityRule("b", 10, "DENY", "read", "*"),
        ]
        d = evaluate_policy(rules, DecisionCase("c", "x", "read", "r"))
        self.assertEqual(d.state, "FREEZE")
        self.assertEqual(d.reason, "TOP_PRIORITY_CONFLICT")

    def test_duplicate_case_rejected(self):
        with self.assertRaisesRegex(FrontierInputError, "DUPLICATE_CASE_ID"):
            simulate_authority_change(self.baseline, self.baseline, [self.cases[0], self.cases[0]])

    def test_report_is_order_deterministic(self):
        candidate = [AuthorityRule("deny-delete", 100, "DENY", "delete", "vault/*")]
        a = simulate_authority_change(self.baseline, candidate, self.cases)
        b = simulate_authority_change(list(reversed(self.baseline)), candidate, list(reversed(self.cases)))
        self.assertEqual(a.fingerprint, b.fingerprint)


if __name__ == "__main__":
    unittest.main()
