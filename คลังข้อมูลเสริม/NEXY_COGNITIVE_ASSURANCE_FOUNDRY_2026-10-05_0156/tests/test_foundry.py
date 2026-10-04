from __future__ import annotations

import unittest

from nexy_caf.contracts import Verdict
from nexy_caf.intent_lattice import IntentLatticeCompiler
from nexy_caf.counterfactual_gate import CounterfactualAdoptionGate, Scenario
from nexy_caf.cognitive_debt import CognitiveDebtLedger, DebtItem, DebtKind
from nexy_caf.proof_horizon import ProofHorizonScheduler, ProofNode
from nexy_caf.trust_budget import HumanTrustBudgetGovernor, TrustContext
from nexy_caf.suite import AssuranceSuite


class IntentLatticeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = IntentLatticeCompiler()

    def test_complete_contract_passes(self) -> None:
        d = self.engine.compile(
            objective="Build advisory evaluator",
            authorized_scope=["AI-CONTEXT/คลังข้อมูลเสริม"],
            protected_scope=["NEXY.AI"],
            invariants=["no NEXY mutation"],
            required_evidence=["E1", "E2"],
            stop_conditions=["scope collision"],
            authority_sources=["user directive"],
        )
        self.assertEqual(d.verdict, Verdict.PASS)
        self.assertEqual(d.score, 100)

    def test_scope_collision_freezes(self) -> None:
        d = self.engine.compile(
            objective="x",
            authorized_scope=["NEXY.AI"],
            protected_scope=["NEXY.AI"],
            invariants=["i"],
            required_evidence=["E2"],
            stop_conditions=["c"],
            authority_sources=["u"],
        )
        self.assertEqual(d.verdict, Verdict.FREEZE)
        self.assertIn("INTENT_SCOPE_COLLISION", {f.code for f in d.findings})

    def test_missing_authority_freezes(self) -> None:
        d = self.engine.compile(
            objective="x",
            authorized_scope=["a"],
            protected_scope=["b"],
            invariants=[],
            required_evidence=["E1"],
            stop_conditions=["s"],
            authority_sources=[],
        )
        self.assertEqual(d.verdict, Verdict.FREEZE)

    def test_output_is_deterministic(self) -> None:
        args = dict(
            objective="x",
            authorized_scope=["b", "a", "a"],
            protected_scope=["z"],
            invariants=["i2", "i1"],
            required_evidence=["E2", "E1"],
            stop_conditions=["s"],
            authority_sources=["u"],
        )
        a = self.engine.compile(**args)
        b = self.engine.compile(**args)
        self.assertEqual(a.canonical_json(), b.canonical_json())
        self.assertEqual(a.fingerprint(), b.fingerprint())


class CounterfactualGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = CounterfactualAdoptionGate()

    def test_safe_proposal_passes(self) -> None:
        d = self.engine.evaluate(
            proposal_id="P1",
            benefit_score=90,
            scenarios=[Scenario("provider outage", 500, 50, True, True, 80)],
            mandatory_invariants_preserved=True,
            rollback_defined=True,
            evidence_plan_defined=True,
        )
        self.assertEqual(d.verdict, Verdict.PASS)

    def test_missing_rollback_freezes(self) -> None:
        d = self.engine.evaluate(
            proposal_id="P2",
            benefit_score=100,
            scenarios=[Scenario("x", 100, 10, True, True, 100)],
            mandatory_invariants_preserved=True,
            rollback_defined=False,
            evidence_plan_defined=True,
        )
        self.assertEqual(d.verdict, Verdict.FREEZE)

    def test_undetectable_irreversible_risk_freezes(self) -> None:
        d = self.engine.evaluate(
            proposal_id="P3",
            benefit_score=100,
            scenarios=[Scenario("silent corruption", 8000, 100, False, False, 0)],
            mandatory_invariants_preserved=True,
            rollback_defined=True,
            evidence_plan_defined=True,
            max_residual_risk=35,
        )
        self.assertEqual(d.verdict, Verdict.FREEZE)
        self.assertGreater(d.payload["worst_residual_risk"], 35)

    def test_scenario_order_does_not_change_fingerprint(self) -> None:
        s1 = Scenario("b", 100, 20, True, True, 50)
        s2 = Scenario("a", 100, 20, True, True, 50)
        kw = dict(
            proposal_id="P4", benefit_score=80, mandatory_invariants_preserved=True,
            rollback_defined=True, evidence_plan_defined=True
        )
        a = self.engine.evaluate(scenarios=[s1, s2], **kw)
        b = self.engine.evaluate(scenarios=[s2, s1], **kw)
        self.assertEqual(a.fingerprint(), b.fingerprint())


class CognitiveDebtTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = CognitiveDebtLedger()

    def test_empty_ledger_passes(self) -> None:
        d = self.engine.assess([])
        self.assertEqual(d.verdict, Verdict.PASS)
        self.assertEqual(d.payload["total_debt"], 0)

    def test_release_blocker_freezes(self) -> None:
        d = self.engine.assess([
            DebtItem("D1", DebtKind.UNVERIFIED_COMPLETION, 10, 0, True)
        ])
        self.assertEqual(d.verdict, Verdict.FREEZE)

    def test_age_amplifies_debt(self) -> None:
        young = self.engine.assess([DebtItem("D", DebtKind.STALE_EVIDENCE, 50, 0)])
        old = self.engine.assess([DebtItem("D", DebtKind.STALE_EVIDENCE, 50, 40)])
        self.assertGreater(old.payload["total_debt"], young.payload["total_debt"])

    def test_threshold_review(self) -> None:
        d = self.engine.assess(
            [DebtItem("D", DebtKind.CONTRADICTION, 100, 0)],
            review_threshold=40,
            freeze_threshold=100,
        )
        self.assertEqual(d.verdict, Verdict.REVIEW)


class ProofHorizonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ProofHorizonScheduler()

    def test_fresh_unchanged_proofs_pass(self) -> None:
        d = self.engine.schedule([
            ProofNode("unit", ("src:core",), "E2", 10, 1),
            ProofNode("e2e", ("proof:unit",), "E4", 10, 1),
        ])
        self.assertEqual(d.verdict, Verdict.PASS)
        self.assertEqual(d.payload["invalid_proof_count"], 0)

    def test_changed_source_invalidates_transitively(self) -> None:
        d = self.engine.schedule([
            ProofNode("unit", ("src:core",), "E2", 10, 1),
            ProofNode("e2e", ("proof:unit",), "E4", 10, 1),
        ], changed_dependencies=["src:core"])
        self.assertEqual(d.verdict, Verdict.FREEZE)
        self.assertEqual(d.payload["invalid_proof_count"], 2)

    def test_stale_low_class_requires_review(self) -> None:
        d = self.engine.schedule([
            ProofNode("static", ("src:x",), "E1", 5, 6),
        ])
        self.assertEqual(d.verdict, Verdict.REVIEW)

    def test_missing_upstream_proof_is_invalid(self) -> None:
        d = self.engine.schedule([
            ProofNode("integration", ("proof:missing",), "E3", 10, 0),
        ])
        self.assertEqual(d.verdict, Verdict.REVIEW)
        plan = d.payload["revalidation_plan"]
        self.assertIn("missing:proof:missing", plan[0][2])

    def test_duplicate_proof_ids_rejected_even_from_generator(self) -> None:
        proofs = (p for p in [
            ProofNode("dup", ("src:a",), "E1", 10, 0),
            ProofNode("dup", ("src:b",), "E2", 10, 0),
        ])
        with self.assertRaises(ValueError):
            self.engine.schedule(proofs)


class TrustBudgetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = HumanTrustBudgetGovernor()

    def test_low_risk_executes(self) -> None:
        d = self.engine.govern(TrustContext(5, 5, 10, 95, 50, 95))
        self.assertEqual(d.verdict, Verdict.PASS)
        self.assertEqual(d.payload["action_mode"], "EXECUTE")

    def test_unclear_scope_freezes(self) -> None:
        d = self.engine.govern(TrustContext(20, 10, 20, 80, 50, 20))
        self.assertEqual(d.verdict, Verdict.FREEZE)

    def test_irreversible_requires_at_least_confirmation(self) -> None:
        d = self.engine.govern(TrustContext(5, 70, 30, 95, 50, 95))
        self.assertIn(d.payload["action_mode"], {"REQUIRE_CONFIRMATION", "FREEZE"})

    def test_high_impact_weak_evidence_freezes(self) -> None:
        d = self.engine.govern(TrustContext(40, 40, 90, 20, 20, 90))
        self.assertEqual(d.verdict, Verdict.FREEZE)


class SuiteTests(unittest.TestCase):
    def test_freeze_dominates_pass(self) -> None:
        intent = IntentLatticeCompiler().compile(
            objective="x", authorized_scope=["a"], protected_scope=["b"],
            invariants=[], required_evidence=["E1"], stop_conditions=["s"], authority_sources=["u"]
        )
        trust = HumanTrustBudgetGovernor().govern(TrustContext(80, 90, 90, 10, 10, 20))
        out = AssuranceSuite().combine([intent, trust])
        self.assertEqual(out.verdict, Verdict.FREEZE)

    def test_suite_is_order_invariant(self) -> None:
        a = IntentLatticeCompiler().compile(
            objective="x", authorized_scope=["a"], protected_scope=["b"],
            invariants=[], required_evidence=["E1"], stop_conditions=["s"], authority_sources=["u"]
        )
        b = CognitiveDebtLedger().assess([])
        s = AssuranceSuite()
        self.assertEqual(s.combine([a, b]), s.combine([b, a]))


if __name__ == "__main__":
    unittest.main()
