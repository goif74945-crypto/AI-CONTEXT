import unittest

from aeul.comet import OverlapEvidence
from aeul.portfolio import PortfolioCandidate, PortfolioPolicy, compose_portfolio
from aeul.q64 import Q64

q = Q64.from_decimal


def c(i, value, cost="0.3", complexity="0.2", domains=("core",), requires=(), conflicts=()):
    return PortfolioCandidate(i, q(value), q(cost), q(complexity), frozenset(domains), frozenset(requires), frozenset(conflicts))


def overlaps():
    return [
        OverlapEvidence("A", "B", q("0.9"), "ab"),
        OverlapEvidence("A", "C", q("0.1"), "ac"),
        OverlapEvidence("B", "C", q("0.1"), "bc"),
    ]


def policy(**kwargs):
    data = dict(budget=q("0.7"), complexity_budget=q("0.5"), max_items=2, minimum_distinct_domains=2, pair_overlap_penalty_weight=q("1"))
    data.update(kwargs)
    return PortfolioPolicy(**data)


class PortfolioTests(unittest.TestCase):
    def test_selects_high_value_low_overlap_diverse_pair(self):
        items = [c("A", "0.8", domains=("core",)), c("B", "0.75", domains=("core",)), c("C", "0.7", domains=("ux",))]
        r = compose_portfolio(items, overlap_evidence=overlaps(), policy=policy())
        self.assertEqual(r.status, "SELECT")
        self.assertEqual(r.selected_ids, ("A", "C"))
        self.assertEqual(r.distinct_domains, ("core", "ux"))

    def test_missing_pairwise_overlap_freezes(self):
        items = [c("A", "0.8"), c("B", "0.7")]
        r = compose_portfolio(items, overlap_evidence=[], policy=PortfolioPolicy(q("1"), q("1"), 2, 1, q("1")))
        self.assertEqual(r.status, "FREEZE")
        self.assertTrue(r.reason.startswith("MISSING_PAIRWISE_OVERLAP"))

    def test_budget_can_make_portfolio_hold(self):
        items = [c("A", "0.8", cost="0.8"), c("B", "0.7", cost="0.8")]
        e = [OverlapEvidence("A", "B", q("0"), "ab")]
        r = compose_portfolio(items, overlap_evidence=e, policy=PortfolioPolicy(q("0.1"), q("1"), 2, 1, q("1")))
        self.assertEqual(r.status, "HOLD")

    def test_conflicting_candidates_not_selected_together(self):
        items = [c("A", "0.8", domains=("core",), conflicts=("B",)), c("B", "0.8", domains=("ux",), conflicts=("A",)), c("C", "0.6", domains=("ux",))]
        r = compose_portfolio(items, overlap_evidence=overlaps(), policy=policy())
        self.assertEqual(r.status, "SELECT")
        self.assertNotEqual(set(r.selected_ids), {"A", "B"})

    def test_dependency_must_be_in_subset_or_capability(self):
        items = [c("A", "0.8", requires=("B",)), c("B", "0.2")]
        e = [OverlapEvidence("A", "B", q("0"), "ab")]
        r = compose_portfolio(items, overlap_evidence=e, policy=PortfolioPolicy(q("1"), q("1"), 1, 1, q("1")))
        self.assertEqual(r.status, "SELECT")
        self.assertEqual(r.selected_ids, ("B",))

    def test_external_capability_satisfies_dependency(self):
        items = [c("A", "0.8", requires=("CAP",))]
        r = compose_portfolio(items, overlap_evidence=[], policy=PortfolioPolicy(q("1"), q("1"), 1, 1, q("1")), available_capabilities=frozenset({"CAP"}))
        self.assertEqual(r.selected_ids, ("A",))

    def test_reference_limit_freezes(self):
        items = [c(f"P{i}", "0.5") for i in range(19)]
        r = compose_portfolio(items, overlap_evidence=[], policy=PortfolioPolicy(q("10"), q("10"), 1, 1, q("1")))
        self.assertEqual(r.status, "FREEZE")
        self.assertEqual(r.reason, "REFERENCE_ENUMERATION_LIMIT_EXCEEDED")

    def test_order_deterministic(self):
        items = [c("A", "0.8", domains=("core",)), c("B", "0.75", domains=("core",)), c("C", "0.7", domains=("ux",))]
        a = compose_portfolio(items, overlap_evidence=overlaps(), policy=policy())
        b = compose_portfolio(reversed(items), overlap_evidence=reversed(overlaps()), policy=policy())
        self.assertEqual(a.fingerprint, b.fingerprint)
