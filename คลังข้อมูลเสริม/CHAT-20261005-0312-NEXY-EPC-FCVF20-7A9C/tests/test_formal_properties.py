import ast
import pathlib
import unittest
from dataclasses import replace

from epc_fcvf.canonical import canonical_hash, canonical_json
from epc_fcvf.engine import Constitution, initial_state, transition
from epc_fcvf.fixtures import cut_event, evidence_events, keep_event, pins, ready_event
from epc_fcvf.model import Event, EventKind, VoteRound
from epc_fcvf.modelcheck import execute_trace
from epc_fcvf.systems import SYSTEM_REGISTRY, evaluate_all


class FormalPropertyTests(unittest.TestCase):
    def setUp(self):
        self.initial = initial_state(
            chat_id="CHAT-FORMAL",
            candidate_id="FCVF",
            candidate_path="path/fcvf",
            pins=pins(),
        )

    def test_evidence_is_monotone_across_accepted_transitions(self):
        state = self.initial
        trace = (*evidence_events(), ready_event(), Event(EventKind.DEFER), keep_event())
        prior = frozenset(state.evidence)
        for event in trace:
            result = transition(state, event)
            self.assertTrue(result.accepted)
            now = frozenset(result.state.evidence)
            self.assertTrue(prior.issubset(now))
            prior = now
            state = result.state

    def test_blocked_authority_events_are_state_identity(self):
        for kind in (
            EventKind.ATTEMPT_PROMOTION,
            EventKind.ATTEMPT_CORE_MUTATION,
            EventKind.ATTEMPT_CANON_OVERRIDE,
        ):
            result = transition(self.initial, Event(kind))
            self.assertFalse(result.accepted)
            self.assertIs(result.state, self.initial)
            self.assertEqual(canonical_hash(result.state), canonical_hash(self.initial))

    def test_weak_core_mutation_is_detected(self):
        weak = Constitution(allow_core_mutation=True)
        state, results = execute_trace(self.initial, [Event(EventKind.ATTEMPT_CORE_MUTATION)], weak)
        self.assertTrue(results[0].accepted)
        failed = {f.system_id for f in evaluate_all(state) if not f.passed}
        self.assertIn("ANIC", failed)
        self.assertIn("PWCV", failed)

    def test_weak_canon_override_is_detected(self):
        weak = Constitution(allow_canon_override=True)
        state, results = execute_trace(self.initial, [Event(EventKind.ATTEMPT_CANON_OVERRIDE)], weak)
        self.assertTrue(results[0].accepted)
        failed = {f.system_id for f in evaluate_all(state) if not f.passed}
        self.assertIn("CNOP", failed)
        self.assertIn("PWCV", failed)

    def test_cut_receipt_is_non_destructive_and_canonical(self):
        state, results = execute_trace(self.initial, (*evidence_events(), ready_event(), cut_event()))
        self.assertTrue(all(r.accepted for r in results))
        self.assertEqual(state.count_round(VoteRound.CUT), 1)
        encoded1 = canonical_json(state.votes[0])
        encoded2 = canonical_json(state.votes[0])
        self.assertEqual(encoded1, encoded2)
        self.assertNotIn('DELETE', encoded1.upper())
        self.assertNotIn('REMOVE', encoded1.upper())

    def test_registry_binds_all_20_ids_to_callable_checks(self):
        self.assertEqual(len(SYSTEM_REGISTRY), 20)
        for system in SYSTEM_REGISTRY:
            self.assertTrue(system.system_id)
            self.assertTrue(system.name)
            self.assertTrue(system.purpose)
            self.assertTrue(callable(system.check))

    def test_authoritative_source_contains_no_float_literals(self):
        root = pathlib.Path(__file__).parents[1] / "src" / "epc_fcvf"
        floats = []
        for path in sorted(root.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, float):
                    floats.append((str(path), node.lineno, node.value))
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
