import unittest

from authority_provenance import AuthorityRef, PolicyEnvelope
from human_agency_lab import AgencyPolicy, Decision, RequestProfile
from transaction_graph import TransactionNode, TransactionPlan, evaluate_transaction


class TransactionPlanTests(unittest.TestCase):
    def test_empty_plan_rejected(self):
        with self.assertRaises(ValueError):
            TransactionPlan("tx", tuple())

    def test_duplicate_node_rejected(self):
        node = TransactionNode("a", RequestProfile(action_id="read:a"))
        with self.assertRaises(ValueError):
            TransactionPlan("tx", (node, node))

    def test_unknown_dependency_rejected(self):
        node = TransactionNode(
            "a", RequestProfile(action_id="read:a"), depends_on=("missing",)
        )
        with self.assertRaises(ValueError):
            TransactionPlan("tx", (node,))

    def test_self_dependency_rejected(self):
        with self.assertRaises(ValueError):
            TransactionNode(
                "a", RequestProfile(action_id="read:a"), depends_on=("a",)
            )

    def test_cycle_rejected(self):
        a = TransactionNode(
            "a", RequestProfile(action_id="read:a"), depends_on=("b",)
        )
        b = TransactionNode(
            "b", RequestProfile(action_id="read:b"), depends_on=("a",)
        )
        with self.assertRaises(ValueError):
            TransactionPlan("tx", (a, b))

    def test_topological_order_is_stable_and_lexical_for_ready_nodes(self):
        c = TransactionNode(
            "c", RequestProfile(action_id="read:c"), depends_on=("a", "b")
        )
        b = TransactionNode("b", RequestProfile(action_id="read:b"))
        a = TransactionNode("a", RequestProfile(action_id="read:a"))
        plan = TransactionPlan("tx", (c, b, a))
        self.assertEqual(plan.topological_order(), ("a", "b", "c"))

    def test_plan_digest_is_declaration_order_invariant(self):
        a = TransactionNode("a", RequestProfile(action_id="read:a"))
        b = TransactionNode(
            "b", RequestProfile(action_id="read:b"), depends_on=("a",)
        )
        left = TransactionPlan("tx", (a, b))
        right = TransactionPlan("tx", (b, a))
        self.assertEqual(left.digest(), right.digest())


class TransactionEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.policy = PolicyEnvelope("agency", "1", "1", AgencyPolicy())

    def test_all_low_risk_nodes_proceed(self):
        plan = TransactionPlan(
            "tx",
            (
                TransactionNode("a", RequestProfile(action_id="read:a")),
                TransactionNode(
                    "b", RequestProfile(action_id="read:b"), depends_on=("a",)
                ),
            ),
        )
        result = evaluate_transaction(
            plan, authorities={}, revision=1, policy=self.policy
        )
        self.assertEqual(result.overall_decision, Decision.PROCEED)

    def test_hidden_destructive_node_freezes_whole_transaction(self):
        plan = TransactionPlan(
            "tx",
            (
                TransactionNode("read", RequestProfile(action_id="read:a")),
                TransactionNode(
                    "delete",
                    RequestProfile(
                        action_id="repo:delete",
                        destructive=True,
                        rollback_available=False,
                        reversibility=0.0,
                    ),
                    depends_on=("read",),
                ),
            ),
        )
        authority = AuthorityRef(
            "a1", "user", ("repo:",), allow_destructive=True
        )
        result = evaluate_transaction(
            plan,
            authorities={"delete": authority},
            revision=1,
            policy=self.policy,
        )
        self.assertEqual(result.overall_decision, Decision.FREEZE)
        self.assertEqual(result.recovery_groups.blocked, ("delete",))

    def test_missing_authority_on_high_impact_node_freezes_transaction(self):
        plan = TransactionPlan(
            "tx",
            (
                TransactionNode("read", RequestProfile(action_id="read:a")),
                TransactionNode(
                    "wide",
                    RequestProfile(action_id="repo:wide", scope_breadth=0.9),
                ),
            ),
        )
        result = evaluate_transaction(
            plan, authorities={}, revision=1, policy=self.policy
        )
        self.assertEqual(result.overall_decision, Decision.FREEZE)

    def test_confirm_dominates_preview_and_proceed(self):
        plan = TransactionPlan(
            "tx",
            (
                TransactionNode("read", RequestProfile(action_id="read:a")),
                TransactionNode(
                    "preview",
                    RequestProfile(action_id="repo:bulk", scope_breadth=0.8),
                ),
                TransactionNode(
                    "send",
                    RequestProfile(
                        action_id="repo:send",
                        external_side_effect=True,
                        data_sensitivity=0.9,
                    ),
                ),
            ),
        )
        wide = AuthorityRef("a-wide", "user", ("repo:bulk",))
        send = AuthorityRef(
            "a-send", "user", ("repo:send",), allow_external_effect=True
        )
        result = evaluate_transaction(
            plan,
            authorities={"preview": wide, "send": send},
            revision=1,
            policy=self.policy,
        )
        self.assertEqual(result.overall_decision, Decision.CONFIRM)

    def test_destructive_with_rollback_groups_rollback_and_confirms(self):
        plan = TransactionPlan(
            "tx",
            (
                TransactionNode(
                    "delete",
                    RequestProfile(
                        action_id="repo:delete",
                        destructive=True,
                        rollback_available=True,
                        reversibility=0.8,
                    ),
                ),
            ),
        )
        authority = AuthorityRef(
            "a1", "user", ("repo:",), allow_destructive=True
        )
        result = evaluate_transaction(
            plan,
            authorities={"delete": authority},
            revision=1,
            policy=self.policy,
        )
        self.assertEqual(result.overall_decision, Decision.CONFIRM)
        self.assertEqual(result.recovery_groups.rollback_required, ("delete",))

    def test_external_effect_groups_checkpoint(self):
        plan = TransactionPlan(
            "tx",
            (
                TransactionNode(
                    "send",
                    RequestProfile(action_id="repo:send", external_side_effect=True),
                ),
            ),
        )
        authority = AuthorityRef(
            "a1", "user", ("repo:",), allow_external_effect=True
        )
        result = evaluate_transaction(
            plan,
            authorities={"send": authority},
            revision=1,
            policy=self.policy,
        )
        self.assertEqual(result.recovery_groups.checkpoint_required, ("send",))

    def test_evaluation_digest_repeatability(self):
        plan = TransactionPlan(
            "tx",
            (
                TransactionNode("a", RequestProfile(action_id="read:a")),
                TransactionNode("b", RequestProfile(action_id="read:b")),
            ),
        )
        digests = {
            evaluate_transaction(
                plan, authorities={}, revision=1, policy=self.policy
            ).digest()
            for _ in range(500)
        }
        self.assertEqual(len(digests), 1)


if __name__ == "__main__":
    unittest.main()
