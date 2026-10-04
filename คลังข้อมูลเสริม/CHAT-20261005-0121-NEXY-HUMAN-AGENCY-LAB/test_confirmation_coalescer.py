from __future__ import annotations

from dataclasses import replace
from itertools import permutations, product
import unittest

from confirmation_coalescer import (
    CoalescingPolicy,
    InteractionCandidate,
    coalesce_interactions,
)
from human_agency_lab import AgencyDecisionEngine, Decision, RequestProfile


ENGINE = AgencyDecisionEngine()


def candidate(
    action_id: str,
    *,
    authority: str = "authority-A",
    decision_policy: str = "decision-policy-A",
    context: str = "workspace-A",
    **request_values: object,
) -> InteractionCandidate:
    request = RequestProfile(action_id=action_id, **request_values)
    return InteractionCandidate(
        request=request,
        decision=ENGINE.evaluate(request),
        authority_digest=authority,
        decision_policy_digest=decision_policy,
        interaction_context=context,
    )


class CoalescingPolicyTests(unittest.TestCase):
    def test_invalid_limits_rejected(self) -> None:
        with self.assertRaises(ValueError):
            CoalescingPolicy(max_actions=0)
        with self.assertRaises(ValueError):
            CoalescingPolicy(max_attention_cost=-1)
        with self.assertRaises(ValueError):
            CoalescingPolicy(sensitive_data_threshold=1.01)

    def test_digest_repeatability_and_policy_sensitivity(self) -> None:
        first = CoalescingPolicy()
        self.assertEqual(first.digest(), CoalescingPolicy().digest())
        self.assertNotEqual(first.digest(), CoalescingPolicy(max_actions=4).digest())


class CoalescingPlanTests(unittest.TestCase):
    def test_compatible_previews_coalesce_with_action_mapping(self) -> None:
        items = [
            candidate("a", ambiguity=0.4),
            candidate("b", confidence=0.5),
            candidate("c", scope_breadth=0.8),
        ]
        plan = coalesce_interactions(items)
        self.assertEqual(plan.metrics.interruptions_before, 3)
        self.assertEqual(plan.metrics.interruptions_after, 1)
        self.assertEqual(plan.metrics.interruptions_avoided, 2)
        self.assertEqual(plan.batches[0].action_ids, ("a", "b", "c"))
        self.assertEqual(
            tuple(item.action_id for item in plan.batches[0].explanations),
            ("a", "b", "c"),
        )

    def test_proceed_actions_do_not_create_interruptions(self) -> None:
        plan = coalesce_interactions([candidate("a"), candidate("b")])
        self.assertEqual(plan.proceed_action_ids, ("a", "b"))
        self.assertEqual(plan.batches, tuple())
        self.assertEqual(plan.metrics.interruptions_before, 0)
        self.assertEqual(plan.metrics.reduction_ratio, 0.0)

    def test_authority_policy_and_context_boundaries_do_not_merge(self) -> None:
        items = [
            candidate("a", ambiguity=0.4),
            candidate("b", ambiguity=0.4, authority="authority-B"),
            candidate("c", ambiguity=0.4, decision_policy="decision-policy-B"),
            candidate("d", ambiguity=0.4, context="workspace-B"),
        ]
        plan = coalesce_interactions(items)
        self.assertEqual(len(plan.batches), 4)

    def test_decision_classes_do_not_merge(self) -> None:
        preview = candidate("preview", ambiguity=0.4)
        confirm = candidate(
            "confirm",
            external_side_effect=True,
            data_sensitivity=0.8,
        )
        plan = coalesce_interactions([preview, confirm])
        self.assertEqual(len(plan.batches), 2)
        self.assertEqual(
            {batch.decision for batch in plan.batches},
            {Decision.PREVIEW, Decision.CONFIRM},
        )

    def test_max_action_and_attention_limits_split_batches(self) -> None:
        items = [candidate(str(index), ambiguity=0.4) for index in range(5)]
        by_count = coalesce_interactions(items, CoalescingPolicy(max_actions=2))
        self.assertEqual([len(batch.action_ids) for batch in by_count.batches], [2, 2, 1])
        by_cost = coalesce_interactions(
            items,
            CoalescingPolicy(max_actions=10, max_attention_cost=2),
        )
        self.assertEqual([batch.total_attention_cost for batch in by_cost.batches], [2, 2, 1])

    def test_duplicate_action_rejected(self) -> None:
        item = candidate("same", ambiguity=0.4)
        with self.assertRaises(ValueError):
            coalesce_interactions([item, item])

    def test_mismatched_request_decision_rejected(self) -> None:
        request = RequestProfile(action_id="request", ambiguity=0.4)
        other = ENGINE.evaluate(RequestProfile(action_id="other", ambiguity=0.4))
        with self.assertRaises(ValueError):
            InteractionCandidate(request, other, "a", "p", "c")

    def test_input_order_does_not_change_plan_digest(self) -> None:
        items = (
            candidate("a", ambiguity=0.4),
            candidate("b", confidence=0.5),
            candidate("c", scope_breadth=0.8),
            candidate("d"),
        )
        digests = {coalesce_interactions(order).digest() for order in permutations(items)}
        self.assertEqual(len(digests), 1)


