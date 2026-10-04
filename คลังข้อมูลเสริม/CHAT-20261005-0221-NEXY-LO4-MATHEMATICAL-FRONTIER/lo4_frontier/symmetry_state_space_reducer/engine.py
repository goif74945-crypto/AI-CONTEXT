"""Canonical equivalence key for interchangeable entity partitions."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping


def _canonical_json(value: object) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("entity state must be finite JSON-compatible data") from exc


def canonical_partition_key(entities: Mapping[str, dict]) -> str:
    """Hash a state modulo permutations of entities inside the same class.

    Entity identifiers are deliberately excluded from identity.  Class labels
    remain part of the canonical representation, so only explicitly declared
    interchangeable entities collapse to one equivalence class.
    """
    if not isinstance(entities, Mapping) or not entities:
        raise ValueError("entities must be a non-empty mapping")
    partitions: dict[str, list[str]] = {}
    for entity_id, record in entities.items():
        if not isinstance(entity_id, str) or not entity_id:
            raise ValueError("entity ids must be non-empty strings")
        if not isinstance(record, dict):
            raise ValueError(f"entity {entity_id!r} record must be a mapping")
        class_id = record.get("class")
        if not isinstance(class_id, str) or not class_id:
            raise ValueError(f"entity {entity_id!r} requires a non-empty class")
        if "state" not in record:
            raise ValueError(f"entity {entity_id!r} requires state")
        partitions.setdefault(class_id, []).append(_canonical_json(record["state"]))

    canonical = [
        [class_id, sorted(states)]
        for class_id, states in sorted(partitions.items())
    ]
    payload = _canonical_json(canonical).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
