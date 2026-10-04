from __future__ import annotations

from dataclasses import dataclass, replace
import re

from .model import (
    CourtPins,
    CourtState,
    Disposition,
    EvidenceKind,
    EvidenceRef,
    Event,
    EventKind,
    TransitionResult,
    VoteRecord,
    VoteRevision,
    VoteRound,
    WorkStatus,
)
from .q64 import Q64


_RFC3339ISH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})$")


@dataclass(frozen=True, slots=True)
class Constitution:
    max_keep: int = 1
    max_cut: int = 1
    require_complete_evidence: bool = True
    cut_requires_ready: bool = True
    verdict_immutable: bool = True
    allow_promotion: bool = False
    allow_core_mutation: bool = False
    allow_canon_override: bool = False
    destructive_cut_allowed: bool = False
    duplicate_witness_required: bool = True


STRICT_CONSTITUTION = Constitution()


def initial_state(
    *,
    chat_id: str,
    candidate_id: str,
    candidate_path: str,
    pins: CourtPins,
) -> CourtState:
    if not chat_id.strip() or not candidate_id.strip() or not candidate_path.strip():
        raise ValueError("COURT_IDENTITY_REQUIRED")
    pins.validate()
    return CourtState(
        chat_id=chat_id,
        candidate_id=candidate_id,
        candidate_path=candidate_path,
        pins=pins,
    )


def _block(state: CourtState, code: str) -> TransitionResult:
    return TransitionResult(state=state, accepted=False, code=code)


def _accept(state: CourtState, code: str) -> TransitionResult:
    return TransitionResult(state=state, accepted=True, code=code)


def _evidence_locators(state: CourtState, kind: EvidenceKind) -> tuple[str, ...]:
    return tuple(sorted(e.locator for e in state.evidence if e.kind is kind))


def _score_vectors(state: CourtState) -> tuple[Q64, ...]:
    coverage = state.evidence_coverage_q64()
    zero = Q64.zero()
    # These are protocol-integrity metrics, not proposal-quality authority.
    return (
        coverage,  # architecture fit proxy = evidence-bound protocol fit
        Q64.one(),  # canon compatibility is binary only after forbidden paths remain unreachable
        zero,  # novelty is deliberately not an FCVF decision criterion
        zero,  # overlap is deliberately not an FCVF decision criterion
        coverage,  # implementation value proxy from executed evidence coverage
        coverage,  # verification value
        Q64.one(),  # security impact: no privilege path accepted
        Q64.one(),  # determinism impact: deterministic engine contract
        zero,  # maintenance cost is not guessed by the protocol engine
    )


def _make_vote(state: CourtState, event: Event, round_: VoteRound) -> VoteRecord:
    if not event.vote_id.strip():
        raise ValueError("VOTE_ID_REQUIRED")
    if not _RFC3339ISH.match(event.timestamp):
        raise ValueError("VOTE_TIMESTAMP_INVALID")
    if not event.reason.strip() or not event.final_justification.strip():
        raise ValueError("VOTE_JUSTIFICATION_REQUIRED")
    scores = _score_vectors(state)
    duplicates = tuple(sorted(e.semantic_target for e in state.evidence if e.kind is EvidenceKind.SEMANTIC_DUPLICATE))
    disposition = Disposition.ACTIVE if round_ is VoteRound.KEEP else event.requested_disposition
    return VoteRecord(
        vote_id=event.vote_id,
        chat_id=state.chat_id,
        round=round_,
        timestamp=event.timestamp,
        spec_id=state.pins.spec_id,
        spec_hash=state.pins.spec_hash,
        nexy_repo=state.pins.nexy_repo,
        nexy_branch=state.pins.nexy_branch,
        nexy_commit_sha=state.pins.nexy_commit_sha,
        ai_context_commit_sha=state.pins.ai_context_commit_sha,
        candidate_id=state.candidate_id,
        candidate_path=state.candidate_path,
        status_before=state.status,
        verdict=round_.value,
        spec_evidence=_evidence_locators(state, EvidenceKind.SPEC),
        code_evidence=_evidence_locators(state, EvidenceKind.CODE),
        ai_context_evidence=_evidence_locators(state, EvidenceKind.AI_CONTEXT),
        test_evidence=_evidence_locators(state, EvidenceKind.TEST),
        architecture_fit_q64=scores[0],
        canon_compatibility_q64=scores[1],
        novelty_q64=scores[2],
        overlap_q64=scores[3],
        implementation_value_q64=scores[4],
        verification_value_q64=scores[5],
        security_impact_q64=scores[6],
        determinism_impact_q64=scores[7],
        maintenance_cost_q64=scores[8],
        conflicts=(),
        duplicates=duplicates,
        dependencies=tuple(sorted(e.locator for e in state.evidence if e.kind is EvidenceKind.DEPENDENCY)),
        fact=("vote derived from exact pinned evidence",),
        assumption=(),
        unknown=(),
        reason=event.reason,
        counterargument=event.counterargument,
        final_justification=event.final_justification,
        disposition=disposition,
    )


