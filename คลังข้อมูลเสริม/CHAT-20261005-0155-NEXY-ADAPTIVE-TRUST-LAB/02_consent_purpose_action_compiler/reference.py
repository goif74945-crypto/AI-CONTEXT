from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Iterable


@dataclass(frozen=True)
class ConsentGrant:
    grant_id: str
    subject_id: str
    purposes: tuple[str, ...]
    actions: tuple[str, ...]
    resources: tuple[str, ...]
    issued_at: datetime
    expires_at: datetime
    revoked: bool = False


@dataclass(frozen=True)
class ActionRequest:
    request_id: str
    subject_id: str
    purpose: str
    action: str
    resource: str
    at: datetime


@dataclass(frozen=True)
class ConsentDecision:
    status: str
    reason: str
    grant_id: str | None
    receipt_digest: str


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive datetime is forbidden")
    return dt.astimezone(timezone.utc)


def _digest(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def evaluate(grants: Iterable[ConsentGrant], req: ActionRequest) -> ConsentDecision:
    try:
        now = _utc(req.at)
    except ValueError:
        return ConsentDecision("BLOCK", "INVALID_REQUEST_TIME", None, _digest({"request_id": req.request_id, "status": "BLOCK"}))
    if not all([req.request_id, req.subject_id, req.purpose, req.action, req.resource]):
        return ConsentDecision("BLOCK", "MALFORMED_REQUEST", None, _digest({"request_id": req.request_id, "status": "BLOCK"}))

    candidates: list[ConsentGrant] = []
    for g in grants:
        try:
            issued, expires = _utc(g.issued_at), _utc(g.expires_at)
        except ValueError:
            return ConsentDecision("BLOCK", "INVALID_GRANT_TIME", g.grant_id or None, _digest({"request_id": req.request_id, "status": "BLOCK"}))
        fields = [g.grant_id, g.subject_id, *g.purposes, *g.actions, *g.resources]
        if not all(fields) or "*" in fields or issued >= expires:
            return ConsentDecision("BLOCK", "MALFORMED_GRANT", g.grant_id or None, _digest({"request_id": req.request_id, "status": "BLOCK"}))
        if g.subject_id != req.subject_id or g.revoked or not (issued <= now < expires):
            continue
        if req.purpose in g.purposes and req.action in g.actions and req.resource in g.resources:
            candidates.append(g)

    if not candidates:
        payload = {"request_id": req.request_id, "status": "ASK", "reason": "NO_ACTIVE_EXACT_CONSENT"}
        return ConsentDecision("ASK", payload["reason"], None, _digest(payload))

    chosen = sorted(candidates, key=lambda g: (_utc(g.expires_at), g.grant_id))[0]
    payload = {
        "request_id": req.request_id,
        "status": "ALLOW",
        "grant_id": chosen.grant_id,
        "purpose": req.purpose,
        "action": req.action,
        "resource": req.resource,
    }
    return ConsentDecision("ALLOW", "EXACT_ACTIVE_CONSENT", chosen.grant_id, _digest(payload))
