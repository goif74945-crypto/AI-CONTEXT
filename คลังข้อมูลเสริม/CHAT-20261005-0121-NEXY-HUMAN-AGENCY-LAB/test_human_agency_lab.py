
# ===== test_budget.py =====
import unittest

from human_agency_lab import (
    AgencyDecisionEngine,
    AttentionBudget,
    Decision,
    RequestProfile,
    apply_attention_budget,
    batch_interruptions,
)


class AttentionBudgetTests(unittest.TestCase):
    def test_preview_consumes_budget(self):
        engine = AgencyDecisionEngine()
        decision = engine.evaluate(RequestProfile(action_id="wide", scope_breadth=0.8))
        budget = AttentionBudget(capacity=5)
        effective = apply_attention_budget(decision, budget)
        self.assertEqual(effective.decision, Decision.PREVIEW)
        self.assertGreater(budget.consumed, 0)

    def test_soft_preview_can_yield_when_budget_exhausted(self):
        engine = AgencyDecisionEngine()
        decision = engine.evaluate(RequestProfile(action_id="wide", scope_breadth=0.8))
        budget = AttentionBudget(capacity=0)
        effective = apply_attention_budget(decision, budget)
        self.assertEqual(effective.decision, Decision.PROCEED)
        self.assertFalse(effective.hard_gate)

    def test_hard_confirm_never_downgrades(self):
        engine = AgencyDecisionEngine()
        decision = engine.evaluate(
            RequestProfile(action_id="purchase", external_side_effect=True, monetary_cost=0.9)
        )
        budget = AttentionBudget(capacity=0)
        effective = apply_attention_budget(decision, budget)
        self.assertEqual(effective.decision, Decision.CONFIRM)
        self.assertTrue(effective.hard_gate)

    def test_batch_interruptions_filters_proceed(self):
        engine = AgencyDecisionEngine()
        decisions = [
            engine.evaluate(RequestProfile(action_id="a")),
            engine.evaluate(RequestProfile(action_id="b", ambiguity=0.4)),
        ]
        visible = batch_interruptions(decisions)
        self.assertEqual([d.action_id for d in visible], ["b"])

    def test_invalid_budget_rejected(self):
        with self.assertRaises(ValueError):
            AttentionBudget(capacity=-1)


if __name__ == "__main__":
    unittest.main()


# ===== test_engine.py =====
import unittest

from human_agency_lab import AgencyDecisionEngine, Decision, RequestProfile


class AgencyDecisionEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = AgencyDecisionEngine()

    def test_low_risk_proceeds(self):
        result = self.engine.evaluate(RequestProfile(action_id="read"))
        self.assertEqual(result.decision, Decision.PROCEED)
        self.assertFalse(result.hard_gate)

    def test_destructive_without_rollback_freezes(self):
        result = self.engine.evaluate(
            RequestProfile(
                action_id="delete",
                destructive=True,
                rollback_available=False,
                reversibility=0.0,
            )
        )
        self.assertEqual(result.decision, Decision.FREEZE)
        self.assertTrue(result.hard_gate)

    def test_destructive_with_rollback_confirms(self):
        result = self.engine.evaluate(
            RequestProfile(
                action_id="delete-temp",
                destructive=True,
                rollback_available=True,
                reversibility=0.9,
            )
        )
        self.assertEqual(result.decision, Decision.CONFIRM)

    def test_missing_authority_on_high_impact_freezes(self):
        result = self.engine.evaluate(
            RequestProfile(
                action_id="wide",
                scope_breadth=0.9,
                explicit_user_authority=False,
            )
        )
        self.assertEqual(result.decision, Decision.FREEZE)

    def test_sensitive_external_effect_confirms(self):
        result = self.engine.evaluate(
            RequestProfile(
                action_id="share",
                external_side_effect=True,
                data_sensitivity=0.9,
            )
        )
        self.assertEqual(result.decision, Decision.CONFIRM)

    def test_broad_scope_previews(self):
        result = self.engine.evaluate(
            RequestProfile(action_id="bulk", scope_breadth=0.8)
        )
        self.assertEqual(result.decision, Decision.PREVIEW)

    def test_same_input_same_output_and_digest(self):
        req = RequestProfile(
            action_id="stable",
            ambiguity=0.4,
            confidence=0.8,
            scope_breadth=0.2,
        )
        a = self.engine.evaluate(req)
        b = self.engine.evaluate(req)
        self.assertEqual(a, b)
        self.assertEqual(a.digest(), b.digest())

    def test_auth_boundary_confirms(self):
        result = self.engine.evaluate(
            RequestProfile(action_id="auth", crosses_auth_boundary=True)
        )
        self.assertEqual(result.decision, Decision.CONFIRM)

    def test_high_ambiguity_external_irreversible_freezes(self):
        result = self.engine.evaluate(
            RequestProfile(
                action_id="unclear-send",
                ambiguity=0.95,
                external_side_effect=True,
                reversibility=0.1,
            )
        )
        self.assertEqual(result.decision, Decision.FREEZE)


