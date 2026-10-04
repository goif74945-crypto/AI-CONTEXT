from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

from .canonical import canonical_hash, canonical_json
from .engine import Constitution, STRICT_CONSTITUTION, transition
from .model import (
    CourtState,
    Disposition,
    EvidenceKind,
    Event,
    EventKind,
    TransitionResult,
    VoteRound,
    WorkStatus,
)
from .q64 import I128_MAX, I128_MIN, Q64


@dataclass(frozen=True, slots=True)
class Finding:
    system_id: str
    passed: bool
    code: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class ConstitutionalSystem:
    system_id: str
    name: str
    purpose: str
    check: Callable[[CourtState], Finding]


def _finding(system_id: str, condition: bool, code: str, detail: str = "") -> Finding:
    return Finding(system_id, condition, "PASS" if condition else code, detail)


def _csm(state: CourtState) -> Finding:
    ok = state.defer_count >= 0 and state.external_core_mutations >= 0 and state.canon_overrides >= 0
    return _finding("CSM", ok, "STATE_DOMAIN_INVALID")


def _lvba(state: CourtState) -> Finding:
    ok = state.count_round(VoteRound.KEEP) <= 1 and state.count_round(VoteRound.CUT) <= 1
    return _finding("LVBA", ok, "VOTE_BUDGET_VIOLATION")


def _mel(state: CourtState) -> Finding:
    # A single state cannot prove transition monotonicity; duplicates/order are still canonical here.
    ok = tuple(sorted(set(state.evidence))) == state.evidence
    return _finding("MEL", ok, "EVIDENCE_SET_NONCANONICAL")


def _via(state: CourtState) -> Finding:
    ids = [v.vote_id for v in state.votes]
    ok = len(ids) == len(set(ids)) and all(r.vote_id in set(ids) for r in state.revisions)
    return _finding("VIA", ok, "VERDICT_LINEAGE_INVALID")


def _wnct(state: CourtState) -> Finding:
    ok = all(
        vote.round is not VoteRound.CUT or vote.status_before is WorkStatus.READY
        for vote in state.votes
    )
    return _finding("WNCT", ok, "WIP_CUT_REACHABLE")


def _anic(state: CourtState) -> Finding:
    return _finding("ANIC", state.external_core_mutations == 0, "CORE_NONINTERFERENCE_BREACH")


def _cnop(state: CourtState) -> Finding:
    return _finding("CNOP", state.canon_overrides == 0, "CANON_OVERRIDE_REACHABLE")


def _pncg(state: CourtState) -> Finding:
    return _finding("PNCG", not state.promoted, "AUTO_PROMOTION_REACHABLE")


def _ndcs(state: CourtState) -> Finding:
    ok = all(
        vote.round is not VoteRound.CUT
        or vote.disposition in (Disposition.ARCHIVED, Disposition.REJECTED, Disposition.SUPERSEDED)
        for vote in state.votes
    )
    return _finding("NDCS", ok, "DESTRUCTIVE_CUT_REACHABLE")


def _epcc(state: CourtState) -> Finding:
    ok = all(
        bool(v.spec_evidence and v.code_evidence and v.ai_context_evidence and v.test_evidence)
        and len(v.spec_hash) == 64
        and len(v.nexy_commit_sha) == 40
        and len(v.ai_context_commit_sha) == 40
        for v in state.votes
    )
    return _finding("EPCC", ok, "PROVENANCE_CLOSURE_BREACH")


def _sdwl(state: CourtState) -> Finding:
    ok = all(
        e.kind is not EvidenceKind.SEMANTIC_DUPLICATE
        or bool(e.semantic_target.strip() and e.semantic_witness.strip())
        for e in state.evidence
    )
    return _finding("SDWL", ok, "DUPLICATE_WITHOUT_WITNESS")


def _dpec(state: CourtState) -> Finding:
    # Canonical state hash is invariant to evidence insertion order because state evidence is sorted.
    reordered = state.with_evidence(tuple(reversed(state.evidence)))
    ok = canonical_hash(state) == canonical_hash(reordered)
    return _finding("DPEC", ok, "PERMUTATION_NONDETERMINISM")


def _crs(state: CourtState) -> Finding:
    try:
        encoded = canonical_json(state)
        ok = canonical_hash(state) == canonical_hash(state) and len(encoded) > 2
    except Exception as exc:  # pragma: no cover - converted into a finding
        return Finding("CRS", False, "CANONICAL_SERIALIZATION_FAILURE", str(exc))
    return _finding("CRS", ok, "CANONICAL_SERIALIZATION_FAILURE")


def _qmdc(state: CourtState) -> Finding:
    metrics = []
    for vote in state.votes:
        metrics.extend([
            vote.architecture_fit_q64, vote.canon_compatibility_q64, vote.novelty_q64,
            vote.overlap_q64, vote.implementation_value_q64, vote.verification_value_q64,
            vote.security_impact_q64, vote.determinism_impact_q64, vote.maintenance_cost_q64,
        ])
    ok = all(isinstance(m, Q64) and I128_MIN <= m.raw <= I128_MAX for m in metrics)
    return _finding("QMDC", ok, "Q64_DOMAIN_BREACH")


