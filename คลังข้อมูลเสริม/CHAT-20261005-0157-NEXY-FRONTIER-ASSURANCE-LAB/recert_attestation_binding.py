"""State/policy binding extension for experimental RECERT certificates.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping

from frontier_assurance_lab import FreezeError, RecoveryPolicy, stable_hash
from recert_path_integrity import PointerRecoveryPolicy, RecertPathIntegrityAssurance


@dataclass(frozen=True)
class RecoveryAttestationContract:
    """Caller-declared identity of one bounded recovery comparison."""

    attestation_id: str
    incident_id: str
    before_revision: str
    after_revision: str

    def __post_init__(self) -> None:
        for name in (
            "attestation_id",
            "incident_id",
            "before_revision",
            "after_revision",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise FreezeError(f"{name} must be a non-empty string")

    def canonical_record(self) -> dict[str, str]:
        return {
            "schema": "RECERT_ATTESTATION_BINDING_V1",
            "attestation_id": self.attestation_id,
            "incident_id": self.incident_id,
            "before_revision": self.before_revision,
            "after_revision": self.after_revision,
        }


def _snapshot_value(value: Any, active: set[int] | None = None) -> Any:
    """Copy supported built-ins so hash and certification see the same value."""

    if active is None:
        active = set()

    if type(value) is dict:
        identity = id(value)
        if identity in active:
            raise FreezeError("cyclic recovery state")
        if any(not isinstance(key, str) for key in value):
            raise FreezeError("recovery state keys must be strings")
        active.add(identity)
        try:
            return {
                key: _snapshot_value(value[key], active)
                for key in sorted(value)
            }
        finally:
            active.remove(identity)

    if type(value) in (list, tuple):
        identity = id(value)
        if identity in active:
            raise FreezeError("cyclic recovery state")
        active.add(identity)
        try:
            items = [_snapshot_value(item, active) for item in value]
            return items if type(value) is list else tuple(items)
        finally:
            active.remove(identity)

    if isinstance(value, Mapping):
        raise FreezeError("recovery state mappings must be built-in dict values")

    if type(value) not in (type(None), bool, int, float, str):
        raise FreezeError("recovery state contains a non-canonical value")
    if type(value) is float and not math.isfinite(value):
        raise FreezeError("recovery state floats must be finite")
    return value


def _snapshot_state(name: str, state: Mapping[str, Any]) -> dict[str, Any]:
    if type(state) is not dict:
        raise FreezeError(f"{name} must be a built-in dict")
    snapshot = _snapshot_value(state)
    if type(snapshot) is not dict:
        raise FreezeError(f"{name} snapshot must remain a dict")
    return snapshot


def _typed_state_record(value: Any) -> dict[str, Any]:
    """Preserve container and scalar types in the state commitment."""

    if type(value) is dict:
        return {
            "type": "dict",
            "entries": [
                {"key": key, "value": _typed_state_record(value[key])}
                for key in sorted(value)
            ],
        }
    if type(value) is list:
        return {
            "type": "list",
            "items": [_typed_state_record(item) for item in value],
        }
    if type(value) is tuple:
        return {
            "type": "tuple",
            "items": [_typed_state_record(item) for item in value],
        }
    if value is None:
        return {"type": "null"}
    if type(value) is bool:
        return {"type": "bool", "value": value}
    if type(value) is int:
        return {"type": "int", "value": value}
    if type(value) is float:
        return {"type": "float", "value": repr(value)}
    return {"type": "str", "value": value}


def _snapshot_original_policy(policy: RecoveryPolicy) -> tuple[RecoveryPolicy, dict[str, Any]]:
    if not isinstance(policy, RecoveryPolicy):
        raise FreezeError("invalid original recovery policy")
    if type(policy.modes) is not dict:
        raise FreezeError("original recovery policy modes must be a built-in dict")
    if type(policy.ignore_prefixes) is not tuple:
        raise FreezeError("original recovery ignore prefixes must be a tuple")
    if any(not isinstance(prefix, str) or not prefix.strip() for prefix in policy.ignore_prefixes):
        raise FreezeError("original recovery ignore prefixes must be non-empty strings")
    snapshot = RecoveryPolicy(
        modes=dict(policy.modes),
        ignore_prefixes=tuple(policy.ignore_prefixes),
    )
    record = {
        "modes": {name: snapshot.modes[name] for name in sorted(snapshot.modes)},
        "ignore_prefixes": sorted(snapshot.ignore_prefixes),
    }
    return snapshot, record


def _snapshot_pointer_policy(
    policy: PointerRecoveryPolicy,
) -> tuple[PointerRecoveryPolicy, dict[str, Any]]:
    if not isinstance(policy, PointerRecoveryPolicy):
        raise FreezeError("invalid pointer recovery policy")
    if type(policy.modes) is not dict:
        raise FreezeError("pointer recovery policy modes must be a built-in dict")
    if type(policy.ignore_prefixes) is not tuple:
        raise FreezeError("pointer recovery ignore prefixes must be a tuple")
    snapshot = PointerRecoveryPolicy(
        modes=dict(policy.modes),
        ignore_prefixes=tuple(policy.ignore_prefixes),
    )
    record = {
        "modes": {name: snapshot.modes[name] for name in sorted(snapshot.modes)},
        "ignore_prefixes": sorted(snapshot.ignore_prefixes),
    }
    return snapshot, record


class RecertAttestationBindingAssurance:
    """Bind RECERT's decision to exact snapshotted states and policies."""

    def __init__(self) -> None:
        self.base = RecertPathIntegrityAssurance()

    def assess(
        self,
        contract: RecoveryAttestationContract,
        before: Mapping[str, Any],
        after: Mapping[str, Any],
        original_policy: RecoveryPolicy,
        pointer_policy: PointerRecoveryPolicy,
    ) -> dict[str, Any]:
        if not isinstance(contract, RecoveryAttestationContract):
            raise FreezeError("invalid recovery attestation contract")

        before_snapshot = _snapshot_state("before state", before)
        after_snapshot = _snapshot_state("after state", after)
        original_snapshot, original_record = _snapshot_original_policy(original_policy)
        pointer_snapshot, pointer_record = _snapshot_pointer_policy(pointer_policy)

        contract_hash = stable_hash(contract.canonical_record())
        before_hash = stable_hash(_typed_state_record(before_snapshot))
        after_hash = stable_hash(_typed_state_record(after_snapshot))
        original_policy_hash = stable_hash(original_record)
        pointer_policy_hash = stable_hash(pointer_record)
        binding_record = {
            "schema": "RECERT_ATTESTATION_BINDING_V1",
            "attestation_contract_hash": contract_hash,
            "before_state_hash": before_hash,
            "after_state_hash": after_hash,
            "original_policy_hash": original_policy_hash,
            "pointer_policy_hash": pointer_policy_hash,
        }
        binding_hash = stable_hash(binding_record)

        base = self.base.assess(
            before_snapshot,
            after_snapshot,
            original_snapshot,
            pointer_snapshot,
        )
        result: dict[str, Any] = {
            "status": base["status"],
            "reason": base["reason"],
            "original": base["original"],
            "pointer_safe": base["pointer_safe"],
            "base_result_hash": base["result_hash"],
            **binding_record,
            "binding_hash": binding_hash,
        }
        result["result_hash"] = stable_hash(result)
        return result
