import unittest
from dataclasses import replace

from epc_fcvf.canonical import canonical_hash
from epc_fcvf.engine import initial_state, transition
from epc_fcvf.fixtures import evidence_events, keep_event, cut_event, pins, ready_event, h
from epc_fcvf.model import Disposition, EvidenceKind, EvidenceRef, Event, EventKind, VoteRound, WorkStatus
from epc_fcvf.modelcheck import execute_trace
from epc_fcvf.systems import SYSTEM_REGISTRY, evaluate_all


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.state = initial_state(
            chat_id="CHAT-T",
            candidate_id="CAND",
            candidate_path="path/cand",
            pins=pins(),
        )

    def completed(self):
        s, results = execute_trace(self.state, (*evidence_events(), ready_event()))
        self.assertTrue(all(r.accepted for r in results))
        return s

    def test_exactly_twenty_systems_unique(self):
        self.assertEqual(len(SYSTEM_REGISTRY), 20)
        self.assertEqual(len({x.system_id for x in SYSTEM_REGISTRY}), 20)

    def test_keep_once(self):
        s = self.completed()
        first = transition(s, keep_event(1))
        self.assertTrue(first.accepted)
        second = transition(first.state, keep_event(2))
        self.assertFalse(second.accepted)
        self.assertEqual(second.code, "KEEP_RIGHT_EXHAUSTED")
        self.assertEqual(first.state.count_round(VoteRound.KEEP), 1)

    def test_cut_once(self):
        s = self.completed()
        first = transition(s, cut_event(1))
        self.assertTrue(first.accepted)
        second = transition(first.state, cut_event(2))
        self.assertFalse(second.accepted)
        self.assertEqual(second.code, "CUT_RIGHT_EXHAUSTED")
        self.assertIn(first.state.disposition, {Disposition.ARCHIVED, Disposition.REJECTED, Disposition.SUPERSEDED})

    def test_defer_consumes_no_rights(self):
        s = self.state
        for _ in range(5):
            result = transition(s, Event(EventKind.DEFER))
            self.assertTrue(result.accepted)
            s = result.state
        self.assertEqual(s.count_round(VoteRound.KEEP), 0)
        self.assertEqual(s.count_round(VoteRound.CUT), 0)
        self.assertEqual(s.defer_count, 5)

    def test_wip_cut_forbidden_even_with_evidence(self):
        s, _ = execute_trace(self.state, evidence_events())
        r = transition(s, cut_event())
        self.assertFalse(r.accepted)
        self.assertEqual(r.code, "WIP_OR_INSUFFICIENT_CUT_FORBIDDEN")

    def test_insufficient_cut_forbidden(self):
        s, _ = execute_trace(self.state, evidence_events())
        s = transition(s, Event(EventKind.SET_STATUS, status=WorkStatus.INSUFFICIENT_EVIDENCE)).state
        r = transition(s, cut_event())
        self.assertFalse(r.accepted)

    def test_missing_evidence_blocks_vote(self):
        s = transition(self.state, ready_event()).state
        r = transition(s, keep_event())
        self.assertFalse(r.accepted)
        self.assertEqual(r.code, "CRITICAL_EVIDENCE_INCOMPLETE")

    def test_authority_escalations_blocked_and_noninterfering(self):
        for kind, code in (
            (EventKind.ATTEMPT_PROMOTION, "PROMOTION_AUTHORITY_FORBIDDEN"),
            (EventKind.ATTEMPT_CORE_MUTATION, "CORE_MUTATION_FORBIDDEN"),
            (EventKind.ATTEMPT_CANON_OVERRIDE, "CANON_OVERRIDE_FORBIDDEN"),
        ):
            r = transition(self.state, Event(kind))
            self.assertFalse(r.accepted)
            self.assertEqual(r.code, code)
            self.assertEqual(r.state, self.state)

    def test_verdict_immutable_revision(self):
        s = transition(self.completed(), keep_event()).state
        r = transition(s, Event(
            EventKind.REVISE_VOTE,
            target_vote_id="VOTE-KEEP-1",
            revision_id="REV-1",
            reason="CHANGE_VERDICT:CUT",
            note="malicious retrospective rewrite",
        ))
        self.assertFalse(r.accepted)
        self.assertEqual(r.code, "VERDICT_IMMUTABLE")

    def test_append_only_revision_allowed(self):
        s = transition(self.completed(), keep_event()).state
        r = transition(s, Event(
            EventKind.REVISE_VOTE,
            target_vote_id="VOTE-KEEP-1",
            revision_id="REV-1",
            reason="ADD_EVIDENCE",
            note="new non-verdict evidence",
        ))
        self.assertTrue(r.accepted)
        self.assertEqual(r.state.votes, s.votes)
        self.assertEqual(len(r.state.revisions), 1)

    def test_duplicate_evidence_requires_target_and_witness(self):
        bad = EvidenceRef(EvidenceKind.SEMANTIC_DUPLICATE, "dup", h("dup"))
        r = transition(self.state, Event(EventKind.ATTACH_EVIDENCE, evidence=bad))
        self.assertFalse(r.accepted)
        self.assertEqual(r.code, "SEMANTIC_DUPLICATE_WITNESS_REQUIRED")
        good = EvidenceRef(
            EvidenceKind.SEMANTIC_DUPLICATE, "dup", h("dup2"),
            semantic_target="path/existing", semantic_witness="semantic-proof-v1"
        )
        r2 = transition(self.state, Event(EventKind.ATTACH_EVIDENCE, evidence=good))
        self.assertTrue(r2.accepted)

    def test_permutation_equivalence(self):
        ev = evidence_events()
        s1, _ = execute_trace(self.state, (*ev, ready_event(), keep_event()))
        s2, _ = execute_trace(self.state, (*reversed(ev), ready_event(), keep_event()))
        self.assertEqual(canonical_hash(s1), canonical_hash(s2))

    def test_all_systems_pass_valid_state(self):
        s = transition(self.completed(), keep_event()).state
        findings = evaluate_all(s)
        self.assertEqual(len(findings), 20)
        self.assertTrue(all(f.passed for f in findings), findings)


if __name__ == "__main__":
    unittest.main()