class BoundaryIsolationTests(unittest.TestCase):
    def test_each_high_risk_boundary_is_isolated(self) -> None:
        risky = (
            candidate("destructive", destructive=True, rollback_available=True),
            candidate("auth", crosses_auth_boundary=True),
            candidate("external", external_side_effect=True, ambiguity=0.4),
            candidate("sensitive", data_sensitivity=0.8, ambiguity=0.4),
            candidate("cost", monetary_cost=0.8, ambiguity=0.4),
        )
        plan = coalesce_interactions(risky)
        self.assertEqual(len(plan.batches), len(risky))
        self.assertTrue(all(batch.isolated for batch in plan.batches))
        self.assertTrue(all(len(batch.action_ids) == 1 for batch in plan.batches))

    def test_freeze_is_always_isolated(self) -> None:
        frozen = candidate(
            "frozen",
            destructive=True,
            rollback_available=False,
            reversibility=0.0,
        )
        plan = coalesce_interactions([frozen])
        self.assertEqual(plan.batches[0].decision, Decision.FREEZE)
        self.assertIn("FREEZE_ISOLATED", plan.batches[0].isolation_reasons)

    def test_oversized_single_interaction_is_explicitly_isolated(self) -> None:
        item = candidate("preview", ambiguity=0.4)
        plan = coalesce_interactions(
            [item],
            CoalescingPolicy(max_attention_cost=0),
        )
        self.assertTrue(plan.batches[0].isolated)
        self.assertIn(
            "ATTENTION_COST_EXCEEDS_BATCH_LIMIT",
            plan.batches[0].isolation_reasons,
        )

    def test_exhaustive_boundary_grid_never_coalesces_risky_actions(self) -> None:
        items = []
        index = 0
        for destructive, auth, external, sensitive, material in product(
            (False, True), repeat=5
        ):
            if not any((destructive, auth, external, sensitive, material)):
                continue
            items.append(
                candidate(
                    f"risk-{index:02d}",
                    destructive=destructive,
                    rollback_available=True,
                    crosses_auth_boundary=auth,
                    external_side_effect=external,
                    data_sensitivity=0.8 if sensitive else 0.0,
                    monetary_cost=0.8 if material else 0.0,
                    ambiguity=0.4,
                )
            )
            index += 1
        plan = coalesce_interactions(items)
        self.assertEqual(len(plan.batches), 31)
        self.assertTrue(all(batch.isolated for batch in plan.batches))
        self.assertTrue(all(len(batch.action_ids) == 1 for batch in plan.batches))

    def test_candidate_identity_fields_are_required(self) -> None:
        base = candidate("a", ambiguity=0.4)
        for field in ("authority_digest", "decision_policy_digest", "interaction_context"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                replace(base, **{field: ""})


class SyntheticMetricsTests(unittest.TestCase):
    def test_interruption_reduction_is_exact_and_deterministic(self) -> None:
        items = [
            candidate(f"team-a-{index:02d}", ambiguity=0.4, context="team-a")
            for index in range(6)
        ] + [
            candidate(f"team-b-{index:02d}", confidence=0.5, context="team-b")
            for index in range(6)
        ]
        plan = coalesce_interactions(
            items,
            CoalescingPolicy(max_actions=4, max_attention_cost=10),
        )
        self.assertEqual(plan.metrics.interruptions_before, 12)
        self.assertEqual(plan.metrics.interruptions_after, 4)
        self.assertEqual(plan.metrics.interruptions_avoided, 8)
        self.assertEqual(plan.metrics.reduction_ratio, 8 / 12)
        self.assertEqual(len({plan.digest() for _ in range(100)}), 1)


if __name__ == "__main__":
    unittest.main()
