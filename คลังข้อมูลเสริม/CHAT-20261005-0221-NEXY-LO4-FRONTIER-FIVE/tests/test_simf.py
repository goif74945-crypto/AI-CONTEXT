import unittest

from nexy_lo4_frontier import Observation, falsify_shadow_invariants, mine_shadow_invariants


class ShadowInvariantMinerTests(unittest.TestCase):
    def setUp(self):
        self.training = [
            Observation("a", (("status", "PASS"), ("requested", 2), ("granted", 2), ("latency_ms", 10))),
            Observation("b", (("status", "PASS"), ("requested", 4), ("granted", 4), ("latency_ms", 20))),
            Observation("c", (("status", "PASS"), ("requested", 6), ("granted", 6), ("latency_ms", 30))),
        ]

    def test_mines_proposals_without_promoting_them(self):
        report = mine_shadow_invariants(self.training)
        self.assertTrue(report.candidates)
        self.assertTrue(all(x.status == "Lo4_AI_PROPOSAL_ONLY" for x in report.candidates))
        self.assertTrue(any(x.kind == "CONSTANT" and x.fields == ("status",) for x in report.candidates))
        self.assertTrue(any(x.kind == "FIELD_EQUALITY" and x.fields == ("granted", "requested") for x in report.candidates))

    def test_challenge_falsifies_weak_invariants(self):
        mined = mine_shadow_invariants(self.training)
        challenge = [Observation("fault", (("status", "FREEZE"), ("requested", 6), ("granted", 2), ("latency_ms", 100)))]
        report = falsify_shadow_invariants(mined.candidates, challenge)
        dead_kinds = {x.invariant_id for x in report.falsified}
        self.assertTrue(dead_kinds)
        self.assertLess(len(report.surviving), len(mined.candidates))

    def test_mining_is_order_deterministic(self):
        a = mine_shadow_invariants(self.training)
        b = mine_shadow_invariants(list(reversed(self.training)))
        self.assertEqual(a.fingerprint, b.fingerprint)


if __name__ == "__main__":
    unittest.main()
