import unittest

from qcp.fixed import Q64
from qcp.uncertainty import UncertaintyStage, UncertaintyMassCompiler
from qcp.robustness import LinearFeature, DecisionRobustnessEngine
from qcp.budget import BudgetState, Reservation, VectorBudgetReactor
from qcp.reversibility import ReversibilityPolicy, ReversibilityHalfLifeScheduler
from qcp.expectation import Consequence, ExpectationDivergenceBarrier
from qcp.pipeline import ConstitutionalPhysicsPipeline

q = Q64.from_decimal


class UncertaintyMassCompilerTests(unittest.TestCase):
    def test_conservation_passes_with_evidence_receipt(self):
        stages = [
            UncertaintyStage("normalize", q("0.60"), q("0.10"), q("0.20"), q("0.50"), ("E-1",)),
            UncertaintyStage("verify", q("0.50"), q("0.00"), q("0.30"), q("0.20"), ("E-2",)),
        ]
        d = UncertaintyMassCompiler().compile(stages)
        self.assertEqual(d.status, "PASS")
        self.assertEqual(d.final_mass, q("0.20"))

    def test_laundered_uncertainty_freezes(self):
        stages = [UncertaintyStage("bad", q("0.80"), q("0.00"), q("0.10"), q("0.10"), ("E",))]
        d = UncertaintyMassCompiler().compile(stages)
        self.assertEqual(d.status, "FREEZE")
        self.assertEqual(d.reason, "MASS_NOT_CONSERVED")

    def test_resolution_without_evidence_freezes(self):
        stages = [UncertaintyStage("bad", q("0.40"), q("0.00"), q("0.10"), q("0.30"), ())]
        d = UncertaintyMassCompiler().compile(stages)
        self.assertEqual(d.reason, "UNSUPPORTED_RESOLUTION")

    def test_stage_chain_mismatch_freezes(self):
        stages = [
            UncertaintyStage("a", q("0.40"), q("0"), q("0.10"), q("0.30"), ("E",)),
            UncertaintyStage("b", q("0.29"), q("0"), q("0"), q("0.29"), ()),
        ]
        self.assertEqual(UncertaintyMassCompiler().compile(stages).reason, "CHAIN_MISMATCH")


class DecisionRobustnessEngineTests(unittest.TestCase):
    def test_allow_certificate_when_entire_box_above_threshold(self):
        features = [
            LinearFeature("evidence", q("0.8"), q("1.0"), q("0.05")),
            LinearFeature("risk", q("-0.5"), q("0.2"), q("0.02")),
        ]
        d = DecisionRobustnessEngine().certify(features, bias=q("0.2"), threshold=q("0.7"))
        self.assertEqual(d.status, "CERTIFY_ALLOW")
        self.assertGreater(d.robust_margin, Q64.zero())

    def test_boundary_crossing_freezes(self):
        features = [LinearFeature("x", q("1.0"), q("0.5"), q("0.2"))]
        d = DecisionRobustnessEngine().certify(features, bias=q("0"), threshold=q("0.5"))
        self.assertEqual(d.status, "FREEZE")
        self.assertEqual(d.reason, "PERTURBATION_CAN_FLIP_DECISION")

    def test_deny_certificate_when_entire_box_below_threshold(self):
        features = [LinearFeature("x", q("1"), q("0.2"), q("0.05"))]
        d = DecisionRobustnessEngine().certify(features, bias=q("0"), threshold=q("0.5"))
        self.assertEqual(d.status, "CERTIFY_DENY")

    def test_negative_radius_rejected(self):
        with self.assertRaises(ValueError):
            LinearFeature("x", q("1"), q("0"), q("-0.1"))


