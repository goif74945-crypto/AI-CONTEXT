"""Semantic normalization for order-insensitive NEXY-REFLEX snapshots."""

from __future__ import annotations

from typing import Any

from .canonical import canonical_json, sha256_digest
from .models import Snapshot


def semantic_snapshot_payload(snapshot: Snapshot) -> dict[str, Any]:
    """Normalize order-insensitive collections while preserving authority precedence."""
    return {
        "snapshot_version": snapshot.snapshot_version,
        "target": snapshot.target.to_dict(),
        "authority_order": list(snapshot.authority_order),
        "requirements": sorted(
            (claim.to_dict() for claim in snapshot.requirements),
            key=canonical_json,
        ),
        "evidence": sorted(
            (record.to_dict() for record in snapshot.evidence),
            key=canonical_json,
        ),
    }


def snapshot_digest(snapshot: Snapshot) -> str:
    """Return a semantic snapshot digest invariant to list ordering."""
    return sha256_digest(semantic_snapshot_payload(snapshot))
