from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .common import ContractError, canonical_data, sha256_hex, require_nonempty


CLASSIFICATION = "AI_PROPOSED_CONCEPT_NOT_ADOPTED"
AUTHORITY = "ADVISORY_ONLY"


@dataclass(frozen=True)
class CompanionEnvelope:
    concept: str
    payload: dict[str, Any]
    classification: str
    authority: str
    may_mutate_core: bool
    payload_hash: str


def companion_envelope(concept: str, payload: dict[str, Any]) -> CompanionEnvelope:
    require_nonempty(concept, "concept")
    if not isinstance(payload, dict):
        raise ContractError("payload must be an object")
    normalized = canonical_data(payload)
    if not isinstance(normalized, dict):
        raise ContractError("normalized payload must remain an object")
    return CompanionEnvelope(
        concept=concept,
        payload=normalized,
        classification=CLASSIFICATION,
        authority=AUTHORITY,
        may_mutate_core=False,
        payload_hash=sha256_hex(normalized),
    )


def assert_advisory_boundary(envelope: CompanionEnvelope) -> None:
    if envelope.classification != CLASSIFICATION:
        raise ContractError("classification boundary violated")
    if envelope.authority != AUTHORITY:
        raise ContractError("authority boundary violated")
    if envelope.may_mutate_core:
        raise ContractError("companion envelope must never authorize core mutation")
