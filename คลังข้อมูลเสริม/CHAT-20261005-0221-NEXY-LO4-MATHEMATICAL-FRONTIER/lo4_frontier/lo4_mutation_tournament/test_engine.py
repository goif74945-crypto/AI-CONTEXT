import unittest
from lo4_frontier.lo4_mutation_tournament.engine import run_tournament

class TournamentTests(unittest.TestCase):
    def test_invariant_failure_cannot_win(self):
        candidates = [
            {"id":"unsafe","metrics":{"safety":1,"utility":1,"proof":1,"reversibility":1,"novelty":1},"invariant_failures":["CANON_WRITE"]},
            {"id":"safe","metrics":{"safety":0.95,"utility":0.8,"proof":0.9,"reversibility":0.9,"novelty":0.7},"invariant_failures":[]},
        ]
        r = run_tournament(candidates)
        self.assertEqual(r["winner_id"], "safe")
        self.assertFalse(r["promotion_permitted"])
        self.assertEqual(r["rejected"]["unsafe"], "INVARIANT_FAILURE")

    def test_pareto_frontier_excludes_dominated_candidate(self):
        candidates = [
            {"id":"a","metrics":{"safety":0.95,"utility":0.9,"proof":0.9,"reversibility":0.8,"novelty":0.8},"invariant_failures":[]},
            {"id":"b","metrics":{"safety":0.95,"utility":0.8,"proof":0.9,"reversibility":0.8,"novelty":0.8},"invariant_failures":[]},
        ]
        r = run_tournament(candidates)
        self.assertEqual(r["pareto_ids"], ("a",))

    def test_threshold_failure_rejected(self):
        candidate = {"id":"x","metrics":{"safety":0.5,"utility":1,"proof":1,"reversibility":1,"novelty":1},"invariant_failures":[]}
        r = run_tournament([candidate])
        self.assertIsNone(r["winner_id"])
        self.assertEqual(r["status"], "NO_ELIGIBLE_CANDIDATE")

    def test_output_is_deterministic(self):
        cs = [
            {"id":"b","metrics":{"safety":0.95,"utility":0.8,"proof":0.9,"reversibility":0.9,"novelty":0.8},"invariant_failures":[]},
            {"id":"a","metrics":{"safety":0.95,"utility":0.8,"proof":0.9,"reversibility":0.9,"novelty":0.8},"invariant_failures":[]},
        ]
        self.assertEqual(run_tournament(cs), run_tournament(list(reversed(cs))))
        self.assertEqual(run_tournament(cs)["winner_id"], "a")
