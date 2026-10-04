from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Mapping, Sequence


class FingerprintError(ValueError):
    """Raised when a behavior record cannot be canonically represented."""


@dataclass(frozen=True)
class ScenarioRecord:
    scenario_id: str
    input_payload: Any
    outcome_status: str
    output_payload: Any
    side_effects: tuple[str, ...] = ()


@dataclass(frozen=True)
class BehaviorFingerprint:
    digest: str
    scenario_digests: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class BehaviorDiff:
    added: tuple[str, ...]
    removed: tuple[str, ...]
    changed: tuple[str, ...]
    unchanged: tuple[str, ...]


def _validate_canonical(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (str, int, bool)):
        return
    if isinstance(value, float):
        raise FingerprintError(f"floats are forbidden in canonical payloads at {path}")
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                raise FingerprintError(f"mapping keys must be strings at {path}")
            _validate_canonical(child, f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            _validate_canonical(child, f"{path}[{index}]")
        return
    raise FingerprintError(f"unsupported canonical payload type at {path}: {type(value).__name__}")


def _canonical_json(value: Any) -> str:
    _validate_canonical(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _scenario_material(record: ScenarioRecord) -> dict[str, Any]:
    if not record.scenario_id.strip():
        raise FingerprintError("scenario_id must be non-empty")
    if not record.outcome_status.strip():
        raise FingerprintError(f"scenario {record.scenario_id} outcome_status must be non-empty")
    return {
        "scenario_id": record.scenario_id,
        "input": record.input_payload,
        "status": record.outcome_status,
        "output": record.output_payload,
        "side_effects": list(record.side_effects),
    }


def _digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_fingerprint(records: Iterable[ScenarioRecord]) -> BehaviorFingerprint:
    ordered = sorted(records, key=lambda record: record.scenario_id)
    if not ordered:
        raise FingerprintError("at least one scenario is required")
    ids = [record.scenario_id for record in ordered]
    if len(ids) != len(set(ids)):
        raise FingerprintError("scenario IDs must be unique")

    scenario_pairs: list[tuple[str, str]] = []
    aggregate: list[dict[str, str]] = []
    for record in ordered:
        material = _scenario_material(record)
        scenario_digest = _digest_text(_canonical_json(material))
        scenario_pairs.append((record.scenario_id, scenario_digest))
        aggregate.append({"scenario_id": record.scenario_id, "digest": scenario_digest})

    return BehaviorFingerprint(
        digest=_digest_text(_canonical_json(aggregate)),
        scenario_digests=tuple(scenario_pairs),
    )


def diff_fingerprints(old: BehaviorFingerprint, new: BehaviorFingerprint) -> BehaviorDiff:
    old_map = dict(old.scenario_digests)
    new_map = dict(new.scenario_digests)
    old_ids = set(old_map)
    new_ids = set(new_map)
    common = old_ids & new_ids
    return BehaviorDiff(
        added=tuple(sorted(new_ids - old_ids)),
        removed=tuple(sorted(old_ids - new_ids)),
        changed=tuple(sorted(sid for sid in common if old_map[sid] != new_map[sid])),
        unchanged=tuple(sorted(sid for sid in common if old_map[sid] == new_map[sid])),
    )
