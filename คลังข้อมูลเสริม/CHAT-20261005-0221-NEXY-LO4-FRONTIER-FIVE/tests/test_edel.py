import unittest

from nexy_lo4_frontier import EvidenceArtifact, FrontierInputError, ProofClaim, assess_evidence_debt


class EpistemicDebtLedgerTests(unittest.TestCase):
    def test_current_evidence_passes(self):
        claims = [ProofClaim("policy-evaluator", 2, 10, ("policy.py",))]
        evidence = [EvidenceArtifact("unit-1", ("policy-evaluator",), 2, (("policy.py", "v1"),))]
        report = assess_evidence_debt(claims, evidence, {"policy.py": "v1"})
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.total_debt_points, 0)

    def test_stale_root_propagates_debt_to_dependents(self):
        claims = [
            ProofClaim("core", 2, 50, ("core.py",)),
            ProofClaim("api", 3, 30, ("api.py",), ("core",)),
            ProofClaim("ui-flow", 4, 20, ("ui.ts",), ("api",)),
        ]
        evidence = [
            EvidenceArtifact("e-core", ("core",), 2, (("core.py", "old"),)),
            EvidenceArtifact("e-api", ("api",), 3, (("api.py", "v1"),)),
            EvidenceArtifact("e-ui", ("ui-flow",), 4, (("ui.ts", "v1"),)),
        ]
        report = assess_evidence_debt(claims, evidence, {"core.py": "new", "api.py": "v1", "ui.ts": "v1"})
        self.assertEqual(report.status, "FREEZE")
        self.assertEqual(report.directly_invalid_claims, ("core",))
        self.assertEqual(report.propagated_invalid_claims, ("api", "ui-flow"))
        self.assertEqual(report.reverify_frontier, ("core",))
        self.assertGreater(report.total_debt_points, 0)

    def test_insufficient_evidence_class_is_debt(self):
        claims = [ProofClaim("integration", 3, 10, ("svc",))]
        evidence = [EvidenceArtifact("unit-only", ("integration",), 2, (("svc", "a"),))]
        report = assess_evidence_debt(claims, evidence, {"svc": "a"})
        self.assertEqual(report.status, "FREEZE")
        self.assertIn("INSUFFICIENT_CLASS:unit-only", report.claims[0].reasons)

    def test_unknown_dependency_rejected(self):
        with self.assertRaisesRegex(FrontierInputError, "UNKNOWN_DEPENDENCY"):
            assess_evidence_debt([ProofClaim("a", 1, depends_on=("missing",))], [], {})

    def test_dependency_cycle_rejected(self):
        claims = [
            ProofClaim("a", 1, depends_on=("b",)),
            ProofClaim("b", 1, depends_on=("a",)),
        ]
        with self.assertRaisesRegex(FrontierInputError, "DEPENDENCY_CYCLE"):
            assess_evidence_debt(claims, [], {})

    def test_deterministic_evidence_order(self):
        claims = [ProofClaim("a", 1, 2, ("x",))]
        evidence = [
            EvidenceArtifact("z", ("a",), 1, (("x", "1"),)),
            EvidenceArtifact("a", ("a",), 1, (("x", "1"),)),
        ]
        r1 = assess_evidence_debt(claims, evidence, {"x": "1"})
        r2 = assess_evidence_debt(claims, list(reversed(evidence)), {"x": "1"})
        self.assertEqual(r1.fingerprint, r2.fingerprint)
        self.assertEqual(r1.claims[0].usable_evidence_ids, ("a", "z"))


if __name__ == "__main__":
    unittest.main()
