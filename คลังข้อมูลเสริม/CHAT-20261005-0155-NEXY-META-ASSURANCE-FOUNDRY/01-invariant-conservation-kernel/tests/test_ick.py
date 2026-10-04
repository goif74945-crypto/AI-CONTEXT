import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from ick import ContractError, Snapshot, TransitionReceipt, evaluate_transition


class InvariantConservationKernelTests(unittest.TestCase):
    def base(self):
        return Snapshot.build(
            authority_level=1,
            evidence_level=1,
            unknowns=["u1", "u2"],
            constraints=["c1", "c2"],
            capabilities=["read"],
            side_effects=[],
        )

    def test_safe_strengthening_passes(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=1,
            evidence_level=1,
            unknowns=["u1", "u2", "u3"],
            constraints=["c1", "c2", "c3"],
            capabilities=[],
            side_effects=[],
        )
        report = evaluate_transition(before, after)
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.action, "RELEASE")

    def test_authority_inflation_freezes(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=2,
            evidence_level=1,
            unknowns=before.unknowns,
            constraints=before.constraints,
            capabilities=before.capabilities,
        )
        report = evaluate_transition(before, after)
        self.assertIn("AUTHORITY_INFLATION", report.reason_codes)

    def test_authority_grant_allows_increase(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=2,
            evidence_level=1,
            unknowns=before.unknowns,
            constraints=before.constraints,
            capabilities=before.capabilities,
        )
        receipt = TransitionReceipt.build(authority_grant_id="grant-1")
        self.assertEqual(evaluate_transition(before, after, receipt).status, "PASS")

    def test_evidence_inflation_requires_reference(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=1,
            evidence_level=2,
            unknowns=before.unknowns,
            constraints=before.constraints,
            capabilities=before.capabilities,
        )
        self.assertIn("EVIDENCE_INFLATION", evaluate_transition(before, after).reason_codes)
        receipt = TransitionReceipt.build(evidence_refs=["E2:test-123"])
        self.assertEqual(evaluate_transition(before, after, receipt).status, "PASS")

    def test_unknown_cannot_disappear_without_resolution(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=1,
            evidence_level=1,
            unknowns=["u2"],
            constraints=before.constraints,
            capabilities=before.capabilities,
        )
        report = evaluate_transition(before, after)
        self.assertEqual(report.details["unresolved_removed_unknowns"], ("u1",))
        receipt = TransitionReceipt.build(resolved_unknowns=["u1"])
        self.assertEqual(evaluate_transition(before, after, receipt).status, "PASS")

    def test_constraint_cannot_disappear_without_waiver(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=1,
            evidence_level=1,
            unknowns=before.unknowns,
            constraints=["c2"],
            capabilities=before.capabilities,
        )
        self.assertIn("CONSTRAINT_WEAKENING", evaluate_transition(before, after).reason_codes)
        receipt = TransitionReceipt.build(waived_constraints=["c1"])
        self.assertEqual(evaluate_transition(before, after, receipt).status, "PASS")

    def test_capability_growth_requires_grant(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=1,
            evidence_level=1,
            unknowns=before.unknowns,
            constraints=before.constraints,
            capabilities=["read", "write"],
        )
        self.assertIn("CAPABILITY_ESCALATION", evaluate_transition(before, after).reason_codes)
        receipt = TransitionReceipt.build(granted_capabilities=["write"])
        self.assertEqual(evaluate_transition(before, after, receipt).status, "PASS")

    def test_side_effect_requires_capability_even_with_grant_receipt(self):
        before = self.base()
        after = Snapshot.build(
            authority_level=1,
            evidence_level=1,
            unknowns=before.unknowns,
            constraints=before.constraints,
            capabilities=["read"],
            side_effects=["write"],
        )
        report = evaluate_transition(before, after, TransitionReceipt.build(granted_capabilities=["write"]))
        self.assertIn("SIDE_EFFECT_WITHOUT_CAPABILITY", report.reason_codes)

    def test_input_order_does_not_change_fingerprint(self):
        a = Snapshot.build(
            authority_level=1, evidence_level=1,
            unknowns=["b", "a"], constraints=["y", "x"], capabilities=["r"], side_effects=[]
        )
        b = Snapshot.build(
            authority_level=1, evidence_level=1,
            unknowns=["a", "b"], constraints=["x", "y"], capabilities=["r"], side_effects=[]
        )
        self.assertEqual(evaluate_transition(a, a).fingerprint, evaluate_transition(b, b).fingerprint)

    def test_invalid_values_fail_contract(self):
        with self.assertRaises(ContractError):
            Snapshot.build(authority_level=-1, evidence_level=0)
        with self.assertRaises(ContractError):
            Snapshot.build(authority_level=0, evidence_level=0, unknowns=[""])


if __name__ == "__main__":
    unittest.main()
