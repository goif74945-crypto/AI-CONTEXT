from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any, Mapping

from .models import DecisionRecord


def canonical_json(value: Any) -> str:
    """Return deterministic JSON suitable for hashing and replay comparison."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def mapping_digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def record_digest(record: DecisionRecord) -> str:
    payload = asdict(record)
    payload["outcome"] = record.outcome.value
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
