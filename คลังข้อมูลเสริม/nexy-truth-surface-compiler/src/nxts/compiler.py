from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import sha256_hex
from .model import (
    ALLOWED_STATUSES,
    BLOCKING_STATUSES,
    FACT_STATUSES,
    MAX_CLAIMS,
    UNCERTAINTY_STATUSES,
    Claim,
)
from .redaction import redact_text

COMPILER_VERSION = "0.2.0"
SCHEMA_VERSION = "nxts.result-capsule.v0"
MAX_OBJECTIVE_CHARS = 4096
MAX_REQUEST_ID_CHARS = 256


class ValidationError(ValueError):
    pass


def _validate_payload(payload: Any) -> tuple[str, str, list[Claim]]:
    if not isinstance(payload, dict):
        raise ValidationError("payload must be a JSON object")

    request_id = payload.get("request_id")
    objective = payload.get("objective")
    claims_raw = payload.get("claims")

    if not isinstance(request_id, str) or not request_id.strip():
        raise ValidationError("request_id must be a non-empty string")
    if len(request_id) > MAX_REQUEST_ID_CHARS:
        raise ValidationError(f"request_id exceeds {MAX_REQUEST_ID_CHARS} characters")
    if not isinstance(objective, str) or not objective.strip():
        raise ValidationError("objective must be a non-empty string")
    if len(objective) > MAX_OBJECTIVE_CHARS:
        raise ValidationError(f"objective exceeds {MAX_OBJECTIVE_CHARS} characters")
    if not isinstance(claims_raw, list) or not claims_raw:
        raise ValidationError("claims must be a non-empty list")
    if len(claims_raw) > MAX_CLAIMS:
        raise ValidationError(f"claims exceeds maximum of {MAX_CLAIMS}")

    claims: list[Claim] = []
    seen: set[str] = set()
    for item in claims_raw:
        if not isinstance(item, dict):
            raise ValidationError("each claim must be an object")
        try:
            claim = Claim.from_mapping(item)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        if claim.claim_id in seen:
            raise ValidationError(f"duplicate claim id: {claim.claim_id}")
        seen.add(claim.claim_id)
        claims.append(claim)

    claims.sort(key=lambda c: c.claim_id)
    return request_id.strip(), objective.strip(), claims


def _normalized_input(request_id: str, objective: str, claims: list[Claim]) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "objective": objective,
        "claims": [
            {
                "id": c.claim_id,
                "text": c.text,
                "status": c.status,
                "materiality": c.materiality,
                "visibility": c.visibility,
                "evidence_refs": list(c.evidence_refs),
            }
            for c in claims
        ],
    }


def _reason(code: str, claim: Claim, detail: str) -> dict[str, str]:
    return {
        "code": code,
        "claim_id": redact_text(claim.claim_id) if claim.visibility == "PUBLIC" else "[WITHHELD]",
        "detail": redact_text(detail),
    }


def compile_payload(payload: Any) -> dict[str, Any]:
    request_id, objective, claims = _validate_payload(payload)
    normalized_input = _normalized_input(request_id, objective, claims)

    facts: list[dict[str, Any]] = []
    uncertainties: list[dict[str, Any]] = []
    freeze_reasons: list[dict[str, str]] = []
    public_evidence_set: set[str] = set()

    for claim in claims:
        status = claim.status

        if status not in ALLOWED_STATUSES:
            freeze_reasons.append(_reason(
                "UNKNOWN_STATUS",
                claim,
                f"Claim status {status!r} is not recognized; fail-closed release policy applied.",
            ))
            continue

        if status in BLOCKING_STATUSES and claim.materiality == "MATERIAL":
            freeze_reasons.append(_reason(
                f"MATERIAL_{status}",
                claim,
                f"Material claim is {status}; verified release is not allowed.",
            ))

        if status in FACT_STATUSES and claim.materiality == "MATERIAL" and not claim.evidence_refs:
            freeze_reasons.append(_reason(
                "MATERIAL_FACT_WITHOUT_EVIDENCE",
                claim,
                "Material fact has no evidence reference.",
            ))

        if claim.visibility != "PUBLIC":
            continue

        safe_refs = [redact_text(ref) for ref in claim.evidence_refs]
        public_evidence_set.update(safe_refs)
        safe_text = redact_text(claim.text)
        safe_id = redact_text(claim.claim_id)

        if status in FACT_STATUSES:
            facts.append({
                "claim_id": safe_id,
                "text": safe_text,
                "status": status,
                "evidence_refs": safe_refs,
            })
        elif status in UNCERTAINTY_STATUSES or status in BLOCKING_STATUSES:
            uncertainties.append({
                "claim_id": safe_id,
                "text": safe_text,
                "status": status,
                "materiality": claim.materiality,
            })

    freeze_reasons.sort(key=lambda r: (r["code"], r["claim_id"], r["detail"]))
    facts.sort(key=lambda x: x["claim_id"])
    uncertainties.sort(key=lambda x: x["claim_id"])

    decision = "FREEZE" if freeze_reasons else "RELEASE"
    summary = (
        "Verified result is releasable under the prototype truth-surface rules."
        if decision == "RELEASE"
        else f"Release frozen by {len(freeze_reasons)} material truth/integrity condition(s)."
    )

    capsule: dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "request_id": redact_text(request_id),
        "objective": redact_text(objective),
        "decision": decision,
        "summary": summary,
        "facts": facts,
        "uncertainties": uncertainties,
        "freeze_reasons": freeze_reasons,
        "evidence_refs": sorted(public_evidence_set),
        "receipt": {
            "compiler_version": COMPILER_VERSION,
            "input_sha256": sha256_hex(normalized_input),
        },
    }

    digest_view = deepcopy(capsule)
    capsule["receipt"]["output_sha256"] = sha256_hex(digest_view)
    return capsule


def validate_output_digest(capsule: dict[str, Any]) -> bool:
    if not isinstance(capsule, dict):
        return False
    receipt = capsule.get("receipt")
    if not isinstance(receipt, dict):
        return False
    expected = receipt.get("output_sha256")
    if not isinstance(expected, str):
        return False
    digest_view = deepcopy(capsule)
    digest_view.get("receipt", {}).pop("output_sha256", None)
    return sha256_hex(digest_view) == expected
