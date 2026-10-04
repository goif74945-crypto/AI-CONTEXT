from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .canonical import sha256

_ALLOWED_RULES = {"MUST_EQUAL", "REVERIFY_IF_DIFFERENT", "CAN_DIFFER"}


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    result["fingerprint"] = sha256(result)
    return result


def _parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamps must include timezone information")
    return dt.astimezone(timezone.utc)


def assess_portability(evidence: dict[str, Any], target: dict[str, Any], policy: dict[str, str]) -> dict[str, Any]:
    """Assess whether evidence can be carried to a target context without overclaiming.

    Every observed source/target context dimension must be governed by policy. This
    prevents a caller from obtaining PORTABLE merely by omitting a changed dimension.
    """
    if not all(isinstance(x, dict) for x in (evidence, target, policy)):
        raise ValueError("evidence, target, and policy must be objects")

    claim_id = evidence.get("claim_id")
    if not isinstance(claim_id, str) or not claim_id:
        raise ValueError("evidence.claim_id is required")
    if target.get("claim_id") != claim_id:
        return _finish({"status": "INVALID", "reason": "CLAIM_ID_MISMATCH", "claim_id": claim_id})

    source_class = evidence.get("evidence_class")
    required_classes = target.get("required_evidence_classes")
    if (
        not isinstance(source_class, str)
        or not source_class
        or not isinstance(required_classes, list)
        or not required_classes
        or any(not isinstance(x, str) or not x for x in required_classes)
    ):
        raise ValueError("evidence_class and non-empty string required_evidence_classes are required")
    if source_class not in required_classes:
        return _finish({
            "status": "INVALID",
            "reason": "EVIDENCE_CLASS_NOT_ACCEPTED",
            "claim_id": claim_id,
            "source_class": source_class,
            "required_classes": sorted(set(required_classes)),
        })

    source_ctx = evidence.get("source_context")
    target_ctx = target.get("target_context")
    if not isinstance(source_ctx, dict) or not isinstance(target_ctx, dict):
        raise ValueError("source_context and target_context must be objects")
    if any(not isinstance(k, str) or not k for k in source_ctx) or any(not isinstance(k, str) or not k for k in target_ctx):
        raise ValueError("context dimension names must be non-empty strings")

    context_dimensions = set(source_ctx) | set(target_ctx)
    policy_dimensions = set(policy)
    ungoverned = sorted(context_dimensions - policy_dimensions)
    if ungoverned:
        return _finish({
            "status": "FREEZE",
            "reason": "UNGOVERNED_PORTABILITY_DIMENSIONS",
            "claim_id": claim_id,
            "dimensions": ungoverned,
        })
    unknown_policy_dimensions = sorted(policy_dimensions - context_dimensions)
    if unknown_policy_dimensions:
        return _finish({
            "status": "FREEZE",
            "reason": "PORTABILITY_POLICY_DIMENSION_UNKNOWN",
            "claim_id": claim_id,
            "dimensions": unknown_policy_dimensions,
        })

    invalid: list[dict[str, Any]] = []
    reverify: list[dict[str, Any]] = []
    checked: list[dict[str, Any]] = []

    for dimension in sorted(policy):
        rule = policy[dimension]
        if rule not in _ALLOWED_RULES:
            raise ValueError(f"unknown portability rule for {dimension}: {rule}")
        if dimension not in source_ctx or dimension not in target_ctx:
            return _finish({
                "status": "FREEZE",
                "reason": "PORTABILITY_DIMENSION_UNKNOWN",
                "claim_id": claim_id,
                "dimension": dimension,
            })
        src = source_ctx[dimension]
        dst = target_ctx[dimension]
        same = src == dst
        checked.append({"dimension": dimension, "rule": rule, "same": same, "source": src, "target": dst})
        if not same and rule == "MUST_EQUAL":
            invalid.append({"dimension": dimension, "source": src, "target": dst})
        elif not same and rule == "REVERIFY_IF_DIFFERENT":
            reverify.append({"dimension": dimension, "source": src, "target": dst})

    evaluation_time_raw = target.get("evaluation_time")
    collected_at_raw = evidence.get("collected_at")
    expires_at_raw = evidence.get("expires_at")

    needs_time = collected_at_raw is not None or expires_at_raw is not None
    if needs_time and not isinstance(evaluation_time_raw, str):
        return _finish({"status": "FREEZE", "reason": "FRESHNESS_TIME_UNKNOWN", "claim_id": claim_id})

    evaluation_time = _parse_time(evaluation_time_raw) if isinstance(evaluation_time_raw, str) else None
    if collected_at_raw is not None:
        if not isinstance(collected_at_raw, str):
            return _finish({"status": "FREEZE", "reason": "COLLECTION_TIME_UNKNOWN", "claim_id": claim_id})
        if evaluation_time is not None and evaluation_time < _parse_time(collected_at_raw):
            return _finish({
                "status": "INVALID",
                "reason": "TEMPORAL_INCONSISTENCY",
                "claim_id": claim_id,
                "collected_at": collected_at_raw,
                "evaluation_time": evaluation_time_raw,
            })

    if expires_at_raw is not None:
        if not isinstance(expires_at_raw, str):
            return _finish({"status": "FREEZE", "reason": "EXPIRY_TIME_UNKNOWN", "claim_id": claim_id})
        if evaluation_time is not None and evaluation_time >= _parse_time(expires_at_raw):
            reverify.append({"dimension": "freshness", "source": expires_at_raw, "target": evaluation_time_raw})

    if invalid:
        status, reason = "INVALID", "NON_PORTABLE_CONTEXT"
    elif reverify:
        status, reason = "REVERIFY", "PARTIAL_PORTABILITY"
    else:
        status, reason = "PORTABLE", "PORTABILITY_PROVEN_BY_POLICY"

    return _finish({
        "status": status,
        "reason": reason,
        "claim_id": claim_id,
        "checked": checked,
        "invalid_dimensions": invalid,
        "reverify_dimensions": reverify,
    })
