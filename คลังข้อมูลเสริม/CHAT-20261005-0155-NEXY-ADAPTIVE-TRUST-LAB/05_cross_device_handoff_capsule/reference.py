from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

_ALLOWED_FIELDS = {
    "objective", "authority_sources", "verified_state", "completed", "unknowns",
    "next_action", "evidence_refs", "rollback_data",
}
_SENSITIVE_MARKERS = ("password", "token", "cookie", "secret", "api_key", "private_key", "credential")
_VERSION = 1


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _target_hash(target: str) -> str:
    return hashlib.sha256(target.encode("utf-8")).hexdigest()


def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            low = str(k).lower()
            if any(marker in low for marker in _SENSITIVE_MARKERS):
                continue
            out[str(k)] = _sanitize(v)
        return out
    if isinstance(value, list):
        return [_sanitize(v) for v in value]
    if isinstance(value, tuple):
        return [_sanitize(v) for v in value]
    return value


def build_capsule(state: dict[str, Any], secret: bytes, target: str, now_epoch: int, ttl_seconds: int = 900) -> dict[str, Any]:
    if not secret or not target or now_epoch < 0 or ttl_seconds <= 0:
        raise ValueError("invalid capsule parameters")
    payload = {k: _sanitize(state[k]) for k in sorted(_ALLOWED_FIELDS) if k in state}
    body = {
        "version": _VERSION,
        "issued_at": now_epoch,
        "expires_at": now_epoch + ttl_seconds,
        "target_hash": _target_hash(target),
        "payload": payload,
    }
    signature = hmac.new(secret, _canonical(body), hashlib.sha256).hexdigest()
    return {**body, "signature": signature}


def verify_capsule(capsule: dict[str, Any], secret: bytes, target: str, now_epoch: int) -> tuple[str, str, dict[str, Any] | None]:
    if not secret or not target or now_epoch < 0:
        return "FREEZE", "INVALID_VERIFIER_PARAMETERS", None
    required = {"version", "issued_at", "expires_at", "target_hash", "payload", "signature"}
    if set(capsule) != required:
        return "FREEZE", "MALFORMED_CAPSULE", None
    if capsule["version"] != _VERSION:
        return "FREEZE", "UNSUPPORTED_VERSION", None
    if capsule["target_hash"] != _target_hash(target):
        return "FREEZE", "TARGET_MISMATCH", None
    if not isinstance(capsule["issued_at"], int) or not isinstance(capsule["expires_at"], int) or capsule["issued_at"] >= capsule["expires_at"]:
        return "FREEZE", "INVALID_TIME_RANGE", None
    if now_epoch >= capsule["expires_at"]:
        return "FREEZE", "EXPIRED", None
    body = {k: capsule[k] for k in ("version", "issued_at", "expires_at", "target_hash", "payload")}
    expected = hmac.new(secret, _canonical(body), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, str(capsule["signature"])):
        return "FREEZE", "SIGNATURE_MISMATCH", None
    return "ALLOW", "VERIFIED_CAPSULE", capsule["payload"]