class VectorBudgetReactorTests(unittest.TestCase):
    def setUp(self):
        self.engine = VectorBudgetReactor()
        self.state = BudgetState.create({
            "privacy": q("1.0"),
            "irreversibility": q("0.8"),
            "compute": q("10"),
        })

    def test_reserve_commit_release_flow(self):
        r = Reservation.create("R1", {"privacy": q("0.2"), "compute": q("3")})
        s1, d1 = self.engine.reserve(self.state, r)
        self.assertEqual(d1.status, "PASS")
        s2, d2 = self.engine.commit(s1, "R1")
        self.assertEqual(d2.status, "PASS")
        self.assertEqual(s2.used["privacy"], q("0.2"))
        self.assertNotIn("R1", s2.reservations)

    def test_non_fungible_dimension_cannot_borrow_from_other(self):
        r = Reservation.create("R2", {"privacy": q("1.1"), "compute": q("1")})
        _, d = self.engine.reserve(self.state, r)
        self.assertEqual(d.status, "FREEZE")
        self.assertEqual(d.reason, "DIMENSION_CAP_EXCEEDED")
        self.assertEqual(d.bottleneck, "privacy")

    def test_duplicate_reservation_id_freezes(self):
        r = Reservation.create("R", {"compute": q("1")})
        s1, _ = self.engine.reserve(self.state, r)
        _, d = self.engine.reserve(s1, r)
        self.assertEqual(d.reason, "DUPLICATE_RESERVATION")

    def test_unknown_dimension_freezes(self):
        r = Reservation.create("R3", {"money": q("1")})
        _, d = self.engine.reserve(self.state, r)
        self.assertEqual(d.reason, "UNKNOWN_DIMENSION")


class ReversibilityHalfLifeSchedulerTests(unittest.TestCase):
    def test_scheduler_finds_latest_safe_tick(self):
        p = ReversibilityPolicy(
            initial_reversibility=q("1.0"),
            retention_per_tick=q("0.9"),
            minimum_reversibility=q("0.6"),
            hard_deadline_tick=10,
        )
        d = ReversibilityHalfLifeScheduler().assess(p, current_tick=2)
        self.assertEqual(d.status, "PASS")
        self.assertGreaterEqual(d.latest_safe_tick, 4)
        self.assertLessEqual(d.latest_safe_tick, 5)

    def test_expired_window_freezes(self):
        p = ReversibilityPolicy(q("1"), q("0.5"), q("0.6"), 10)
        d = ReversibilityHalfLifeScheduler().assess(p, current_tick=2)
        self.assertEqual(d.status, "FREEZE")
        self.assertEqual(d.reason, "REVERSIBILITY_BELOW_FLOOR")

    def test_invalid_retention_rejected(self):
        with self.assertRaises(ValueError):
            ReversibilityPolicy(q("1"), q("1.1"), q("0.5"), 10)

    def test_checkpoint_required_near_safe_edge(self):
        p = ReversibilityPolicy(q("1"), q("0.8"), q("0.5"), 10)
        d = ReversibilityHalfLifeScheduler().assess(p, current_tick=2, checkpoint_guard_ticks=1)
        self.assertEqual(d.status, "CHECKPOINT_REQUIRED")


class ExpectationDivergenceBarrierTests(unittest.TestCase):
    def test_matching_preview_passes(self):
        preview = [Consequence("data_delete", q("0.2"), q("1"))]
        actual = [Consequence("data_delete", q("0.2"), q("1"))]
        d = ExpectationDivergenceBarrier().compare(preview, actual, tolerance=q("0.01"))
        self.assertEqual(d.status, "PASS")
        self.assertEqual(d.divergence, Q64.zero())

    def test_large_surprise_freezes(self):
        preview = [Consequence("data_delete", q("0.1"), q("1"))]
        actual = [Consequence("data_delete", q("0.8"), q("1"))]
        d = ExpectationDivergenceBarrier().compare(preview, actual, tolerance=q("0.2"))
        self.assertEqual(d.status, "FREEZE")
        self.assertEqual(d.reason, "PREVIEW_DIVERGENCE")

    def test_undeclared_actual_dimension_freezes(self):
        preview = [Consequence("email", q("0.1"), q("1"))]
        actual = [Consequence("email", q("0.1"), q("1")), Consequence("billing", q("0.1"), q("1"))]
        d = ExpectationDivergenceBarrier().compare(preview, actual, tolerance=q("1"))
        self.assertEqual(d.reason, "UNDECLARED_CONSEQUENCE")

    def test_weight_zero_rejected(self):
        with self.assertRaises(ValueError):
            Consequence("x", q("0.1"), q("0"))


