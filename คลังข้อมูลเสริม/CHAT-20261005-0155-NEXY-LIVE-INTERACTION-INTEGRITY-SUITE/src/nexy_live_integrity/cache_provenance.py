from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .common import GateDecision, GateStatus, canonical_digest, require_digest, require_nonempty


@dataclass(frozen=True, slots=True)
class CacheNamespace:
    project_id: str
    user_scope: str
    policy_hash: str
    model_contract_hash: str
    tool_contract_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "project_id", require_nonempty("project_id", self.project_id))
        object.__setattr__(self, "user_scope", require_nonempty("user_scope", self.user_scope))
        object.__setattr__(self, "policy_hash", require_digest("policy_hash", self.policy_hash))
        object.__setattr__(self, "model_contract_hash", require_digest("model_contract_hash", self.model_contract_hash))
        object.__setattr__(self, "tool_contract_hash", require_digest("tool_contract_hash", self.tool_contract_hash))
        object.__setattr__(self, "schema_version", require_nonempty("schema_version", self.schema_version))


@dataclass(frozen=True, slots=True)
class CacheEntry:
    namespace: CacheNamespace
    input_digest: str
    value: Any
    value_digest: str
    entry_digest: str


class CacheProvenanceFirewall:
    """In-memory reference cache with exact provenance binding.

    Cache reuse is legal only when every namespace dimension and the input digest
    match. There is no permissive fallback from one user/project/policy/model/tool
    contract to another.
    """

    def __init__(self) -> None:
        self._entries: dict[str, CacheEntry] = {}

    @staticmethod
    def cache_key(namespace: CacheNamespace, input_material: Any) -> str:
        return canonical_digest({"namespace": namespace, "input": input_material})

    def put(self, namespace: CacheNamespace, input_material: Any, value: Any) -> CacheEntry:
        input_digest = canonical_digest(input_material)
        value_digest = canonical_digest(value)
        entry_digest = canonical_digest({
            "namespace": namespace,
            "input_digest": input_digest,
            "value_digest": value_digest,
        })
        entry = CacheEntry(namespace, input_digest, value, value_digest, entry_digest)
        self._entries[self.cache_key(namespace, input_material)] = entry
        return entry

    def validate_entry(self, namespace: CacheNamespace, input_material: Any, entry: CacheEntry) -> GateDecision:
        fingerprint = canonical_digest({"expected_namespace": namespace, "input": input_material, "entry": entry})
        if entry.namespace != namespace:
            return GateDecision(GateStatus.FREEZE, "CACHE_PROVENANCE_MISMATCH", "Cached value belongs to a different provenance namespace.", fingerprint)
        if entry.input_digest != canonical_digest(input_material):
            return GateDecision(GateStatus.FREEZE, "CACHE_INPUT_MISMATCH", "Cached value was produced for different input.", fingerprint)
        if entry.value_digest != canonical_digest(entry.value):
            return GateDecision(GateStatus.FREEZE, "CACHE_VALUE_TAMPERED", "Cached value digest does not match its content.", fingerprint)
        expected_entry = canonical_digest({
            "namespace": entry.namespace,
            "input_digest": entry.input_digest,
            "value_digest": entry.value_digest,
        })
        if entry.entry_digest != expected_entry:
            return GateDecision(GateStatus.FREEZE, "CACHE_ENTRY_TAMPERED", "Cache entry envelope integrity check failed.", fingerprint)
        return GateDecision(GateStatus.PASS, "CACHE_PROVENANCE_VALID", "Cache entry exactly matches current provenance and input.", fingerprint)

    def get(self, namespace: CacheNamespace, input_material: Any) -> tuple[GateDecision, Any | None]:
        key = self.cache_key(namespace, input_material)
        entry = self._entries.get(key)
        if entry is None:
            return (
                GateDecision(GateStatus.REJECT, "CACHE_MISS", "No cache entry exists for the exact provenance/input key.", key),
                None,
            )
        decision = self.validate_entry(namespace, input_material, entry)
        return decision, entry.value if decision.allowed else None
