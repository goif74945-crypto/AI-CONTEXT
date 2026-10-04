import unittest

from counterfactual_minimizer import (
    CounterfactualCapabilities,
    InterventionKind,
    minimize_gate,
)
from human_agency_lab import AgencyPolicy, Decision, RequestProfile


class CounterfactualMinimizerTests(unittest.TestCase):
    def test_noop_when_already_at_or_below_target(self):
        request = RequestProfile(action_id="read")
        plan = minimize_gate(
            request,
            target=Decision.PREVIEW,
            capabilities=CounterfactualCapabilities(),
        )
        self.assertIsNotNone(plan)
        self.assertEqual(plan.interventions, tuple())
        self.assertEqual(plan.achieved_decision, Decision.PROCEED)

    def test_low_confidence_preview_can_be_removed_by_evidence_improvement(self):
        request = RequestProfile(action_id="analyze", confidence=0.4)
        plan = minimize_gate(
            request,
            target=Decision.PROCEED,
            capabilities=CounterfactualCapabilities(can_improve_confidence=True),
        )
        self.assertIsNotNone(plan)
        self.assertEqual(plan.interventions, (InterventionKind.IMPROVE_CONFIDENCE,))
        self.assertEqual(plan.achieved_decision, Decision.PROCEED)

    def test_ambiguity_preview_can_be_removed_by_resolution(self):
        request = RequestProfile(action_id="rename", ambiguity=0.4)
        plan = minimize_gate(
            request,
            target=Decision.PROCEED,
            capabilities=CounterfactualCapabilities(can_resolve_ambiguity=True),
        )
        self.assertIsNotNone(plan)
        self.assertEqual(plan.interventions, (InterventionKind.RESOLVE_AMBIGUITY,))

    def test_destructive_no_rollback_can_reach_confirm_by_building_rollback(self):
        request = RequestProfile(
            action_id="delete",
            destructive=True,
            rollback_available=False,
            reversibility=0.0,
        )
        plan = minimize_gate(
            request,
            target=Decision.CONFIRM,
            capabilities=CounterfactualCapabilities(can_build_rollback=True),
        )
        self.assertIsNotNone(plan)
        self.assertEqual(plan.interventions, (InterventionKind.ADD_ROLLBACK,))
        self.assertEqual(plan.achieved_decision, Decision.CONFIRM)

    def test_destructive_no_rollback_has_no_plan_without_material_capability(self):
        request = RequestProfile(
            action_id="delete",
            destructive=True,
            rollback_available=False,
            reversibility=0.0,
        )
        plan = minimize_gate(
            request,
            target=Decision.CONFIRM,
            capabilities=CounterfactualCapabilities(),
        )
        self.assertIsNone(plan)

    def test_reversible_alternative_can_reduce_destructive_gate(self):
        request = RequestProfile(
            action_id="delete",
            destructive=True,
            rollback_available=False,
            reversibility=0.0,
        )
        plan = minimize_gate(
            request,
            target=Decision.PROCEED,
            capabilities=CounterfactualCapabilities(
                can_use_reversible_alternative=True
            ),
        )
        self.assertIsNotNone(plan)
        self.assertFalse(plan.modified_request.destructive)
        self.assertTrue(plan.modified_request.rollback_available)

    def test_sensitive_external_confirm_can_be_reduced_by_redaction(self):
        request = RequestProfile(
            action_id="send",
            external_side_effect=True,
            data_sensitivity=0.9,
        )
        plan = minimize_gate(
            request,
            target=Decision.PREVIEW,
            capabilities=CounterfactualCapabilities(can_redact_data=True),
        )
        self.assertIsNotNone(plan)
        self.assertEqual(plan.interventions, (InterventionKind.REDACT_SENSITIVE_DATA,))
        self.assertLessEqual(plan.modified_request.data_sensitivity, 0.0)

    def test_material_cost_confirm_can_be_reduced_only_when_cost_can_be_removed(self):
        request = RequestProfile(
            action_id="purchase",
            external_side_effect=True,
            monetary_cost=0.9,
        )
        no_plan = minimize_gate(
            request,
            target=Decision.PREVIEW,
            capabilities=CounterfactualCapabilities(),
        )
        yes_plan = minimize_gate(
            request,
            target=Decision.PREVIEW,
            capabilities=CounterfactualCapabilities(can_remove_material_cost=True),
        )
        self.assertIsNone(no_plan)
        self.assertIsNotNone(yes_plan)
        self.assertEqual(yes_plan.interventions, (InterventionKind.REMOVE_MATERIAL_COST,))

    def test_scope_reduction_never_increases_scope(self):
        request = RequestProfile(
            action_id="wide",
            scope_breadth=0.9,
            explicit_user_authority=False,
        )
        plan = minimize_gate(
            request,
            target=Decision.PREVIEW,
            capabilities=CounterfactualCapabilities(can_reduce_scope=True),
        )
        self.assertIsNotNone(plan)
        self.assertLess(plan.modified_request.scope_breadth, request.scope_breadth)

    def test_external_isolation_changes_semantics_not_authority_flag(self):
        request = RequestProfile(
            action_id="send",
            external_side_effect=True,
            ambiguity=0.8,
        )
        plan = minimize_gate(
            request,
            target=Decision.PREVIEW,
            capabilities=CounterfactualCapabilities(can_isolate_external_effect=True),
        )
        self.assertIsNotNone(plan)
        self.assertFalse(plan.modified_request.external_side_effect)
        self.assertEqual(
            plan.modified_request.explicit_user_authority,
            request.explicit_user_authority,
        )

    def test_max_steps_limits_combination_search(self):
        request = RequestProfile(
            action_id="complex",
            ambiguity=0.4,
            confidence=0.4,
        )
        capabilities = CounterfactualCapabilities(
            can_resolve_ambiguity=True,
            can_improve_confidence=True,
        )
        blocked = minimize_gate(
            request,
            target=Decision.PROCEED,
            capabilities=capabilities,
            max_steps=1,
        )
        solved = minimize_gate(
            request,
            target=Decision.PROCEED,
            capabilities=capabilities,
            max_steps=2,
        )
        self.assertIsNone(blocked)
        self.assertIsNotNone(solved)
        self.assertEqual(len(solved.interventions), 2)

    def test_tie_break_is_deterministic(self):
        request = RequestProfile(action_id="preview", scope_breadth=0.9)
        capabilities = CounterfactualCapabilities(
            can_reduce_scope=True,
            can_resolve_ambiguity=True,
        )
        # Ambiguity intervention is a no-op; only semantic changes are candidates.
        plans = {
            minimize_gate(
                request,
                target=Decision.PROCEED,
                capabilities=capabilities,
            ).digest()
            for _ in range(500)
        }
        self.assertEqual(len(plans), 1)

    def test_custom_policy_boundary_is_respected(self):
        policy = AgencyPolicy(broad_scope=0.4, high_impact_scope=0.5)
        request = RequestProfile(action_id="wide", scope_breadth=0.8)
        plan = minimize_gate(
            request,
            target=Decision.PROCEED,
            capabilities=CounterfactualCapabilities(can_reduce_scope=True),
            policy=policy,
        )
        self.assertIsNotNone(plan)
        self.assertLess(plan.modified_request.scope_breadth, 0.4)

    def test_negative_max_steps_rejected(self):
        with self.assertRaises(ValueError):
            minimize_gate(
                RequestProfile(action_id="read"),
                target=Decision.PROCEED,
                capabilities=CounterfactualCapabilities(),
                max_steps=-1,
            )


if __name__ == "__main__":
    unittest.main()
