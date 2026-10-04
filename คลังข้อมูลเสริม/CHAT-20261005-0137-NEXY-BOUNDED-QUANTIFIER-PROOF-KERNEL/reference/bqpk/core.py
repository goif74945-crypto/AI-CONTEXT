"""Deterministic bounded-quantifier proof evaluator.

The core is intentionally pure: no filesystem, network, clock, randomness,
environment, database, or process-state access.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

ENGINE_VERSION = "BQPK/0.1"
MAX_POPULATION = 10_000
VALID_QUANTIFIERS = frozenset({"ALL", "NONE", "EXACTLY", "AT_LEAST", "AT_MOST"})
COUNT_QUANTIFIERS = frozenset({"EXACTLY", "AT_LEAST", "AT_MOST"})
VALID_OUTCOMES = frozenset({"MATCH", "NO_MATCH", "UNKNOWN", "NOT_VERIFIED"})


def _nonblank_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fingerprint(document: Any) -> str | None:
    try:
        canonical = json.dumps(
            document,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError):
        return None
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def _base_result(
    *,
    fingerprint: str | None,
    claim_id: str | None,
    quantifier: str | None,
    status: str,
    action: str,
    decision: str,
    reason_codes: list[str],
    metrics: dict[str, Any] | None = None,
    missing_members: list[str] | None = None,
    stale_members: list[str] | None = None,
    counterexample_members: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "engine": ENGINE_VERSION,
        "status": status,
        "action": action,
        "decision": decision,
        "claim_id": claim_id,
        "quantifier": quantifier,
        "reason_codes": reason_codes,
        "metrics": metrics or {
            "population_size": 0,
            "match_count": 0,
            "no_match_count": 0,
            "unknown_count": 0,
            "not_verified_count": 0,
            "stale_count": 0,
            "missing_count": 0,
            "lower_bound_matches": 0,
            "upper_bound_matches": None,
            "upper_bound_kind": "UNAVAILABLE",
        },
        "missing_members": missing_members or [],
        "stale_members": stale_members or [],
        "counterexample_members": counterexample_members or [],
        "input_fingerprint": fingerprint,
    }


def _invalid(
    fingerprint: str | None,
    reason_codes: list[str],
    claim_id: str | None = None,
    quantifier: str | None = None,
) -> dict[str, Any]:
    return _base_result(
        fingerprint=fingerprint,
        claim_id=claim_id,
        quantifier=quantifier,
        status="FAIL",
        action="FREEZE",
        decision="INVALID",
        reason_codes=reason_codes,
    )


def evaluate_claim(document: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate whether supplied evidence entails a quantified claim.

    The function verifies structure, bounded-domain metadata, revision freshness,
    coverage, and quantifier logic. It does not verify that external evidence is
    truthful; callers must establish evidence authenticity separately.
    """

    fingerprint = _fingerprint(document)
    if not isinstance(document, Mapping):
        return _invalid(fingerprint, ["DOCUMENT_NOT_MAPPING"])
    if fingerprint is None:
        return _invalid(None, ["DOCUMENT_NOT_CANONICAL_JSON"])

    claim_id_value = document.get("claim_id")
    quantifier_value = document.get("quantifier")
    claim_id = claim_id_value if isinstance(claim_id_value, str) else None
    quantifier = quantifier_value if isinstance(quantifier_value, str) else None

    errors: list[str] = []

    if not _nonblank_string(claim_id_value):
        errors.append("INVALID_CLAIM_ID")
    if not _nonblank_string(document.get("predicate")):
        errors.append("INVALID_PREDICATE")
    if not isinstance(quantifier_value, str) or quantifier_value not in VALID_QUANTIFIERS:
        errors.append("INVALID_QUANTIFIER")
    target_revision = document.get("target_revision")
    if not _nonblank_string(target_revision):
        errors.append("INVALID_TARGET_REVISION")

    domain = document.get("domain")
    if not isinstance(domain, Mapping):
        errors.append("INVALID_DOMAIN")
        return _invalid(fingerprint, errors, claim_id, quantifier)

    population = domain.get("population")
    if not isinstance(population, list):
        errors.append("INVALID_POPULATION")
        return _invalid(fingerprint, errors, claim_id, quantifier)
    if len(population) == 0:
        errors.append("EMPTY_DOMAIN_FORBIDDEN")
    if len(population) > MAX_POPULATION:
        errors.append("DOMAIN_TOO_LARGE")
    population_members_valid = all(_nonblank_string(member) for member in population)
    if not population_members_valid:
        errors.append("INVALID_POPULATION_MEMBER")
    elif len(set(population)) != len(population):
        errors.append("DUPLICATE_POPULATION_MEMBER")

    enumeration = domain.get("enumeration")
    if not isinstance(enumeration, Mapping):
        errors.append("INVALID_ENUMERATION")
        complete = False
    else:
        complete_value = enumeration.get("complete")
        if not isinstance(complete_value, bool):
            errors.append("INVALID_ENUMERATION_COMPLETE")
            complete = False
        else:
            complete = complete_value
        if not _nonblank_string(enumeration.get("method")):
            errors.append("INVALID_ENUMERATION_METHOD")
        if not _nonblank_string(enumeration.get("evidence_ref")):
            errors.append("INVALID_ENUMERATION_EVIDENCE_REF")

    if isinstance(quantifier_value, str) and quantifier_value in COUNT_QUANTIFIERS:
        threshold = document.get("threshold")
        if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 0:
            errors.append("INVALID_THRESHOLD")
    else:
        threshold = None

    evidence = document.get("evidence")
    if not isinstance(evidence, list):
        errors.append("INVALID_EVIDENCE_LIST")
        return _invalid(fingerprint, errors, claim_id, quantifier)

    if errors:
        return _invalid(fingerprint, errors, claim_id, quantifier)

    population_set = set(population)
    evidence_by_member: dict[str, Mapping[str, Any]] = {}
    evidence_errors: list[str] = []

    for record in evidence:
        if not isinstance(record, Mapping):
            evidence_errors.append("INVALID_EVIDENCE_RECORD")
            continue
        member_id = record.get("member_id")
        if not _nonblank_string(member_id):
            evidence_errors.append("INVALID_EVIDENCE_MEMBER_ID")
            continue
        if member_id not in population_set:
            evidence_errors.append("EVIDENCE_MEMBER_OUTSIDE_DOMAIN")
            continue
        if member_id in evidence_by_member:
            evidence_errors.append("DUPLICATE_EVIDENCE_MEMBER")
            continue
        outcome_value = record.get("outcome")
        if not isinstance(outcome_value, str) or outcome_value not in VALID_OUTCOMES:
            evidence_errors.append("INVALID_EVIDENCE_OUTCOME")
            continue
        if not _nonblank_string(record.get("evidence_ref")):
            evidence_errors.append("INVALID_EVIDENCE_REF")
            continue
        if not _nonblank_string(record.get("target_revision")):
            evidence_errors.append("INVALID_EVIDENCE_REVISION")
            continue
        evidence_by_member[member_id] = record

    if evidence_errors:
        return _invalid(
            fingerprint,
            list(dict.fromkeys(evidence_errors)),
            claim_id,
            quantifier,
        )

    match_members: list[str] = []
    no_match_members: list[str] = []
    unknown_members: list[str] = []
    not_verified_members: list[str] = []
    stale_members: list[str] = []
    missing_members: list[str] = []

    for member_id in population:
        record = evidence_by_member.get(member_id)
        if record is None:
            missing_members.append(member_id)
            continue
        if record["target_revision"] != target_revision:
            stale_members.append(member_id)
            continue
        outcome = record["outcome"]
        if outcome == "MATCH":
            match_members.append(member_id)
        elif outcome == "NO_MATCH":
            no_match_members.append(member_id)
        elif outcome == "UNKNOWN":
            unknown_members.append(member_id)
        else:
            not_verified_members.append(member_id)

    unresolved_count = (
        len(unknown_members)
        + len(not_verified_members)
        + len(stale_members)
        + len(missing_members)
    )
    lower = len(match_members)
    upper = lower + unresolved_count if complete else None

    metrics = {
        "population_size": len(population),
        "match_count": len(match_members),
        "no_match_count": len(no_match_members),
        "unknown_count": len(unknown_members),
        "not_verified_count": len(not_verified_members),
        "stale_count": len(stale_members),
        "missing_count": len(missing_members),
        "lower_bound_matches": lower,
        "upper_bound_matches": upper,
        "upper_bound_kind": "FINITE" if complete else "UNBOUNDED",
    }

    unresolved_reasons: list[str] = []
    if not complete:
        unresolved_reasons.append("INCOMPLETE_ENUMERATION")
    if missing_members:
        unresolved_reasons.append("MISSING_EVIDENCE")
    if stale_members:
        unresolved_reasons.append("STALE_EVIDENCE")
    if unknown_members:
        unresolved_reasons.append("EVIDENCE_UNKNOWN")
    if not_verified_members:
        unresolved_reasons.append("EVIDENCE_NOT_VERIFIED")

    def proven(reason: str) -> dict[str, Any]:
        return _base_result(
            fingerprint=fingerprint,
            claim_id=claim_id,
            quantifier=quantifier,
            status="PASS",
            action="RELEASE",
            decision="PROVEN",
            reason_codes=[reason],
            metrics=metrics,
            missing_members=missing_members,
            stale_members=stale_members,
        )

    def refuted(reason: str, counterexamples: list[str] | None = None) -> dict[str, Any]:
        return _base_result(
            fingerprint=fingerprint,
            claim_id=claim_id,
            quantifier=quantifier,
            status="FAIL",
            action="FREEZE",
            decision="REFUTED",
            reason_codes=[reason],
            metrics=metrics,
            missing_members=missing_members,
            stale_members=stale_members,
            counterexample_members=counterexamples or [],
        )

    def insufficient(extra_reason: str | None = None) -> dict[str, Any]:
        reasons = list(unresolved_reasons)
        if extra_reason and extra_reason not in reasons:
            reasons.append(extra_reason)
        if not reasons:
            reasons.append("INSUFFICIENT_EVIDENCE")
        return _base_result(
            fingerprint=fingerprint,
            claim_id=claim_id,
            quantifier=quantifier,
            status="NOT_VERIFIED",
            action="FREEZE",
            decision="INSUFFICIENT_EVIDENCE",
            reason_codes=reasons,
            metrics=metrics,
            missing_members=missing_members,
            stale_members=stale_members,
        )

    if quantifier_value == "ALL":
        if no_match_members:
            return refuted("COUNTEREXAMPLE_TO_ALL", no_match_members)
        if complete and unresolved_count == 0 and lower == len(population):
            return proven("ALL_MEMBERS_PROVEN_MATCH")
        return insufficient("ALL_REQUIRES_CLOSED_FULL_COVERAGE")

    if quantifier_value == "NONE":
        if match_members:
            return refuted("COUNTEREXAMPLE_TO_NONE", match_members)
        if complete and upper == 0:
            return proven("ZERO_MATCHES_PROVEN_IN_CLOSED_DOMAIN")
        return insufficient("NONE_REQUIRES_ZERO_FINITE_UPPER_BOUND")

    assert isinstance(threshold, int) and not isinstance(threshold, bool)

    if quantifier_value == "EXACTLY":
        if lower > threshold:
            return refuted("LOWER_BOUND_EXCEEDS_EXACT", match_members[: threshold + 1])
        if upper is not None and upper < threshold:
            return refuted("FINITE_UPPER_BELOW_EXACT")
        if upper is not None and lower == threshold and upper == threshold:
            return proven("EXACT_COUNT_PROVEN")
        return insufficient("EXACT_COUNT_NOT_PINNED")

    if quantifier_value == "AT_LEAST":
        if lower >= threshold:
            return proven("LOWER_BOUND_MEETS_THRESHOLD")
        if upper is not None and upper < threshold:
            return refuted("FINITE_UPPER_BELOW_THRESHOLD")
        return insufficient("LOWER_BOUND_BELOW_THRESHOLD")

    if quantifier_value == "AT_MOST":
        if lower > threshold:
            return refuted("LOWER_BOUND_EXCEEDS_THRESHOLD", match_members[: threshold + 1])
        if upper is not None and upper <= threshold:
            return proven("FINITE_UPPER_WITHIN_THRESHOLD")
        return insufficient("FINITE_UPPER_REQUIRED")

    return _invalid(fingerprint, ["INVALID_QUANTIFIER"], claim_id, quantifier)
