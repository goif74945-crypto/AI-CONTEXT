import unittest

from nexy_lo4_frontier import Capability, ForbiddenPrivilegeSet, analyze_capability_composition


class CapabilityCompositionFirewallTests(unittest.TestCase):
    def setUp(self):
        self.rules = [ForbiddenPrivilegeSet("secret-exfiltration", frozenset({"secret-read", "network-egress"}))]
        self.caps = [
            Capability("read-vault", frozenset({"authenticated"}), frozenset({"secret-read"}), "project"),
            Capability("prepare-http", frozenset({"authenticated"}), frozenset({"http-client"}), "project"),
            Capability("send-http", frozenset({"http-client"}), frozenset({"network-egress"}), "project"),
        ]

    def test_dangerous_composition_freezes_with_minimal_witness(self):
        report = analyze_capability_composition(self.caps, ["authenticated"], self.rules, allowed_scopes=frozenset({"project"}))
        self.assertEqual(report.status, "FREEZE")
        self.assertEqual(report.violated_rules, ("secret-exfiltration",))
        self.assertIn("read-vault", report.witness_capabilities)
        self.assertIn("send-http", report.witness_capabilities)

    def test_scope_lock_prevents_composition(self):
        caps = [
            Capability("read-vault", frozenset({"authenticated"}), frozenset({"secret-read"}), "project"),
            Capability("send-http", frozenset({"authenticated"}), frozenset({"network-egress"}), "external"),
        ]
        report = analyze_capability_composition(caps, ["authenticated"], self.rules, allowed_scopes=frozenset({"project"}))
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.violated_rules, ())

    def test_initial_violation_is_detected(self):
        report = analyze_capability_composition([], ["secret-read", "network-egress"], self.rules, allowed_scopes=frozenset())
        self.assertEqual(report.status, "FREEZE")
        self.assertEqual(report.witness_capabilities, ())

    def test_order_deterministic(self):
        a = analyze_capability_composition(self.caps, ["authenticated"], self.rules, allowed_scopes=frozenset({"project"}))
        b = analyze_capability_composition(list(reversed(self.caps)), ["authenticated"], list(reversed(self.rules)), allowed_scopes=frozenset({"project"}))
        self.assertEqual(a.fingerprint, b.fingerprint)
        self.assertEqual(a.witness_capabilities, b.witness_capabilities)


if __name__ == "__main__":
    unittest.main()
