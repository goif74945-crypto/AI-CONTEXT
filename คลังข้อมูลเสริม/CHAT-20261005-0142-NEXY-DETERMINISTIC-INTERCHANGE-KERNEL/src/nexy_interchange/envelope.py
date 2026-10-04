from __future__ import annotations

from copy import deepcopy
import re
from typing import Any

from .canonical import CanonicalLimits, DEFAULT_LIMITS, canonical_text, fingerprint
from .errors import EnvelopeVerificationError

ENVELOPE_FORMAT = "NEXY-NDIK-ENVELOPE/1"
_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_REQUIRED_FIELDS = {
    "format",
    "kind",
    "observed_at",
    "payload",
    "payload_hash",
    "provenance",
    "schema_version",
    "envelope_hash",
}


def _validate_metadata(
    *, kind: Any, schema_version: Any, provenance: Any, observed_at: Any
) -> None:
    if not isinstance(kind, str) or not kind.strip():
        raise ValueError("kind must be a non-empty string")
    if not isinstance(schema_version, str) or not schema_version.strip():
        raise ValueError("schema_version must be a non-empty string")
    if not isinstance(observed_at, str) or not observed_at.strip():
        raise ValueError("observed_at must be explicit and non-empty")
    if type(provenance) is not dict:
        raise ValueError("provenance must be an object/dict")


def build_envelope(
    *,
    kind: str,
    schema_version: str,
    payload: Any,
    provenance: dict[str, Any],
    observed_at: str,
    limits: CanonicalLimits = DEFAULT_LIMITS,
) -> dict[str, Any]:
    """Build a deterministic proof-carrying envelope.

    observed_at is explicit input by design. This function never reads the system
    clock, generates randomness, or consults the environment.
    """

    _validate_metadata(
        kind=kind,
        schema_version=schema_version,
        provenance=provenance,
        observed_at=observed_at,
    )

    payload_copy = deepcopy(payload)
    provenance_copy = deepcopy(provenance)
    payload_hash = fingerprint(
        payload_copy, domain="NEXY-NDIK-PAYLOAD-V1", limits=limits
    )

    unsigned = {
        "format": ENVELOPE_FORMAT,
        "kind": kind,
        "observed_at": observed_at,
        "payload": payload_copy,
        "payload_hash": payload_hash,
        "provenance": provenance_copy,
        "schema_version": schema_version,
    }
    envelope_hash = fingerprint(
        unsigned, domain="NEXY-NDIK-ENVELOPE-V1", limits=limits
    )
    envelope = dict(unsigned)
    envelope["envelope_hash"] = envelope_hash
    canonical_text(envelope, limits=limits)
    return envelope


def verify_envelope(
    envelope: dict[str, Any], *, limits: CanonicalLimits = DEFAULT_LIMITS
) -> bool:
    if type(envelope) is not dict:
        raise EnvelopeVerificationError("envelope must be an object/dict", path="$")
    keys = set(envelope)
    if keys != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - keys)
        extra = sorted(keys - _REQUIRED_FIELDS)
        raise EnvelopeVerificationError(
            f"envelope key mismatch; missing={missing}, extra={extra}", path="$"
        )
    if envelope["format"] != ENVELOPE_FORMAT:
        raise EnvelopeVerificationError("unsupported envelope format", path="$.format")
    try:
        _validate_metadata(
            kind=envelope["kind"],
            schema_version=envelope["schema_version"],
            provenance=envelope["provenance"],
            observed_at=envelope["observed_at"],
        )
    except ValueError as exc:
        raise EnvelopeVerificationError(str(exc), path="$") from exc

    if not isinstance(envelope["payload_hash"], str) or not _SHA256_RE.fullmatch(
        envelope["payload_hash"]
    ):
        raise EnvelopeVerificationError("invalid payload_hash encoding", path="$.payload_hash")
    if not isinstance(envelope["envelope_hash"], str) or not _SHA256_RE.fullmatch(
        envelope["envelope_hash"]
    ):
        raise EnvelopeVerificationError("invalid envelope_hash encoding", path="$.envelope_hash")

    actual_payload_hash = fingerprint(
        envelope["payload"], domain="NEXY-NDIK-PAYLOAD-V1", limits=limits
    )
    if actual_payload_hash != envelope["payload_hash"]:
        raise EnvelopeVerificationError("payload hash mismatch", path="$.payload_hash")

    unsigned = {key: value for key, value in envelope.items() if key != "envelope_hash"}
    actual_envelope_hash = fingerprint(
        unsigned, domain="NEXY-NDIK-ENVELOPE-V1", limits=limits
    )
    if actual_envelope_hash != envelope["envelope_hash"]:
        raise EnvelopeVerificationError("envelope hash mismatch", path="$.envelope_hash")
    return True
