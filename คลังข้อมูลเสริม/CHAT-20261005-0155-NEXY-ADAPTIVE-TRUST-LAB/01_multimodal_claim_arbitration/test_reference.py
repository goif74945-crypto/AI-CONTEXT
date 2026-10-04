import unittest
from reference import Claim, Policy, arbitrate


class TestMCAE(unittest.TestCase):
    def test_consensus_allows(self):
        claims = [
            Claim("c1", "door", "closed", "vision", "camera-a", "verified", 0.95),
            Claim("c2", "door", "closed", "sensor", "reed-a", "observed", 0.99),
        ]
        d = arbitrate(claims)
        self.assertEqual(d.status, "ALLOW")
        self.assertEqual(d.value, "closed")

    def test_top_tier_conflict_freezes_as_conflict(self):
        claims = [
            Claim("c1", "state", "A", "tool", "s1", "authoritative", 1.0),
            Claim("c2", "state", "B", "tool", "s2", "authoritative", 1.0),
            Claim("c3", "state", "A", "text", "s3", "generated", 1.0),
        ]
        self.assertEqual(arbitrate(claims).status, "CONFLICT")

    def test_same_source_cannot_repeat_to_win(self):
        claims = [
            Claim("a1", "x", "A", "text", "same", "generated", 1.0),
            Claim("a2", "x", "A", "audio", "same", "generated", 1.0),
            Claim("b1", "x", "B", "tool", "other", "observed", 1.0),
        ]
        d = arbitrate(claims, Policy(min_score=1.0, min_margin=0.5))
        self.assertEqual(d.value, "B")

    def test_small_margin_freezes(self):
        claims = [
            Claim("a", "x", "A", "tool", "s1", "observed", 0.30),
            Claim("b", "x", "B", "text", "s2", "generated", 0.55),
        ]
        self.assertEqual(arbitrate(claims, Policy(min_score=0.5, min_margin=0.5)).status, "FREEZE")

    def test_invalid_confidence_freezes(self):
        d = arbitrate([Claim("a", "x", 1, "tool", "s", "verified", 1.2)])
        self.assertEqual(d.reason, "INVALID_CONFIDENCE")


if __name__ == "__main__":
    unittest.main()
