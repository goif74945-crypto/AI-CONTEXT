from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .canonical import sha256_hex
from .model import (
    AuthorityState,
    BindingType,
    CapabilityManifest,
    Commitment,
    CommitmentState,
    Decision,
    Evaluation,
    EvidenceBundle,
    RevisionCheck,
    TemporalMode,
    TransitionResult,
)


_MODE_BINDING = {
    TemporalMode.IMMEDIATE: BindingType.INLINE_SESSION,
    TemporalMode.SCHEDULED: BindingType.SCHEDULED_TASK,
    TemporalMode.CONDITIONAL: BindingType.CONDITION_WATCH,
    TemporalMode.RECURRING: BindingType.RECURRING_TASK,
}

_TERMINAL = {
    CommitmentState.FULFILLED,
    CommitmentState.FAILED,
    CommitmentState.CANCELLED,
    CommitmentState.EXPIRED,
    CommitmentState.SUPERSEDED,
}


def _normalized_commitment_payload(commitment: Commitment) -> dict:
    return {
        "commitment_id": commitment.commitment_id,
        "revision": commitment.revision,
        "issuer": commitment.issuer,
        "beneficiary": commitment.beneficiary,
        "objective": commitment.objective,
        "deliverable": commitment.deliverable,
        "scope": sorted(set(commitment.scope), key=str.casefold),
        "protected_scope": sorted(set(commitment.protected_scope), key=str.casefold),
        "temporal_mode": commitment.temporal_mode,
        "effect": commitment.effect,
        "authority_state": commitment.authority_state,
        "authority_refs": sorted(set(commitment.authority_refs), key=str.casefold),
        "required_evidence": sorted(set(commitment.required_evidence), key=lambda x: x.value),
        "binding": commitment.binding,
        "trigger_spec": commitment.trigger_spec,
        "deadline_spec": commitment.deadline_spec,
        "supersedes_fingerprint": commitment.supersedes_fingerprint,
        "metadata": dict(commitment.metadata),
    }


def fingerprint(commitment: Commitment) -> str:
    return sha256_hex(_normalized_commitment_payload(commitment))


def _scope_intersects_protected(scope: Iterable[str], protected: Iterable[str]) -> bool:
    scope_set = {x.casefold().strip() for x in scope if x.strip()}
    protected_set = {x.casefold().strip() for x in protected if x.strip()}
    return bool(scope_set & protected_set)


def evaluate_commitment(commitment: Commitment, capabilities: CapabilityManifest) -> Evaluation:
    fp = fingerprint(commitment)
    reasons: list[str] = []

    if not commitment.commitment_id.strip():
        reasons.append("INVALID_COMMITMENT_ID")
    if commitment.revision < 1:
        reasons.append("INVALID_REVISION")
    if not commitment.issuer.strip() or not commitment.beneficiary.strip():
        reasons.append("MISSING_PARTY")
    if not commitment.objective.strip() or not commitment.deliverable.strip():
        reasons.append("MISSING_OBJECTIVE_OR_DELIVERABLE")
    if not commitment.scope:
        reasons.append("EMPTY_SCOPE")
    if not commitment.authority_refs:
        reasons.append("MISSING_AUTHORITY_PROVENANCE")
    if not commitment.binding.binding_ref.strip() or not commitment.binding.capability_proof_ref.strip():
        reasons.append("MISSING_EXECUTION_BINDING_PROOF")
    if _scope_intersects_protected(commitment.scope, commitment.protected_scope):
        reasons.append("PROTECTED_SCOPE_COLLISION")

    if reasons:
        return Evaluation(Decision.FREEZE, tuple(sorted(set(reasons))), fp)

    if commitment.authority_state is AuthorityState.CONFLICT:
        return Evaluation(Decision.FREEZE, ("AUTHORITY_CONFLICT",), fp)
    if commitment.authority_state is AuthorityState.UNRESOLVED:
        return Evaluation(Decision.ASK_AUTHORITY, ("AUTHORITY_UNRESOLVED",), fp)

    expected_binding = _MODE_BINDING[commitment.temporal_mode]
    if commitment.binding.binding_type is not expected_binding:
        return Evaluation(Decision.FREEZE, ("TEMPORAL_BINDING_MISMATCH",), fp)
    if expected_binding not in capabilities.supported_bindings:
        return Evaluation(Decision.FREEZE, ("EXECUTION_CAPABILITY_UNAVAILABLE",), fp)
    if commitment.temporal_mode is not TemporalMode.IMMEDIATE and not commitment.binding.durable:
        return Evaluation(Decision.FREEZE, ("FUTURE_COMMITMENT_NOT_DURABLE",), fp)
    if commitment.temporal_mode in {TemporalMode.CONDITIONAL, TemporalMode.RECURRING} and not (commitment.trigger_spec or "").strip():
        return Evaluation(Decision.FREEZE, ("MISSING_TRIGGER_SPEC",), fp)
    if commitment.temporal_mode is TemporalMode.SCHEDULED and not ((commitment.deadline_spec or "").strip() or (commitment.trigger_spec or "").strip()):
        return Evaluation(Decision.FREEZE, ("MISSING_SCHEDULE_SPEC",), fp)
    if commitment.effect not in capabilities.supported_effects:
        return Evaluation(Decision.FREEZE, ("EFFECT_CAPABILITY_UNAVAILABLE",), fp)

    missing_evidence = set(commitment.required_evidence) - set(capabilities.evidence_classes)
    if missing_evidence:
        return Evaluation(
            Decision.FREEZE,
            tuple("EVIDENCE_CAPABILITY_MISSING:" + x.value for x in sorted(missing_evidence, key=lambda x: x.value)),
            fp,
        )

    return Evaluation(Decision.ALLOW_COMMITMENT, ("COMMITMENT_BACKED_AND_AUTHORIZED",), fp)


