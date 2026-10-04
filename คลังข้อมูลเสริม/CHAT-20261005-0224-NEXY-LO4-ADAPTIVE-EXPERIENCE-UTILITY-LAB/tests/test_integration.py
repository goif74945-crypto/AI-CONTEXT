import unittest

from aeul.comet import OverlapEvidence
from aeul.complexity import ChangeSurface, ComplexityWeights
from aeul.experiment import ExperimentPolicy, ExperimentProposal
from aeul.integration import run_innovation_capital_flow
from aeul.portfolio import PortfolioCandidate, PortfolioPolicy
from aeul.q64 import Q64
from aeul.regret import ProposalCandidate, RegretPolicy, UtilityInterval

q = Q64.from_decimal


class IntegrationTests(unittest.TestCase):
    def _base(self):
        utility = [
            ProposalCandidate("A", {"user_value": UtilityInterval(q("0.8"), q("0.9")), "reliability": UtilityInterval(q("0.7"), q("0.9"))}),
            ProposalCandidate("B", {"user_value": UtilityInterval(q("0.6"), q("1")), "reliability": UtilityInterval(q("0.8"), q("1"))}),
        ]
        regret_policy = RegretPolicy({"user_value": q("0.75"), "reliability": q("0.25")}, {"reliability": q("0.6")}, q("0.35"))
        overlaps = [
            OverlapEvidence("A", "B", q("0.9"), "ab"),
            OverlapEvidence("A", "C", q("0.1"), "ac"),
            OverlapEvidence("B", "C", q("0.1"), "bc"),
            OverlapEvidence("A", "legacy", q("0.2"), "al"),
        ]
        surfaces = [ChangeSurface("view-contract", q("0.4"), q("0.1"), q("0.1"), q("0.4"), q("0.2"))]
        cweights = ComplexityWeights(q("0.25"), q("0.25"), q("0.25"), q("0.25"))
        portfolio = [
            PortfolioCandidate("A", q("0.8"), q("0.3"), q("0.15"), frozenset({"control"})),
            PortfolioCandidate("B", q("0.75"), q("0.3"), q("0.15"), frozenset({"control"})),
            PortfolioCandidate("C", q("0.7"), q("0.3"), q("0.15"), frozenset({"ux"})),
        ]
        ppolicy = PortfolioPolicy(q("0.7"), q("0.4"), 2, 2, q("1"))
        pilot = ExperimentProposal("A", "VIEW_ONLY", q("0.8"), q("0.1"), q("0.1"), q("1"), q("0.1"), 100, "rollback:A", "stop:A")
        epolicy = ExperimentPolicy(q("0.2"), q("0.3"), q("0.3"), q("0.9"), 1000, q("0.2"), q("0.1"), q("0.4"), q("0.3"), q("0.3"))
        return dict(
            utility_candidates=utility, regret_policy=regret_policy,
            candidate_for_marginal="A", candidate_base_value=q("0.8"), already_selected=["legacy"],
            overlap_evidence=overlaps, max_allowed_overlap=q("0.5"),
            change_surfaces=surfaces, complexity_weights=cweights, max_total_tax=q("0.5"), max_surface_tax=q("0.5"),
            portfolio_candidates=portfolio, portfolio_policy=ppolicy,
            pilot_by_candidate={"A": pilot}, pilot_policy=epolicy,
        )

    def test_full_flow_ready_for_bounded_pilot_review(self):
        r = run_innovation_capital_flow(**self._base())
        self.assertEqual(r.regret.status, "SELECT")
        self.assertEqual(r.marginal.status, "VALUE")
        self.assertEqual(r.complexity.status, "PASS")
        self.assertEqual(r.portfolio.status, "SELECT")
        self.assertEqual(r.portfolio.selected_ids, ("A", "C"))
        self.assertEqual(r.pilot.status, "PLAN")
        self.assertEqual(r.status, "READY_FOR_BOUNDED_PILOT_REVIEW")

    def test_high_overlap_rejects_flow(self):
        data = self._base()
        data["overlap_evidence"] = [
            OverlapEvidence("A", "B", q("0.9"), "ab"),
            OverlapEvidence("A", "C", q("0.1"), "ac"),
            OverlapEvidence("B", "C", q("0.1"), "bc"),
            OverlapEvidence("A", "legacy", q("0.9"), "al"),
        ]
        r = run_innovation_capital_flow(**data)
        self.assertEqual(r.marginal.status, "COLLISION")
        self.assertEqual(r.status, "REJECT")

    def test_missing_overlap_freezes_flow(self):
        data = self._base()
        data["overlap_evidence"] = [OverlapEvidence("A", "legacy", q("0.2"), "al")]
        r = run_innovation_capital_flow(**data)
        self.assertEqual(r.portfolio.status, "FREEZE")
        self.assertEqual(r.status, "FREEZE")

    def test_flow_fingerprint_deterministic(self):
        x = run_innovation_capital_flow(**self._base())
        y = run_innovation_capital_flow(**self._base())
        self.assertEqual(x.fingerprint, y.fingerprint)
