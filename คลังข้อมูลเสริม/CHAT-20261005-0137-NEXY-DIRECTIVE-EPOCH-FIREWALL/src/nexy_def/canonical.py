from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_hex(value: Any) -> str:
    if not isinstance(value, str):
        value = canonical_json(value)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def chained_hash(previous: str, event_hash: str, epoch: int) -> str:
    return sha256_hex({"previous": previous, "event_hash": event_hash, "epoch": epoch})


def approval_binding(action_id: str, epoch: int, action_digest: str, lineage_hash: str) -> str:
    """Deterministic binding only; NOT an authentication/signature mechanism."""
    return sha256_hex(
        {
            "domain": "NEXY_DEF_APPROVAL_V1",
            "action_id": action_id,
            "epoch": epoch,
            "action_digest": action_digest,
            "lineage_hash": lineage_hash,
        }
    )
