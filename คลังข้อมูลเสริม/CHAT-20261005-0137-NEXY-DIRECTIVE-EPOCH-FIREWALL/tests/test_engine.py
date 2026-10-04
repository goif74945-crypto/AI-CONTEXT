from __future__ import annotations

import unittest
from dataclasses import replace

from nexy_def import (
    ActionKind,
    DecisionStatus,
    DirectiveEpochFirewall,
    DirectiveEvent,
    DirectiveOperation,
    EngineStatus,
    JournalRecord,
    ProtocolError,
)


def new_event(event_id="e1", directive_id="d1", allowed=None):
    return DirectiveEvent(
        event_id=event_id,
        directive_id=directive_id,
        operation=DirectiveOperation.NEW,
        allowed_actions=tuple(allowed or [ActionKind.READ, ActionKind.REVERSIBLE_WRITE]),
        constraints={"project": "alpha"},
    )


class FirewallTests(unittest.TestCase):
    def test_valid_reversible_action_commits(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        action = fw.prepare_action("a1", ActionKind.REVERSIBLE_WRITE, {"path": "x"})
        decision = fw.commit_gate(action)
        self.assertEqual(decision.status, DecisionStatus.ALLOW)
        self.assertEqual(decision.code, "CURRENT_AND_AUTHORIZED")

    def test_replace_invalidates_prepared_action_and_freezes(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        action = fw.prepare_action("a1", ActionKind.REVERSIBLE_WRITE, {"path": "x"})
        fw.apply(
            DirectiveEvent(
                event_id="e2",
                directive_id="d2",
                operation=DirectiveOperation.REPLACE,
                expected_epoch=1,
                allowed_actions=(ActionKind.READ,),
            )
        )
        decision = fw.commit_gate(action)
        self.assertEqual(decision.status, DecisionStatus.FREEZE)
        self.assertEqual(decision.code, "STALE_DIRECTIVE_EPOCH")
        self.assertEqual(fw.state.status, EngineStatus.FROZEN)

    def test_narrow_cannot_expand_scope(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event(allowed=[ActionKind.READ]))
        state = fw.apply(
            DirectiveEvent(
                event_id="e2",
                directive_id="d1-narrow",
                operation=DirectiveOperation.NARROW,
                expected_epoch=1,
                allowed_actions=(ActionKind.READ, ActionKind.REVERSIBLE_WRITE),
            )
        )
        self.assertEqual(state.status, EngineStatus.FROZEN)
        self.assertEqual(state.freeze_reason, "NARROW_ATTEMPTED_SCOPE_EXPANSION")

    def test_narrow_reduces_scope_and_old_action_becomes_stale(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        action = fw.prepare_action("a1", ActionKind.REVERSIBLE_WRITE, {"path": "x"})
        fw.apply(
            DirectiveEvent(
                event_id="e2",
                directive_id="d1-narrow",
                operation=DirectiveOperation.NARROW,
                expected_epoch=1,
                allowed_actions=(ActionKind.READ,),
            )
        )
        decision = fw.commit_gate(action)
        self.assertEqual(decision.code, "STALE_DIRECTIVE_EPOCH")

    def test_irreversible_requires_exact_approval_binding(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event(allowed=[ActionKind.IRREVERSIBLE_WRITE]))
        action = fw.prepare_action("a1", ActionKind.IRREVERSIBLE_WRITE, {"target": "prod"})
        denied = fw.commit_gate(action)
        self.assertEqual(denied.status, DecisionStatus.REJECT)
        self.assertEqual(denied.code, "EXPLICIT_APPROVAL_REQUIRED")
        approved = replace(action, approval_binding=fw.expected_approval_binding(action))
        allowed = fw.commit_gate(approved)
        self.assertEqual(allowed.status, DecisionStatus.ALLOW)

    def test_revoke_blocks_prepared_action(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        action = fw.prepare_action("a1", ActionKind.READ, {"query": "x"})
        fw.apply(
            DirectiveEvent(
                event_id="e2",
                directive_id="d1",
                operation=DirectiveOperation.REVOKE,
                expected_epoch=1,
            )
        )
        decision = fw.commit_gate(action)
        self.assertEqual(decision.status, DecisionStatus.FREEZE)
        self.assertEqual(decision.code, "DIRECTIVE_REVOKED")

    def test_tampered_payload_freezes(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        action = fw.prepare_action("a1", ActionKind.READ, {"query": "safe"})
        tampered = replace(action, payload={"query": "changed"})
        decision = fw.commit_gate(tampered)
        self.assertEqual(decision.status, DecisionStatus.FREEZE)
        self.assertEqual(decision.code, "ACTION_DIGEST_MISMATCH")

    def test_expected_epoch_mismatch_freezes(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        state = fw.apply(
            DirectiveEvent(
                event_id="e2",
                directive_id="d2",
                operation=DirectiveOperation.REPLACE,
                expected_epoch=0,
                allowed_actions=(ActionKind.READ,),
            )
        )
        self.assertEqual(state.status, EngineStatus.FROZEN)
        self.assertEqual(state.freeze_reason, "EXPECTED_EPOCH_MISMATCH")

    def test_duplicate_event_same_payload_is_idempotent(self):
        fw = DirectiveEpochFirewall()
        event = new_event()
        first = fw.apply(event)
        second = fw.apply(event)
        self.assertEqual(first.state_hash, second.state_hash)
        self.assertEqual(len(fw.applied_events), 1)

    def test_duplicate_event_id_different_payload_freezes(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        state = fw.apply(new_event(event_id="e1", directive_id="DIFFERENT"))
        self.assertEqual(state.status, EngineStatus.FROZEN)
        self.assertEqual(state.freeze_reason, "EVENT_ID_REUSE_WITH_DIFFERENT_CONTENT")

    def test_replay_is_deterministic(self):
        events = [
            new_event(),
            DirectiveEvent(
                event_id="e2",
                directive_id="d2",
                operation=DirectiveOperation.REPLACE,
                expected_epoch=1,
                allowed_actions=(ActionKind.READ,),
                constraints={"project": "beta"},
            ),
        ]
        a = DirectiveEpochFirewall.replay(events)
        b = DirectiveEpochFirewall.replay(events)
        self.assertEqual(a.state.state_hash, b.state.state_hash)
        self.assertEqual(a.state.lineage_hash, b.state.lineage_hash)

    def test_recovery_requires_new_replacement_and_old_action_stays_invalid(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        old = fw.prepare_action("a1", ActionKind.READ, {"query": "x"})
        fw.apply(new_event(event_id="e1", directive_id="collision"))
        self.assertEqual(fw.state.status, EngineStatus.FROZEN)
        recovered = fw.recover_with_replacement(
            DirectiveEvent(
                event_id="e3",
                directive_id="d3",
                operation=DirectiveOperation.REPLACE,
                expected_epoch=1,
                allowed_actions=(ActionKind.READ,),
            )
        )
        self.assertEqual(recovered.status, EngineStatus.ACTIVE)
        decision = fw.commit_gate(old)
        self.assertEqual(decision.code, "STALE_DIRECTIVE_EPOCH")

    def test_prepare_outside_scope_rejected(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event(allowed=[ActionKind.READ]))
        with self.assertRaises(ProtocolError):
            fw.prepare_action("a1", ActionKind.REVERSIBLE_WRITE, {"path": "x"})

    def test_full_journal_replay_reproduces_commit_freeze(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        old = fw.prepare_action("a1", ActionKind.REVERSIBLE_WRITE, {"path": "x"})
        fw.apply(
            DirectiveEvent(
                event_id="e2", directive_id="d2", operation=DirectiveOperation.REPLACE,
                expected_epoch=1, allowed_actions=(ActionKind.READ,)
            )
        )
        fw.commit_gate(old)
        self.assertEqual(fw.state.status, EngineStatus.FROZEN)
        replayed = DirectiveEpochFirewall.replay_journal(fw.journal)
        self.assertEqual(replayed.state.state_hash, fw.state.state_hash)
        self.assertEqual(replayed.journal_head, fw.journal_head)

    def test_failed_directive_attempt_is_journaled_and_replayable(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event(allowed=[ActionKind.READ]))
        fw.apply(
            DirectiveEvent(
                event_id="e2", directive_id="bad-narrow", operation=DirectiveOperation.NARROW,
                expected_epoch=1, allowed_actions=(ActionKind.READ, ActionKind.REVERSIBLE_WRITE)
            )
        )
        self.assertEqual(fw.state.status, EngineStatus.FROZEN)
        self.assertEqual(fw.journal[-1].outcome_code, "NARROW_ATTEMPTED_SCOPE_EXPANSION")
        replayed = DirectiveEpochFirewall.replay_journal(fw.journal)
        self.assertEqual(replayed.state.state_hash, fw.state.state_hash)

    def test_journal_tamper_is_detected(self):
        fw = DirectiveEpochFirewall()
        fw.apply(new_event())
        original = fw.journal[0]
        tampered = JournalRecord(
            index=original.index, kind=original.kind, payload={**original.payload, "directive_id": "tampered"},
            outcome_code=original.outcome_code, resulting_state_hash=original.resulting_state_hash,
            previous_record_hash=original.previous_record_hash, record_hash=original.record_hash
        )
        with self.assertRaises(ProtocolError):
            DirectiveEpochFirewall.replay_journal([tampered])


if __name__ == "__main__":
    unittest.main()