if __name__ == "__main__":
    unittest.main()


# ===== test_invariants.py =====
import itertools
import unittest

from human_agency_lab import (
    AgencyDecisionEngine,
    AttentionBudget,
    Decision,
    RequestProfile,
    apply_attention_budget,
)


RANK = {
    Decision.PROCEED: 0,
    Decision.PREVIEW: 1,
    Decision.CONFIRM: 2,
    Decision.FREEZE: 3,
}


class InvariantGridTests(unittest.TestCase):
    def setUp(self):
        self.engine = AgencyDecisionEngine()

    def test_high_impact_without_authority_always_freezes_over_grid(self):
        for scope, sensitivity, cost in itertools.product(
            [0.0, 0.6, 1.0], [0.0, 0.65, 1.0], [0.0, 0.5, 1.0]
        ):
            if scope < 0.6 and sensitivity < 0.65 and cost < 0.5:
                continue
            with self.subTest(scope=scope, sensitivity=sensitivity, cost=cost):
                result = self.engine.evaluate(
                    RequestProfile(
                        action_id=f"grid-{scope}-{sensitivity}-{cost}",
                        scope_breadth=scope,
                        data_sensitivity=sensitivity,
                        monetary_cost=cost,
                        explicit_user_authority=False,
                    )
                )
                self.assertEqual(result.decision, Decision.FREEZE)
                self.assertTrue(result.hard_gate)

    def test_destructive_without_rollback_always_freezes_over_grid(self):
        for ambiguity, confidence, scope in itertools.product(
            [0.0, 0.5, 1.0], [0.0, 0.5, 1.0], [0.0, 0.5, 1.0]
        ):
            with self.subTest(ambiguity=ambiguity, confidence=confidence, scope=scope):
                result = self.engine.evaluate(
                    RequestProfile(
                        action_id="destructive-grid",
                        ambiguity=ambiguity,
                        confidence=confidence,
                        scope_breadth=scope,
                        destructive=True,
                        rollback_available=False,
                        reversibility=0.0,
                    )
                )
                self.assertEqual(result.decision, Decision.FREEZE)

    def test_attention_budget_never_weakens_hard_gate_over_grid(self):
        hard_requests = [
            RequestProfile(action_id="auth", crosses_auth_boundary=True),
            RequestProfile(
                action_id="money", external_side_effect=True, monetary_cost=1.0
            ),
            RequestProfile(
                action_id="secret", external_side_effect=True, data_sensitivity=1.0
            ),
            RequestProfile(
                action_id="delete",
                destructive=True,
                rollback_available=False,
                reversibility=0.0,
            ),
        ]
        for capacity in [0, 1, 2, 3, 100]:
            for request in hard_requests:
                original = self.engine.evaluate(request)
                effective = apply_attention_budget(original, AttentionBudget(capacity=capacity))
                with self.subTest(capacity=capacity, action=request.action_id):
                    self.assertEqual(effective.decision, original.decision)
                    self.assertEqual(effective.hard_gate, original.hard_gate)

    def test_external_ambiguity_is_monotonic_non_decreasing(self):
        decisions = []
        for ambiguity in [0.0, 0.29, 0.30, 0.59, 0.60, 0.89, 0.90, 1.0]:
            result = self.engine.evaluate(
                RequestProfile(
                    action_id=f"ambiguity-{ambiguity}",
                    ambiguity=ambiguity,
                    external_side_effect=True,
                    reversibility=1.0,
                )
            )
            decisions.append(RANK[result.decision])
        self.assertEqual(decisions, sorted(decisions))

    def test_digest_repeatability_500_iterations(self):
        request = RequestProfile(
            action_id="repeatable",
            ambiguity=0.42,
            confidence=0.77,
            scope_breadth=0.21,
            external_side_effect=False,
        )
        digests = {self.engine.evaluate(request).digest() for _ in range(500)}
        self.assertEqual(len(digests), 1)


if __name__ == "__main__":
    unittest.main()


# ===== test_metrics.py =====
import unittest

from human_agency_lab import AgencyDecisionEngine, RequestProfile, summarize