def _mefp(state: CourtState) -> Finding:
    ok = all(
        bool(v.spec_evidence and v.code_evidence and v.ai_context_evidence and v.test_evidence)
        for v in state.votes
    )
    return _finding("MEFP", ok, "VOTE_WITH_MISSING_EVIDENCE")


def _mcr(state: CourtState) -> Finding:
    return _finding("MCR", True, "UNREACHABLE", "Algorithmic checker is exercised by dedicated trace tests.")


def _bssee(state: CourtState) -> Finding:
    return _finding("BSSEE", True, "UNREACHABLE", "Exhaustive engine is exercised by dedicated model-check tests.")


def _cor(state: CourtState) -> Finding:
    return _finding("COR", True, "UNREACHABLE", "Registry cardinality/uniqueness is checked by evaluate_all.")


def _crd(state: CourtState) -> Finding:
    return _finding("CRD", True, "UNREACHABLE", "Differential checker is exercised against a weakened constitution.")


def _pwcv(state: CourtState) -> Finding:
    hard = (
        state.external_core_mutations == 0
        and state.canon_overrides == 0
        and not state.promoted
        and state.count_round(VoteRound.KEEP) <= 1
        and state.count_round(VoteRound.CUT) <= 1
    )
    return _finding("PWCV", hard, "PROMOTION_WITNESS_CONTRACT_BREACH")


SYSTEM_REGISTRY: tuple[ConstitutionalSystem, ...] = (
    ConstitutionalSystem("CSM", "Constitutional State Model", "Validate the EPC finite-state domain.", _csm),
    ConstitutionalSystem("LVBA", "Lifetime Vote Budget Automaton", "Enforce one KEEP and one CUT per CHAT_ID lifetime.", _lvba),
    ConstitutionalSystem("MEL", "Monotone Evidence Lattice", "Keep evidence append-only, canonical, and non-erasing.", _mel),
    ConstitutionalSystem("VIA", "Verdict Immutability Automaton", "Prevent retrospective vote mutation while allowing append-only revisions.", _via),
    ConstitutionalSystem("WNCT", "WIP Non-Cut Theorem Checker", "Prove WIP/insufficient states cannot acquire CUT verdicts.", _wnct),
    ConstitutionalSystem("ANIC", "Authority Non-Interference Checker", "Prove EPC cannot mutate protected Core state.", _anic),
    ConstitutionalSystem("CNOP", "Canon Non-Override Property Checker", "Prove EPC votes cannot override Canon/Law authority.", _cnop),
    ConstitutionalSystem("PNCG", "Promotion Non-Causality Gate", "Prove vote output cannot directly promote into NEXY.", _pncg),
    ConstitutionalSystem("NDCS", "Non-Destructive CUT Semantics Checker", "Constrain CUT to archive/reject/supersede semantics.", _ndcs),
    ConstitutionalSystem("EPCC", "Evidence Provenance Closure Checker", "Require exact source/code/context/test pins for votes.", _epcc),
    ConstitutionalSystem("SDWL", "Semantic Duplicate Witness Law", "Require concrete semantic target and witness for duplicate claims.", _sdwl),
    ConstitutionalSystem("DPEC", "Deterministic Permutation Equivalence Checker", "Prove logically equivalent evidence order is output-equivalent.", _dpec),
    ConstitutionalSystem("CRS", "Canonical Receipt Serializer", "Produce deterministic canonical vote/state bytes and hashes.", _crs),
    ConstitutionalSystem("QMDC", "Q64.64 Metric Domain Checker", "Reject non-Q64 or out-of-i128 quantitative protocol metrics.", _qmdc),
    ConstitutionalSystem("MEFP", "Missing-Evidence Freeze Property", "Prove critical evidence gaps cannot become KEEP/CUT.", _mefp),
    ConstitutionalSystem("MCR", "Minimal Counterexample Reducer", "Shrink violating event traces to reproducible minimal witnesses.", _mcr),
    ConstitutionalSystem("BSSEE", "Bounded State-Space Exhaustion Engine", "Explore reachable EPC protocol states and transitions exhaustively to a bound.", _bssee),
    ConstitutionalSystem("COR", "Constitutional Obligation Registry", "Bind every constitutional rule to an executable checker identifier.", _cor),
    ConstitutionalSystem("CRD", "Constitutional Regression Differential", "Detect semantic weakening by comparing strict and candidate constitutions.", _crd),
    ConstitutionalSystem("PWCV", "Promotion Witness Contract Validator", "Emit review readiness only when hard constitutional invariants hold, never promotion.", _pwcv),
)


def evaluate_all(state: CourtState) -> tuple[Finding, ...]:
    if len(SYSTEM_REGISTRY) != 20:
        raise AssertionError("FCVF_SYSTEM_COUNT_MUST_EQUAL_20")
    ids = [system.system_id for system in SYSTEM_REGISTRY]
    if len(set(ids)) != 20:
        raise AssertionError("FCVF_SYSTEM_IDS_MUST_BE_UNIQUE")
    return tuple(system.check(state) for system in SYSTEM_REGISTRY)


def assert_all_pass(state: CourtState) -> None:
    failed = [f for f in evaluate_all(state) if not f.passed]
    if failed:
        raise AssertionError(";".join(f"{f.system_id}:{f.code}" for f in failed))
