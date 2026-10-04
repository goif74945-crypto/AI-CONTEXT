from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .compiler import compile_contract
from .frontier import satisfaction_frontier
from .recovery import plan_recovery
from .regression import benefit_regression_guard
from .verifier import verify_outcome


def run_outcome_pipeline(
    spec: dict[str, Any],
    *,
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
    alternatives: Sequence[Mapping[str, Any]],
    recovery_actions: Sequence[Mapping[str, Any]],
    max_cost: float,
    max_risk: float,
) -> dict[str, Any]:
    contract, contract_hash = compile_contract(spec)
    candidate_report = verify_outcome(contract, candidate)
    frontier = satisfaction_frontier(contract, alternatives)
    regression = benefit_regression_guard(contract, baseline, candidate)
    recovery = plan_recovery(
        contract,
        candidate,
        recovery_actions,
        max_cost=max_cost,
        max_risk=max_risk,
        require_reversible=True,
    )
    return {
        "contract_hash": contract_hash,
        "candidate_report": candidate_report,
        "frontier": frontier,
        "benefit_regression": regression,
        "recovery": recovery,
    }
