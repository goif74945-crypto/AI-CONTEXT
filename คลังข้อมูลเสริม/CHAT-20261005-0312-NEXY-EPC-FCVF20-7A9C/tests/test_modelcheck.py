import unittest
from dataclasses import replace

from epc_fcvf.engine import Constitution, initial_state
from epc_fcvf.fixtures import evidence_events, keep_event, cut_event, pins, ready_event
from epc_fcvf.model import Event, EventKind, WorkStatus
from epc_fcvf.modelcheck import execute_trace, explore, minimize_counterexample
from epc_fcvf.regression import find_weakening_witness
from epc_fcvf.systems import evaluate_all


class ModelCheckTests(unittest.TestCase):
    def setUp(self):
        self.initial = initial_state(
            chat_id="CHAT-MODEL",
            candidate_id="FCVF",
            candidate_path="path/fcvf",
            pins=pins(),
        )
        ev = evidence_events()
        self.alphabet = (
            Event(EventKind.SET_STATUS, status=WorkStatus.WIP),
            Event(EventKind.SET_STATUS, status=WorkStatus.READY),
            Event(EventKind.SET_STATUS, status=WorkStatus.INSUFFICIENT_EVIDENCE),
            *ev,
            keep_event(1),
            keep_event(2),
            cut_event(1),
            cut_event(2),
            Event(EventKind.DEFER),
            Event(EventKind.ATTEMPT_PROMOTION),
            Event(EventKind.ATTEMPT_CORE_MUTATION),
            Event(EventKind.ATTEMPT_CANON_OVERRIDE),
        )

    def test_bounded_exhaustion_has_no_unsafe_state(self):
        report = explore(self.initial, self.alphabet, depth=6)
        self.assertGreater(report.unique_states, 100)
        self.assertGreater(report.transitions_examined, 1000)
        self.assertEqual(report.unsafe_states, 0, report.first_failure)
        self.assertEqual(len(report.digest), 64)

    def test_exploration_is_deterministic(self):
        r1 = explore(self.initial, self.alphabet, depth=5)
        r2 = explore(self.initial, self.alphabet, depth=5)
        self.assertEqual(r1, r2)

    def test_weakened_vote_budget_is_detected(self):
        weak = Constitution(max_keep=2)
        trace = (*evidence_events(), ready_event(), keep_event(1), keep_event(2))
        witness = find_weakening_witness(self.initial, [trace], weak)
        self.assertTrue(witness.found)
        self.assertLessEqual(len(witness.minimal_trace), len(trace))
        weak_state, _ = execute_trace(self.initial, witness.minimal_trace, weak)
        self.assertTrue(any(not f.passed for f in evaluate_all(weak_state)))

    def test_promotion_authority_weakening_is_detected_by_invariant(self):
        weak = Constitution(allow_promotion=True)
        state, results = execute_trace(self.initial, [Event(EventKind.ATTEMPT_PROMOTION)], weak)
        self.assertTrue(results[0].accepted)
        failures = [f for f in evaluate_all(state) if not f.passed]
        self.assertIn("PNCG", {f.system_id for f in failures})

    def test_counterexample_reducer_is_deterministic_and_one_minimal(self):
        weak = Constitution(max_keep=2)
        noisy = (
            Event(EventKind.DEFER),
            *evidence_events(),
            Event(EventKind.DEFER),
            ready_event(),
            keep_event(1),
            Event(EventKind.DEFER),
            keep_event(2),
        )
        def violates(trace):
            state, _ = execute_trace(self.initial, trace, weak)
            return any(f.system_id == "LVBA" and not f.passed for f in evaluate_all(state))
        reduced = minimize_counterexample(noisy, violates)
        self.assertTrue(violates(reduced))
        for i in range(len(reduced)):
            trial = reduced[:i] + reduced[i+1:]
            self.assertFalse(trial and violates(trial))


if __name__ == "__main__":
    unittest.main()
