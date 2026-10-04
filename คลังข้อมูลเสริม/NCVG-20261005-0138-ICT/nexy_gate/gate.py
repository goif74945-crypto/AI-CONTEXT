from __future__ import annotations

from typing import Any

from .canonical import sha256_hex
from .model import Finding, GateDecision
from .validator import validate_bundle_semantics


def evaluate_bundle(bundle: Any) -> GateDecision:
    """Evaluate a bundle without trusting caller-provided completion claims.

    Any canonicalization failure is converted into a deterministic FREEZE
    decision instead of propagating an optimistic or ambiguous result.
    """
    try:
        bundle_hash = sha256_hex(bundle)
    except (TypeError, ValueError, RecursionError) as exc:
        finding = Finding(
            code="BUNDLE_CANONICALIZATION_FAILED",
            path="$",
            message=f"Bundle cannot be canonicalized as JSON: {type(exc).__name__}",
            severity="ERROR",
        )
        return GateDecision(
            decision="FREEZE",
            status="FAIL",
            bundle_sha256="UNAVAILABLE",
            findings=(finding,),
            verified_requirements=(),
            total_mandatory_requirements=0,
        )

    findings, verified, mandatory_count = validate_bundle_semantics(bundle)
    blocking = tuple(f for f in findings if f.severity == "ERROR")
    complete = mandatory_count > 0 and len(verified) == mandatory_count

    if not blocking and complete:
        decision = "ALLOW"
        status = "PASS"
    else:
        decision = "FREEZE"
        status = "FAIL"

    return GateDecision(
        decision=decision,
        status=status,
        bundle_sha256=bundle_hash,
        findings=tuple(findings),
        verified_requirements=tuple(sorted(verified)),
        total_mandatory_requirements=mandatory_count,
    )
