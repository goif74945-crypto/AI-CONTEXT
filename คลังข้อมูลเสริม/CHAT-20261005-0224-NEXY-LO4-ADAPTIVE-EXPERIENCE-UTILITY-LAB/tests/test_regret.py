import unittest

from aeul.q64 import Q64
from aeul.regret import ProposalCandidate, RegretPolicy, UtilityInterval, select_proposal

q = Q64.from_decimal


def u(lo, hi): return UtilityInterval(q(lo), q(hi))

def cand(i, quality, speed): return ProposalCandidate(i, {"quality": u(*quality), "speed": u(*speed)})

def policy(max_regret="0.4"):
    return RegretPolicy({"quality": q("0.75"), "speed": q("0.25")}, {"quality": q("0.5")}, q(max_regret))


class RegretTests(unittest.TestCase):
    def test_selects_lowest_worst_case_regret(self):
        a = cand("a", ("0.8", "0.9"), ("0.4", "0.7"))
        b = cand("b", ("0.6", "1"), ("0.8", "1"))
        r = select_proposal([a, b], policy())
        self.assertEqual(r.status, "SELECT")
        self.assertEqual(r.selected_id, "a")

    def test_protected_minimum_cannot_be_hidden_by_other_gain(self):
        bad = cand("fast-but-bad", ("0.2", "1"), ("1", "1"))
        r = select_proposal([bad], policy())
        self.assertEqual(r.status, "FREEZE")
        self.assertEqual(r.reason, "ALL_CANDIDATES_VIOLATE_PROTECTED_MINIMA")

    def test_high_regret_holds(self):
        a = cand("a", ("0.5", "1"), ("0", "1"))
        b = cand("b", ("0.5", "1"), ("0", "1"))
        r = select_proposal([a, b], policy("0.01"))
        self.assertEqual(r.status, "HOLD")

    def test_objective_mismatch_freezes(self):
        bad = ProposalCandidate("bad", {"quality": u("0.8", "0.9")})
        r = select_proposal([bad], policy())
        self.assertEqual(r.status, "FREEZE")
        self.assertEqual(r.reason, "OBJECTIVE_SET_MISMATCH")

    def test_duplicate_id_freezes(self):
        a = cand("x", ("0.8", "0.9"), ("0.4", "0.7"))
        r = select_proposal([a, a], policy())
        self.assertEqual(r.status, "FREEZE")

    def test_order_deterministic(self):
        a = cand("a", ("0.8", "0.9"), ("0.4", "0.7"))
        b = cand("b", ("0.6", "1"), ("0.8", "1"))
        x = select_proposal([a, b], policy())
        y = select_proposal([b, a], policy())
        self.assertEqual(x.fingerprint, y.fingerprint)
