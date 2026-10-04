import itertools
import unittest

from lo4lab.upa import EvidenceValue, TruthState


class UpaTests(unittest.TestCase):
    def test_knowledge_join_detects_conflict(self):
        t = EvidenceValue(TruthState.TRUE, ("source-a",))
        f = EvidenceValue(TruthState.FALSE, ("source-b",))
        merged = t.knowledge_join(f)
        self.assertEqual(merged.state, TruthState.CONFLICT)
        self.assertEqual(merged.provenance, ("source-a", "source-b"))
        self.assertFalse(merged.releaseable)

    def test_unknown_plus_true_knowledge_becomes_true(self):
        u = EvidenceValue(TruthState.UNKNOWN, ("missing",))
        t = EvidenceValue(TruthState.TRUE, ("proof",))
        self.assertEqual(u.knowledge_join(t).state, TruthState.TRUE)

    def test_de_morgan_all_states(self):
        values = [EvidenceValue(s) for s in TruthState]
        for a, b in itertools.product(values, repeat=2):
            left = a.logical_and(b).negate().state
            right = a.negate().logical_or(b.negate()).state
            self.assertEqual(left, right)

    def test_and_or_commutative_all_states(self):
        values = [EvidenceValue(s) for s in TruthState]
        for a, b in itertools.product(values, repeat=2):
            self.assertEqual(a.logical_and(b).state, b.logical_and(a).state)
            self.assertEqual(a.logical_or(b).state, b.logical_or(a).state)

    def test_release_only_true(self):
        for state in TruthState:
            self.assertEqual(EvidenceValue(state).releaseable, state is TruthState.TRUE)


if __name__ == "__main__":
    unittest.main()