class MetricsTests(unittest.TestCase):
    def test_summary_is_exact_for_known_corpus(self):
        engine = AgencyDecisionEngine()
        decisions = [
            engine.evaluate(RequestProfile(action_id="a")),
            engine.evaluate(RequestProfile(action_id="b", ambiguity=0.4)),
            engine.evaluate(
                RequestProfile(action_id="c", external_side_effect=True, monetary_cost=0.9)
            ),
        ]
        metrics = summarize(decisions)
        self.assertEqual(metrics.total, 3)
        self.assertEqual(metrics.human_interruptions, 2)
        self.assertEqual(metrics.hard_gates, 1)
        self.assertAlmostEqual(metrics.autonomy_rate, 1 / 3)

    def test_empty_summary(self):
        metrics = summarize([])
        self.assertEqual(metrics.total, 0)
        self.assertEqual(metrics.autonomy_rate, 1.0)


if __name__ == "__main__":
    unittest.main()


# ===== test_models.py =====
import unittest

from human_agency_lab import RequestProfile


class RequestProfileTests(unittest.TestCase):
    def test_empty_action_rejected(self):
        with self.assertRaises(ValueError):
            RequestProfile(action_id=" ")

    def test_unit_interval_fields_validated(self):
        with self.assertRaises(ValueError):
            RequestProfile(action_id="x", ambiguity=1.1)

    def test_negative_attention_cost_rejected(self):
        with self.assertRaises(ValueError):
            RequestProfile(action_id="x", user_attention_cost=-1)


if __name__ == "__main__":
    unittest.main()


# ===== test_policy.py =====
import unittest

from human_agency_lab import AgencyPolicy


class AgencyPolicyTests(unittest.TestCase):
    def test_valid_json_policy(self):
        policy = AgencyPolicy.from_json('{"confirm_ambiguity": 0.7}')
        self.assertEqual(policy.confirm_ambiguity, 0.7)

    def test_unknown_key_rejected(self):
        with self.assertRaises(ValueError):
            AgencyPolicy.from_json('{"mystery": 1}')

    def test_invalid_threshold_order_rejected(self):
        with self.assertRaises(ValueError):
            AgencyPolicy(preview_ambiguity=0.8, confirm_ambiguity=0.5)

    def test_out_of_range_threshold_rejected(self):
        with self.assertRaises(ValueError):
            AgencyPolicy(material_cost=2.0)


if __name__ == "__main__":
    unittest.main()


# ===== test_recovery.py =====
import unittest

from human_agency_lab import RecoveryLevel, RequestProfile, plan_recovery, recovery_coverage


class RecoveryTests(unittest.TestCase):
    def test_destructive_without_rollback_blocked(self):
        plan = plan_recovery(
            RequestProfile(
                action_id="delete", destructive=True, rollback_available=False, reversibility=0.0
            )
        )
        self.assertEqual(plan.level, RecoveryLevel.BLOCKED)

    def test_external_effect_gets_checkpoint(self):
        plan = plan_recovery(
            RequestProfile(action_id="send", external_side_effect=True)
        )
        self.assertEqual(plan.level, RecoveryLevel.CHECKPOINT)

    def test_low_risk_needs_no_recovery(self):
        plan = plan_recovery(RequestProfile(action_id="read"))
        self.assertEqual(plan.level, RecoveryLevel.NONE_REQUIRED)

    def test_coverage(self):
        plans = [
            plan_recovery(RequestProfile(action_id="a")),
            plan_recovery(
                RequestProfile(
                    action_id="b", destructive=True, rollback_available=False, reversibility=0.0
                )
            ),
        ]
        self.assertEqual(recovery_coverage(plans), 0.5)


if __name__ == "__main__":
    unittest.main()


# ===== test_simulator.py =====
import pathlib
import unittest

from human_agency_lab import load_scenarios, run_scenarios


ROOT = pathlib.Path(__file__).resolve().parent


class SimulatorTests(unittest.TestCase):
    def test_reference_scenarios_all_pass(self):
        scenarios = load_scenarios(ROOT / "fixtures" / "scenarios.json")
        results = run_scenarios(scenarios)
        failures = [r.name for r in results if not r.passed]
        self.assertEqual(failures, [])
        self.assertGreaterEqual(len(results), 10)

    def test_non_array_scenarios_rejected(self):
        path = ROOT / "fixtures" / "bad-scenarios.json"
        path.write_text('{"x": 1}', encoding="utf-8")
        try:
            with self.assertRaises(ValueError):
                load_scenarios(path)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
