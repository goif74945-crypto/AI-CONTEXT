import unittest

from frontierfive.policy_monotonicity import PolicyPoint, audit_monotonicity

RANK = {"ALLOW": 0, "REVIEW": 1, "FREEZE": 2}


class PolicyMonotonicityTests(unittest.TestCase):
    def test_monotone_grid_allows(self):
        pts = [
            PolicyPoint("p0", (0, 2), "ALLOW"),
            PolicyPoint("p1", (1, 2), "REVIEW"),
            PolicyPoint("p2", (2, 1), "FREEZE"),
        ]
        # risk rises when dim0 rises and dim1 falls
        v = audit_monotonicity(pts, directions=(1, -1), decision_rank=RANK)
        self.assertEqual(v.status, "ALLOW")

    def test_relaxation_at_higher_risk_freezes(self):
        pts = [PolicyPoint("safe", (0,), "REVIEW"), PolicyPoint("riskier", (1,), "ALLOW")]
        v = audit_monotonicity(pts, directions=(1,), decision_rank=RANK)
        self.assertIn("NON_MONOTONIC_POLICY", v.reasons)
        self.assertEqual(v.payload["violations"][0]["riskier"], "riskier")

    def test_mixed_direction_detects_violation(self):
        pts = [PolicyPoint("a", (2, 1), "ALLOW"), PolicyPoint("b", (1, 2), "REVIEW")]
        v = audit_monotonicity(pts, directions=(1, -1), decision_rank=RANK)
        self.assertIn("NON_MONOTONIC_POLICY", v.reasons)

    def test_invalid_point_freezes(self):
        v = audit_monotonicity([PolicyPoint("x", (1, 2), "ALLOW")], directions=(1,), decision_rank=RANK)
        self.assertIn("INVALID_POLICY_POINT", v.reasons)
