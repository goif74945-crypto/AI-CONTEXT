from __future__ import annotations

from dataclasses import replace
import unittest

from nexy_lease import (
    Action,
    AuthorityLease,
    DecisionStatus,
    Effect,
    HashChainJournal,
    LeaseState,
    Plan,
    POLICY_VERSION,
    commit_allowed_action,
    derive_child_lease,
    diff_plans,
    evaluate_action,
    plan_fingerprint,
    revoke,
)


class LeasePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = Plan((
            Action("project://alpha/docs/spec.md", "READ", Effect.READ, cost_units=1),
            Action("project://alpha/output/report.md", "WRITE", Effect.REVERSIBLE_WRITE, cost_units=3),
        ))
        self.lease = AuthorityLease(
            lease_id="lease-001",
            subject="agent-a",
            allowed_resource_patterns=("project://alpha/*",),
            allowed_verbs=("READ", "WRITE"),
            allowed_effects=(Effect.READ, Effect.REVERSIBLE_WRITE),
            max_cost_units=10,
            max_actions=3,
            issued_at_tick=10,
            expires_at_tick=20,
            plan_hash=plan_fingerprint(self.plan),
            policy_version=POLICY_VERSION,
        )

    def test_exact_plan_is_allowed_and_commit_updates_budget(self) -> None:
        state = LeaseState()
        decision = evaluate_action(self.lease, state, self.plan, 0, 10)
        self.assertEqual(decision.status, DecisionStatus.ALLOW)
        state = commit_allowed_action(state, self.plan.actions[0], decision)
        self.assertEqual(state.used_actions, 1)
        self.assertEqual(state.used_cost_units, 1)

    def test_plan_drift_freezes_even_if_new_action_stays_in_broad_scope(self) -> None:
        changed = Plan((
            Action("project://alpha/docs/other.md", "READ", Effect.READ, cost_units=1),
            self.plan.actions[1],
        ))
        decision = evaluate_action(self.lease, LeaseState(), changed, 0, 11)
        self.assertEqual(decision.status, DecisionStatus.FREEZE)
        self.assertEqual(decision.reason_code, "PLAN_HASH_MISMATCH_REAUTHORIZE")

    def test_drift_report_names_semantic_change_categories(self) -> None:
        changed = Plan((
            Action("project://alpha/docs/spec.md", "WRITE", Effect.REVERSIBLE_WRITE, cost_units=2),
            self.plan.actions[1],
        ))
        report = diff_plans(self.plan, changed)
        self.assertTrue(report.changed)
        self.assertEqual(set(report.categories), {"COST_UNITS", "EFFECT", "VERB"})

    def test_resource_scope_violation_freezes(self) -> None:
        outside = Plan((Action("project://beta/x", "READ", Effect.READ),))
        lease = replace(self.lease, plan_hash=plan_fingerprint(outside))
        decision = evaluate_action(lease, LeaseState(), outside, 0, 12)
        self.assertEqual(decision.reason_code, "RESOURCE_OUT_OF_SCOPE")

    def test_verb_scope_violation_freezes(self) -> None:
        plan = Plan((Action("project://alpha/x", "DELETE", Effect.REVERSIBLE_WRITE),))
        lease = replace(self.lease, plan_hash=plan_fingerprint(plan))
        decision = evaluate_action(lease, LeaseState(), plan, 0, 12)
        self.assertEqual(decision.reason_code, "VERB_OUT_OF_SCOPE")

    def test_effect_scope_violation_freezes(self) -> None:
        plan = Plan((Action("project://alpha/x", "WRITE", Effect.IRREVERSIBLE_WRITE),))
        lease = replace(self.lease, plan_hash=plan_fingerprint(plan))
        decision = evaluate_action(lease, LeaseState(), plan, 0, 12)
        self.assertEqual(decision.reason_code, "EFFECT_OUT_OF_SCOPE")

    def test_high_impact_requires_explicit_second_gate(self) -> None:
        plan = Plan((Action("project://alpha/x", "DELETE", Effect.IRREVERSIBLE_WRITE),))
        lease = replace(
            self.lease,
            allowed_verbs=("DELETE",),
            allowed_effects=(Effect.IRREVERSIBLE_WRITE,),
            plan_hash=plan_fingerprint(plan),
            allow_high_impact=False,
        )
        decision = evaluate_action(lease, LeaseState(), plan, 0, 12)
        self.assertEqual(decision.reason_code, "HIGH_IMPACT_NOT_EXPLICITLY_AUTHORIZED")

    def test_expired_and_not_yet_active_leases_freeze(self) -> None:
        before = evaluate_action(self.lease, LeaseState(), self.plan, 0, 9)
        after = evaluate_action(self.lease, LeaseState(), self.plan, 0, 21)
        self.assertEqual(before.reason_code, "LEASE_NOT_ACTIVE")
        self.assertEqual(after.reason_code, "LEASE_EXPIRED")

    def test_revoked_lease_freezes(self) -> None:
        decision = evaluate_action(self.lease, revoke(LeaseState()), self.plan, 0, 11)
        self.assertEqual(decision.reason_code, "LEASE_REVOKED")

    def test_action_and_cost_budgets_freeze(self) -> None:
        by_action = evaluate_action(self.lease, LeaseState(used_actions=3), self.plan, 0, 11)
        by_cost = evaluate_action(self.lease, LeaseState(used_cost_units=10), self.plan, 0, 11)
        self.assertEqual(by_action.reason_code, "ACTION_BUDGET_EXCEEDED")
        self.assertEqual(by_cost.reason_code, "COST_BUDGET_EXCEEDED")

    def test_policy_version_mismatch_freezes(self) -> None:
        lease = replace(self.lease, policy_version="unknown/999")
        decision = evaluate_action(lease, LeaseState(), self.plan, 0, 11)
        self.assertEqual(decision.reason_code, "POLICY_VERSION_MISMATCH")

    def test_child_lease_can_only_narrow_authority(self) -> None:
        child_plan = Plan((Action("project://alpha/docs/spec.md", "READ", Effect.READ),))
        child = derive_child_lease(
            self.lease,
            lease_id="lease-child",
            subject="agent-child",
            allowed_resource_patterns=("project://alpha/docs/spec.md",),
            allowed_verbs=("READ",),
            allowed_effects=(Effect.READ,),
            max_cost_units=5,
            max_actions=1,
            issued_at_tick=10,
            expires_at_tick=15,
            plan_hash=plan_fingerprint(child_plan),
        )
        self.assertEqual(child.parent_lease_id, self.lease.lease_id)
        self.assertEqual(child.allowed_verbs, ("READ",))

    def test_child_novel_wildcard_is_rejected_conservatively(self) -> None:
        child_plan = Plan((Action("project://alpha/docs/spec.md", "READ", Effect.READ),))
        with self.assertRaisesRegex(ValueError, "not provably"):
            derive_child_lease(
                self.lease,
                lease_id="lease-child",
                subject="agent-child",
                allowed_resource_patterns=("project://alpha/docs/*",),
                allowed_verbs=("READ",),
                allowed_effects=(Effect.READ,),
                max_cost_units=5,
                max_actions=1,
                issued_at_tick=10,
                expires_at_tick=15,
                plan_hash=plan_fingerprint(child_plan),
            )

    def test_child_cannot_escalate_high_impact_or_budget_or_expiry(self) -> None:
        child_plan = Plan((Action("project://alpha/docs/spec.md", "READ", Effect.READ),))
        common = dict(
            parent=self.lease,
            lease_id="lease-child",
            subject="agent-child",
            allowed_resource_patterns=("project://alpha/docs/spec.md",),
            allowed_verbs=("READ",),
            allowed_effects=(Effect.READ,),
            max_cost_units=5,
            max_actions=1,
            issued_at_tick=10,
            expires_at_tick=15,
            plan_hash=plan_fingerprint(child_plan),
        )
        with self.assertRaisesRegex(ValueError, "high-impact"):
            derive_child_lease(**common, allow_high_impact=True)
        with self.assertRaisesRegex(ValueError, "cost budget"):
            derive_child_lease(**{**common, "max_cost_units": 11})
        with self.assertRaisesRegex(ValueError, "expires after"):
            derive_child_lease(**{**common, "expires_at_tick": 21})


    def test_high_impact_can_pass_only_when_both_scope_and_second_gate_allow(self) -> None:
        plan = Plan((Action("project://alpha/x", "DELETE", Effect.IRREVERSIBLE_WRITE),))
        lease = replace(
            self.lease,
            allowed_verbs=("DELETE",),
            allowed_effects=(Effect.IRREVERSIBLE_WRITE,),
            plan_hash=plan_fingerprint(plan),
            allow_high_impact=True,
        )
        decision = evaluate_action(lease, LeaseState(), plan, 0, 12)
        self.assertEqual(decision.status, DecisionStatus.ALLOW)

    def test_invalid_action_index_freezes(self) -> None:
        decision = evaluate_action(self.lease, LeaseState(), self.plan, 99, 12)
        self.assertEqual(decision.reason_code, "ACTION_INDEX_INVALID")

    def test_frozen_decision_cannot_mutate_state(self) -> None:
        changed = Plan((Action("project://alpha/other", "READ", Effect.READ),))
        decision = evaluate_action(self.lease, LeaseState(), changed, 0, 12)
        self.assertEqual(decision.status, DecisionStatus.FREEZE)
        with self.assertRaisesRegex(ValueError, "frozen decision"):
            commit_allowed_action(LeaseState(), changed.actions[0], decision)

    def test_destination_change_is_plan_drift(self) -> None:
        granted = Plan((Action("api://mail/send", "SEND", Effect.EXTERNAL_SIDE_EFFECT, destination="alice@example.invalid"),))
        changed = Plan((Action("api://mail/send", "SEND", Effect.EXTERNAL_SIDE_EFFECT, destination="bob@example.invalid"),))
        report = diff_plans(granted, changed)
        self.assertTrue(report.changed)
        self.assertIn("DESTINATION", report.categories)

    def test_deterministic_repeatability(self) -> None:
        state = LeaseState()
        first = evaluate_action(self.lease, state, self.plan, 0, 12)
        for _ in range(1000):
            self.assertEqual(evaluate_action(self.lease, state, self.plan, 0, 12), first)

    def test_action_validation_rejects_negative_cost_and_empty_fields(self) -> None:
        with self.assertRaises(ValueError):
            Action("", "READ", Effect.READ)
        with self.assertRaises(ValueError):
            Action("project://alpha/x", "READ", Effect.READ, cost_units=-1)


class JournalTests(unittest.TestCase):
    def test_hash_chain_verifies_and_tamper_is_detected(self) -> None:
        journal = HashChainJournal()
        e0 = journal.append(logical_tick=1, event_type="LEASE_ISSUED", lease_id="L1", payload={"x": 1})
        e1 = journal.append(logical_tick=2, event_type="DECISION", lease_id="L1", payload={"allow": True})
        self.assertTrue(HashChainJournal.verify(journal.events))
        tampered = replace(e1, previous_hash="f" * 64)
        self.assertFalse(HashChainJournal.verify((e0, tampered)))


if __name__ == "__main__":
    unittest.main()
