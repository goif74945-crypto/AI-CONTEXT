from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from c1_interpretation_convergence.implementation import Interpretation, evaluate_convergence
from c2_context_noninterference.implementation import MutationSet, verify_noninterference
from c3_evidence_acquisition.implementation import ClaimNeed, Probe, plan_evidence_acquisition
from c4_resume_equivalence.implementation import ResumeState, compile_capsule, verify_resume_equivalence
from c5_independent_evidence_quorum.implementation import (
    EvidenceRecord,
    QuorumNeed,
    evaluate_independent_quorum,
)
from shared import GateResult, sha256_hex


@dataclass(frozen=True)
class MeshInput:
    interpretations: tuple[Interpretation, ...]
    baseline_context: Mapping[str, Any]
    excluded_mutations: tuple[MutationSet, ...]
    evidence_needs: tuple[ClaimNeed, ...]
    probes: tuple[Probe, ...]
    available_prerequisites: frozenset[str]
    resume_state: ResumeState
    quorum_need: QuorumNeed
    evidence_records: tuple[EvidenceRecord, ...]


def assess_mesh(
    data: MeshInput,
    *,
    interpretation_evaluator: Callable[[Interpretation], Any],
    context_decision_fn: Callable[[Mapping[str, Any]], Any],
    next_action_fn: Callable[[Mapping[str, Any]], Any],
) -> GateResult:
    """Run the auxiliary mesh. This is advisory preflight; it is not NEXY::JUDGE."""
    stages: list[dict[str, Any]] = []

    convergence = evaluate_convergence(data.interpretations, interpretation_evaluator)
    stages.append({"stage": "interpretation_convergence", "status": convergence.status, "reason": convergence.reason})
    if convergence.status != "RELEASE":
        return GateResult("FREEZE", "MESH_STAGE_BLOCKED", {"blocked_stage": stages[-1], "stages": stages})

    noninterference = verify_noninterference(
        data.baseline_context, data.excluded_mutations, context_decision_fn
    )
    stages.append({"stage": "context_noninterference", "status": noninterference.status, "reason": noninterference.reason})
    if noninterference.status != "PASS":
        return GateResult("FREEZE", "MESH_STAGE_BLOCKED", {"blocked_stage": stages[-1], "stages": stages})

    plan = plan_evidence_acquisition(
        data.evidence_needs,
        data.probes,
        available_prerequisites=data.available_prerequisites,
    )
    stages.append({"stage": "evidence_acquisition", "status": plan.status, "reason": plan.reason})
    if plan.status != "PLANNED":
        return GateResult("FREEZE", "MESH_STAGE_BLOCKED", {"blocked_stage": stages[-1], "stages": stages})

    quorum = evaluate_independent_quorum(data.quorum_need, data.evidence_records)
    stages.append({"stage": "independent_evidence_quorum", "status": quorum.status, "reason": quorum.reason})
    if quorum.status != "PASS":
        return GateResult("FREEZE", "MESH_STAGE_BLOCKED", {"blocked_stage": stages[-1], "stages": stages})

    capsule = compile_capsule(data.resume_state, next_action_fn)
    resume = verify_resume_equivalence(capsule, data.resume_state, next_action_fn)
    stages.append({"stage": "resume_equivalence", "status": resume.status, "reason": resume.reason})
    if resume.status != "VERIFIED":
        return GateResult("FREEZE", "MESH_STAGE_BLOCKED", {"blocked_stage": stages[-1], "stages": stages})

    evidence_bundle = {
        "convergence_hash": convergence.details.get("decision_hash"),
        "noninterference_hash": noninterference.details.get("baseline_hash"),
        "evidence_plan_hash": plan.details.get("plan_hash"),
        "quorum_hash": quorum.details.get("quorum_hash"),
        "resume_capsule_hash": capsule["capsule_hash"],
    }
    return GateResult(
        "READY",
        "AUXILIARY_MESH_CHECKS_SATISFIED",
        {
            "classification": "AI_PROPOSED_ADVISORY_PREFLIGHT_NOT_NEXY_JUDGE",
            "stages": stages,
            "evidence_bundle": evidence_bundle,
            "mesh_witness_hash": sha256_hex({"stages": stages, "evidence_bundle": evidence_bundle}),
        },
    )
