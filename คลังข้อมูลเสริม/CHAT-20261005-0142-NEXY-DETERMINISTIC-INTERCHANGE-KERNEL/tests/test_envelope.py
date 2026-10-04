from __future__ import annotations

from copy import deepcopy

import pytest

from nexy_interchange import EnvelopeVerificationError, build_envelope, verify_envelope


BASE = {
    "kind": "candidate-result",
    "schema_version": "1.0.0",
    "payload": {"decision": "FREEZE", "reason_code": "AMBIGUOUS_INPUT"},
    "provenance": {"source": "unit-test", "revision": "abc123"},
    "observed_at": "2026-10-05T01:42:00+07:00",
}


def test_build_is_deterministic_for_same_explicit_inputs() -> None:
    assert build_envelope(**BASE) == build_envelope(**BASE)


def test_envelope_verifies() -> None:
    envelope = build_envelope(**BASE)
    assert verify_envelope(envelope) is True


def test_payload_tamper_is_detected() -> None:
    envelope = build_envelope(**BASE)
    envelope["payload"]["decision"] = "RUN"
    with pytest.raises(EnvelopeVerificationError, match="payload hash mismatch"):
        verify_envelope(envelope)


def test_provenance_tamper_is_detected_by_envelope_hash() -> None:
    envelope = build_envelope(**BASE)
    envelope["provenance"]["revision"] = "def456"
    with pytest.raises(EnvelopeVerificationError, match="envelope hash mismatch"):
        verify_envelope(envelope)


def test_unknown_field_is_rejected() -> None:
    envelope = build_envelope(**BASE)
    envelope["surprise"] = True
    with pytest.raises(EnvelopeVerificationError, match="key mismatch"):
        verify_envelope(envelope)


def test_missing_field_is_rejected() -> None:
    envelope = build_envelope(**BASE)
    del envelope["provenance"]
    with pytest.raises(EnvelopeVerificationError, match="key mismatch"):
        verify_envelope(envelope)


def test_payload_hash_stable_when_only_provenance_changes() -> None:
    first = build_envelope(**BASE)
    changed = deepcopy(BASE)
    changed["provenance"]["revision"] = "next"
    second = build_envelope(**changed)
    assert first["payload_hash"] == second["payload_hash"]
    assert first["envelope_hash"] != second["envelope_hash"]


def test_observed_at_is_required_instead_of_implicit_clock() -> None:
    broken = dict(BASE)
    broken["observed_at"] = ""
    with pytest.raises(ValueError, match="observed_at"):
        build_envelope(**broken)


def test_invalid_metadata_type_is_rejected_during_verify() -> None:
    envelope = build_envelope(**BASE)
    envelope["kind"] = 123
    with pytest.raises(EnvelopeVerificationError, match="kind"):
        verify_envelope(envelope)


def test_non_object_provenance_is_rejected_during_build() -> None:
    broken = dict(BASE)
    broken["provenance"] = ["not", "an", "object"]
    with pytest.raises(ValueError, match="provenance"):
        build_envelope(**broken)