class PipelineIntegrationTests(unittest.TestCase):
    def test_low_surprise_robust_budgeted_reversible_flow_passes(self):
        pipeline = ConstitutionalPhysicsPipeline()
        d = pipeline.evaluate_demo_case()
        self.assertEqual(d.status, "PASS")
        self.assertEqual(d.engine_statuses, (
            ("UMC", "PASS"),
            ("DRC", "CERTIFY_ALLOW"),
            ("VBR", "PASS"),
            ("RHL", "PASS"),
            ("EDB", "PASS"),
        ))

    def test_freeze_dominates_pipeline(self):
        pipeline = ConstitutionalPhysicsPipeline()
        d = pipeline.evaluate_demo_case(force_preview_divergence=True)
        self.assertEqual(d.status, "FREEZE")
        self.assertIn(("EDB", "FREEZE"), d.engine_statuses)


if __name__ == "__main__":
    unittest.main()

class AdversarialBoundaryTests(unittest.TestCase):
    def test_umc_accepts_one_raw_ulp_quantization_residual_only(self):
        base = Q64.from_raw(100)
        one = Q64.from_raw(1)
        two = Q64.from_raw(2)
        ok = UncertaintyMassCompiler().compile([
            UncertaintyStage("ulp1", base, Q64.zero(), Q64.zero(), base + one, ())
        ])
        bad = UncertaintyMassCompiler().compile([
            UncertaintyStage("ulp2", base, Q64.zero(), Q64.zero(), base + two, ())
        ])
        self.assertEqual(ok.status, "PASS")
        self.assertEqual(bad.reason, "MASS_NOT_CONSERVED")

    def test_drc_is_feature_order_invariant(self):
        features = [
            LinearFeature("b", q("-0.3"), q("0.4"), q("0.02")),
            LinearFeature("a", q("0.9"), q("0.8"), q("0.03")),
        ]
        engine = DecisionRobustnessEngine()
        a = engine.certify(features, bias=q("0.2"), threshold=q("0.5"))
        b = engine.certify(list(reversed(features)), bias=q("0.2"), threshold=q("0.5"))
        self.assertEqual(a, b)

    def test_vbr_release_returns_reserved_capacity_without_spending(self):
        engine = VectorBudgetReactor()
        state = BudgetState.create({"privacy": q("1")})
        state, _ = engine.reserve(state, Reservation.create("r", {"privacy": q("0.8")}))
        state, decision = engine.release(state, "r")
        self.assertEqual(decision.status, "PASS")
        self.assertEqual(state.used["privacy"], Q64.zero())
        state, decision = engine.reserve(state, Reservation.create("r2", {"privacy": q("1")}))
        self.assertEqual(decision.status, "PASS")

    def test_rhl_hard_deadline_expiry_dominates(self):
        p = ReversibilityPolicy(q("1"), q("1"), q("0.5"), 2)
        d = ReversibilityHalfLifeScheduler().assess(p, current_tick=3)
        self.assertEqual(d.reason, "HARD_DEADLINE_EXPIRED")

    def test_edb_missing_execution_consequence_freezes(self):
        preview = [Consequence("billing", q("0.2"), q("1"))]
        d = ExpectationDivergenceBarrier().compare(preview, [], tolerance=q("1"))
        self.assertEqual(d.reason, "MISSING_EXECUTION_CONSEQUENCE")

    def test_edb_importance_model_change_freezes(self):
        preview = [Consequence("billing", q("0.2"), q("1"))]
        actual = [Consequence("billing", q("0.2"), q("0.9"))]
        d = ExpectationDivergenceBarrier().compare(preview, actual, tolerance=q("1"))
        self.assertEqual(d.reason, "IMPORTANCE_MODEL_CHANGED")
