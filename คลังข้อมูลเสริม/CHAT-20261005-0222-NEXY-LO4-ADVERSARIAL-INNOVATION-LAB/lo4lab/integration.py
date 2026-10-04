from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any

from .aurora import AbstentionCase, AbstentionPolicy, evaluate_abstention
from .contract_drift import ContractDriftPolicy, analyze_contract_drift
from .margin import Constraint, evaluate_constraints
from .traceweight import InfluenceGraph
from .upa import EvidenceValue


@dataclass(frozen=True)
class Lo4ReleaseDecision:
    status: str
    blockers: tuple[str, ...]


def evaluate_lo4_release(
    *,
    abstention_cases: Iterable[AbstentionCase],
    abstention_policy: AbstentionPolicy,
    constraints: Iterable[Constraint],
    evidence_requirements: Iterable[EvidenceValue],
    influence_graph: InfluenceGraph,
    influence_target: str,
    before_contract: Mapping[str, Any],
    after_contract: Mapping[str, Any],
    contract_policy: ContractDriftPolicy = ContractDriftPolicy(),
) -> Lo4ReleaseDecision:
    blockers: list[str] = []

    aurora = evaluate_abstention(abstention_cases, abstention_policy)
    if aurora.status != "PASS":
        blockers.append("AURORA:" + ",".join(aurora.reasons))

    margin = evaluate_constraints(constraints)
    if margin.release_status != "RELEASE":
        blockers.append("MARGIN:" + margin.release_status)

    evidence = EvidenceValue.require_all(evidence_requirements)
    if not evidence.releaseable:
        blockers.append("UPA:" + evidence.state.value)

    influence = influence_graph.analyze(influence_target)
    if influence.status != "PASS":
        blockers.append("TRACEWEIGHT:" + ",".join(influence.reasons))

    drift = analyze_contract_drift(
        before_contract,
        after_contract,
        policy=contract_policy,
    )
    if drift.status != "PASS":
        blockers.append("CONTRACT_DRIFT:" + ",".join(drift.reasons))

    return Lo4ReleaseDecision(
        status="RELEASE_CANDIDATE" if not blockers else "FREEZE",
        blockers=tuple(blockers),
    )
