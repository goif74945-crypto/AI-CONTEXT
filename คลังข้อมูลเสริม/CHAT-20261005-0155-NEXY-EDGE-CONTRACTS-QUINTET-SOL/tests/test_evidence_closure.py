import unittest

from frontierfive.evidence_closure import Claim, EvidenceAction, plan_evidence_closure


class EvidenceClosureTests(unittest.TestCase):
    def test_selects_exact_lowest_cost_plan(self):
        claims = {
            "static": Claim("static", 1),
            "unit": Claim("unit", 2, ("static",)),
        }
        actions = [
            EvidenceAction("compile", (("static", 1),), 2),
            EvidenceAction("unit", (("unit", 2),), 3, requires=(("static", 1),)),
            EvidenceAction("all", (("static", 1), ("unit", 2)), 9),
        ]
        v = plan_evidence_closure(claims=claims, targets=["unit"], existing={}, actions=actions)
        self.assertEqual(v.status, "ALLOW")
        self.assertEqual(v.payload["actions"], ["compile", "unit"])
        self.assertEqual(v.payload["cost"], 5)

    def test_existing_evidence_can_zero_cost(self):
        claims = {"c": Claim("c", 2)}
        v = plan_evidence_closure(claims=claims, targets=["c"], existing={"c": 2}, actions=[])
        self.assertEqual(v.status, "ALLOW")
        self.assertEqual(v.payload["actions"], [])

    def test_cycle_freezes(self):
        claims = {"a": Claim("a", 1, ("b",)), "b": Claim("b", 1, ("a",))}
        v = plan_evidence_closure(claims=claims, targets=["a"], existing={}, actions=[])
        self.assertIn("CLAIM_CYCLE", v.reasons)

    def test_impossible_closure_freezes(self):
        claims = {"c": Claim("c", 3)}
        v = plan_evidence_closure(claims=claims, targets=["c"], existing={}, actions=[])
        self.assertIn("NO_EVIDENCE_CLOSURE", v.reasons)

    def test_state_limit_never_false_passes(self):
        claims = {"a": Claim("a", 2)}
        actions = [EvidenceAction("e1", (("a", 1),), 1), EvidenceAction("e2", (("a", 2),), 2)]
        v = plan_evidence_closure(claims=claims, targets=["a"], existing={}, actions=actions, max_states=1)
        self.assertIn("STATE_LIMIT_EXCEEDED", v.reasons)