def validate_revision(old: Commitment, new: Commitment) -> RevisionCheck:
    reasons: list[str] = []
    if new.commitment_id != old.commitment_id:
        reasons.append("COMMITMENT_ID_CHANGED")
    if new.revision != old.revision + 1:
        reasons.append("REVISION_NOT_MONOTONIC")
    if new.issuer != old.issuer:
        reasons.append("ISSUER_CHANGED")
    if new.beneficiary != old.beneficiary:
        reasons.append("BENEFICIARY_CHANGED")
    if new.supersedes_fingerprint != fingerprint(old):
        reasons.append("SUPERSEDES_FINGERPRINT_MISMATCH")
    if new.authority_state is not AuthorityState.RESOLVED:
        reasons.append("REVISED_AUTHORITY_NOT_RESOLVED")
    return RevisionCheck(not reasons, tuple(sorted(set(reasons))))


def transition(
    commitment: Commitment,
    current: CommitmentState,
    event: str,
    evidence: EvidenceBundle | None = None,
) -> TransitionResult:
    ev = event.upper().strip()
    if current in _TERMINAL:
        raise ValueError("TERMINAL_STATE_IMMUTABLE")

    if current is CommitmentState.DRAFT and ev == "ACCEPT":
        return TransitionResult(current, CommitmentState.ACCEPTED, "ACCEPTED")
    if current is CommitmentState.ACCEPTED and ev == "ACTIVATE":
        return TransitionResult(current, CommitmentState.ACTIVE, "ACTIVATED")
    if current in {CommitmentState.ACCEPTED, CommitmentState.ACTIVE, CommitmentState.BLOCKED} and ev == "CANCEL":
        return TransitionResult(current, CommitmentState.CANCELLED, "CANCELLED")
    if current in {CommitmentState.ACCEPTED, CommitmentState.ACTIVE, CommitmentState.BLOCKED} and ev == "EXPIRE":
        return TransitionResult(current, CommitmentState.EXPIRED, "EXPIRED")
    if current is CommitmentState.ACTIVE and ev == "BLOCK":
        return TransitionResult(current, CommitmentState.BLOCKED, "BLOCKED")
    if current is CommitmentState.BLOCKED and ev == "RESUME":
        return TransitionResult(current, CommitmentState.ACTIVE, "RESUMED")
    if current in {CommitmentState.ACTIVE, CommitmentState.BLOCKED} and ev == "FAIL":
        return TransitionResult(current, CommitmentState.FAILED, "FAILED")
    if current in {CommitmentState.ACCEPTED, CommitmentState.ACTIVE, CommitmentState.BLOCKED} and ev == "SUPERSEDE":
        return TransitionResult(current, CommitmentState.SUPERSEDED, "SUPERSEDED")
    if current is CommitmentState.ACTIVE and ev == "COMPLETE":
        _validate_completion_evidence(commitment, evidence)
        return TransitionResult(current, CommitmentState.FULFILLED, "FULFILLED_WITH_EVIDENCE")

    raise ValueError(f"ILLEGAL_TRANSITION:{current.value}:{ev}")


def _validate_completion_evidence(commitment: Commitment, evidence: EvidenceBundle | None) -> None:
    if evidence is None:
        raise ValueError("COMPLETION_EVIDENCE_REQUIRED")
    if evidence.result != "PASS":
        raise ValueError("COMPLETION_EVIDENCE_NOT_PASS")
    if evidence.target_fingerprint != fingerprint(commitment):
        raise ValueError("COMPLETION_EVIDENCE_TARGET_MISMATCH")
    if evidence.commitment_revision != commitment.revision:
        raise ValueError("COMPLETION_EVIDENCE_REVISION_MISMATCH")
    if not evidence.refs:
        raise ValueError("COMPLETION_EVIDENCE_REFS_REQUIRED")
    missing = set(commitment.required_evidence) - set(evidence.classes)
    if missing:
        raise ValueError("COMPLETION_EVIDENCE_CLASS_MISSING:" + ",".join(sorted(x.value for x in missing)))


def with_supersedes(old: Commitment, new: Commitment) -> Commitment:
    return replace(new, supersedes_fingerprint=fingerprint(old))