def transition(
    state: CourtState,
    event: Event,
    constitution: Constitution = STRICT_CONSTITUTION,
) -> TransitionResult:
    if event.kind is EventKind.SET_STATUS:
        if event.status is None:
            return _block(state, "STATUS_REQUIRED")
        return _accept(replace(state, status=event.status), "STATUS_SET")

    if event.kind is EventKind.ATTACH_EVIDENCE:
        if event.evidence is None:
            return _block(state, "EVIDENCE_REQUIRED")
        try:
            event.evidence.validate()
        except ValueError as exc:
            return _block(state, str(exc))
        return _accept(state.with_evidence((event.evidence,)), "EVIDENCE_ATTACHED")

    if event.kind is EventKind.CLAIM_DUPLICATE:
        if constitution.duplicate_witness_required and (
            not event.semantic_target.strip() or not event.semantic_witness.strip()
        ):
            return _block(state, "SEMANTIC_DUPLICATE_WITNESS_REQUIRED")
        # A duplicate claim is evidence, not an authority-bearing verdict.
        return _accept(state, "SEMANTIC_DUPLICATE_WITNESS_ACCEPTED")

    if event.kind is EventKind.DEFER:
        return _accept(replace(state, defer_count=state.defer_count + 1), "DEFER_RECORDED")

    if event.kind in (EventKind.KEEP, EventKind.CUT):
        round_ = VoteRound.KEEP if event.kind is EventKind.KEEP else VoteRound.CUT
        limit = constitution.max_keep if round_ is VoteRound.KEEP else constitution.max_cut
        if state.count_round(round_) >= limit:
            return _block(state, f"{round_.value}_RIGHT_EXHAUSTED")
        if constitution.require_complete_evidence and not state.required_evidence_complete():
            return _block(state, "CRITICAL_EVIDENCE_INCOMPLETE")
        if round_ is VoteRound.CUT and constitution.cut_requires_ready and state.status is not WorkStatus.READY:
            return _block(state, "WIP_OR_INSUFFICIENT_CUT_FORBIDDEN")
        if round_ is VoteRound.CUT:
            if event.requested_disposition not in (
                Disposition.ARCHIVED,
                Disposition.REJECTED,
                Disposition.SUPERSEDED,
            ):
                return _block(state, "CUT_DISPOSITION_INVALID")
            if constitution.destructive_cut_allowed:
                # Kept for regression modeling only; strict law never enables this flag.
                pass
        try:
            vote = _make_vote(state, event, round_)
        except ValueError as exc:
            return _block(state, str(exc))
        new_disposition = state.disposition if round_ is VoteRound.KEEP else vote.disposition
        return _accept(
            replace(state, votes=(*state.votes, vote), disposition=new_disposition),
            f"{round_.value}_RECORDED",
        )

    if event.kind is EventKind.REVISE_VOTE:
        vote = next((v for v in state.votes if v.vote_id == event.target_vote_id), None)
        if vote is None:
            return _block(state, "REVISION_TARGET_NOT_FOUND")
        if not event.revision_id.strip():
            return _block(state, "REVISION_ID_REQUIRED")
        if constitution.verdict_immutable and event.reason.startswith("CHANGE_VERDICT:"):
            return _block(state, "VERDICT_IMMUTABLE")
        revision = VoteRevision(
            revision_id=event.revision_id,
            vote_id=vote.vote_id,
            appended_evidence=tuple(sorted(e.locator for e in state.evidence)),
            note=event.note,
        )
        return _accept(replace(state, revisions=(*state.revisions, revision)), "REVISION_APPENDED")

    if event.kind is EventKind.ATTEMPT_PROMOTION:
        if not constitution.allow_promotion:
            return _block(state, "PROMOTION_AUTHORITY_FORBIDDEN")
        return _accept(replace(state, promoted=True), "PROMOTION_ACCEPTED_WEAK_MODEL")

    if event.kind is EventKind.ATTEMPT_CORE_MUTATION:
        if not constitution.allow_core_mutation:
            return _block(state, "CORE_MUTATION_FORBIDDEN")
        return _accept(
            replace(state, external_core_mutations=state.external_core_mutations + 1),
            "CORE_MUTATION_ACCEPTED_WEAK_MODEL",
        )

    if event.kind is EventKind.ATTEMPT_CANON_OVERRIDE:
        if not constitution.allow_canon_override:
            return _block(state, "CANON_OVERRIDE_FORBIDDEN")
        return _accept(
            replace(state, canon_overrides=state.canon_overrides + 1),
            "CANON_OVERRIDE_ACCEPTED_WEAK_MODEL",
        )

    return _block(state, "UNKNOWN_EVENT")
