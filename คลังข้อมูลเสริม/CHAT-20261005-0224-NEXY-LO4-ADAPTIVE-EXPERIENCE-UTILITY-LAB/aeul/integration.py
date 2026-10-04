from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .comet import MarginalValueDecision, OverlapEvidence, evaluate_marginal_value
from .complexity import ChangeSurface, ComplexityDecision, ComplexityWeights, assess_complexity
from .experiment import ExperimentPlan, ExperimentPolicy, ExperimentProposal, plan_experiment
from .portfolio import PortfolioCandidate, PortfolioDecision, PortfolioPolicy, compose_portfolio
from .regret import ProposalCandidate, RegretDecision, RegretPolicy, select_proposal
from .common import fingerprint
from .q64 import Q64


@dataclass(frozen=True, slots=True)
class InnovationCapitalResult:
    regret: RegretDecision
    marginal: MarginalValueDecision
    complexity: ComplexityDecision
    portfolio: PortfolioDecision
    pilot: ExperimentPlan | None
    status: str
    fingerprint: str


def run_innovation_capital_flow(
    *,
    utility_candidates: Iterable[ProposalCandidate],
    regret_policy: RegretPolicy,
    candidate_for_marginal: str,
    candidate_base_value: Q64,
    already_selected: Iterable[str],
    overlap_evidence: Iterable[OverlapEvidence],
    max_allowed_overlap: Q64,
    change_surfaces: Iterable[ChangeSurface],
    complexity_weights: ComplexityWeights,
    max_total_tax: Q64,
    max_surface_tax: Q64,
    portfolio_candidates: Iterable[PortfolioCandidate],
    portfolio_policy: PortfolioPolicy,
    pilot_by_candidate: dict[str, ExperimentProposal],
    pilot_policy: ExperimentPolicy,
) -> InnovationCapitalResult:
    overlap_items = tuple(overlap_evidence)
    regret = select_proposal(utility_candidates, regret_policy)
    marginal = evaluate_marginal_value(
        candidate_id=candidate_for_marginal,
        base_value=candidate_base_value,
        selected_ids=already_selected,
        evidence=overlap_items,
        max_allowed_overlap=max_allowed_overlap,
    )
    complexity = assess_complexity(
        change_surfaces, weights=complexity_weights, max_total_tax=max_total_tax, max_surface_tax=max_surface_tax
    )
    portfolio = compose_portfolio(
        portfolio_candidates, overlap_evidence=overlap_items, policy=portfolio_policy
    )
    pilot = None
    if portfolio.status == "SELECT" and portfolio.selected_ids:
        # Pilot the selected member with highest explicit pilot option value candidate ordering supplied by map.
        for candidate_id in portfolio.selected_ids:
            proposal = pilot_by_candidate.get(candidate_id)
            if proposal is not None:
                pilot = plan_experiment(proposal, pilot_policy)
                break
    if regret.status == "FREEZE" or marginal.status == "FREEZE" or complexity.status == "FREEZE" or portfolio.status == "FREEZE":
        status = "FREEZE"
    elif marginal.status == "COLLISION" or complexity.status == "REJECT":
        status = "REJECT"
    elif portfolio.status != "SELECT":
        status = "HOLD"
    elif pilot is None:
        status = "PORTFOLIO_READY_NO_PILOT"
    elif pilot.status == "PLAN":
        status = "READY_FOR_BOUNDED_PILOT_REVIEW"
    else:
        status = "PORTFOLIO_READY_PILOT_HELD"
    core = {"regret": regret, "marginal": marginal, "complexity": complexity, "portfolio": portfolio, "pilot": pilot, "status": status}
    return InnovationCapitalResult(regret, marginal, complexity, portfolio, pilot, status, fingerprint(core))
