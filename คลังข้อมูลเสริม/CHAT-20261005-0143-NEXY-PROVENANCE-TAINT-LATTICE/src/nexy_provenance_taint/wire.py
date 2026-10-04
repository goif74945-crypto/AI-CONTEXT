from __future__ import annotations

from typing import Any, Mapping

from .core import ProvenanceEngine, ProvenanceError, compute_receipt_id
from .model import Artifact, ReleaseDecision, Taint, VerificationReceipt

ARTIFACT_SCHEMA = "nexy.provenance-taint.artifact/v1"
RECEIPT_SCHEMA = "nexy.provenance-taint.receipt/v1"
DECISION_SCHEMA = "nexy.provenance-taint.release-decision/v1"

_ARTIFACT_KEYS = frozenset(
    {
        "schema",
        "artifact_id",
        "payload_digest",
        "operation_id",
        "parent_ids",
        "root_origins",
        "authority_floor",
        "assurances",
        "taints",
        "created_epoch",
        "metadata",
        "applied_receipts",
    }
)
_RECEIPT_KEYS = frozenset(
    {
        "schema",
        "receipt_id",
        "verifier_id",
        "artifact_id",
        "added_assurances",
        "cleared_taints",
        "issued_epoch",
        "expires_epoch",
    }
)


def _require_exact_keys(record: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    actual = frozenset(record.keys())
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ProvenanceError(f"{label} keys mismatch missing={missing} extra={extra}")


def _str_list(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ProvenanceError(f"{field} must be a list of strings")
    return tuple(value)


def _int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ProvenanceError(f"{field} must be an integer")
    return value


def artifact_to_record(artifact: Artifact) -> dict[str, Any]:
    ProvenanceEngine().assert_integrity(artifact)
    return {
        "schema": ARTIFACT_SCHEMA,
        "artifact_id": artifact.artifact_id,
        "payload_digest": artifact.payload_digest,
        "operation_id": artifact.operation_id,
        "parent_ids": list(artifact.parent_ids),
        "root_origins": list(artifact.root_origins),
        "authority_floor": artifact.authority_floor,
        "assurances": sorted(artifact.assurances),
        "taints": sorted(t.value for t in artifact.taints),
        "created_epoch": artifact.created_epoch,
        "metadata": [[k, v] for k, v in artifact.metadata],
        "applied_receipts": list(artifact.applied_receipts),
    }


def artifact_from_record(record: Mapping[str, Any]) -> Artifact:
    if not isinstance(record, Mapping):
        raise ProvenanceError("artifact record must be a mapping")
    _require_exact_keys(record, _ARTIFACT_KEYS, "artifact")
    if record["schema"] != ARTIFACT_SCHEMA:
        raise ProvenanceError("unsupported artifact schema")

    metadata_raw = record["metadata"]
    if not isinstance(metadata_raw, list):
        raise ProvenanceError("metadata must be a list")
    metadata: list[tuple[str, str]] = []
    for item in metadata_raw:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not isinstance(item[0], str)
            or not isinstance(item[1], str)
        ):
            raise ProvenanceError("metadata entries must be [string, string]")
        metadata.append((item[0], item[1]))

    try:
        taints = frozenset(Taint(value) for value in _str_list(record["taints"], "taints"))
    except ValueError as exc:
        raise ProvenanceError("unknown taint value") from exc

    artifact = Artifact(
        artifact_id=str(record["artifact_id"]),
        payload_digest=str(record["payload_digest"]),
        operation_id=str(record["operation_id"]),
        parent_ids=_str_list(record["parent_ids"], "parent_ids"),
        root_origins=_str_list(record["root_origins"], "root_origins"),
        authority_floor=_int(record["authority_floor"], "authority_floor"),
        assurances=frozenset(_str_list(record["assurances"], "assurances")),
        taints=taints,
        created_epoch=_int(record["created_epoch"], "created_epoch"),
        metadata=tuple(metadata),
        applied_receipts=_str_list(record["applied_receipts"], "applied_receipts"),
    )
    ProvenanceEngine().assert_integrity(artifact)
    return artifact


def receipt_to_record(receipt: VerificationReceipt) -> dict[str, Any]:
    expected = compute_receipt_id(
        verifier_id=receipt.verifier_id,
        artifact_id=receipt.artifact_id,
        added_assurances=receipt.added_assurances,
        cleared_taints=receipt.cleared_taints,
        issued_epoch=receipt.issued_epoch,
        expires_epoch=receipt.expires_epoch,
    )
    if receipt.receipt_id != expected:
        raise ProvenanceError("receipt identity mismatch")
    return {
        "schema": RECEIPT_SCHEMA,
        "receipt_id": receipt.receipt_id,
        "verifier_id": receipt.verifier_id,
        "artifact_id": receipt.artifact_id,
        "added_assurances": sorted(receipt.added_assurances),
        "cleared_taints": sorted(t.value for t in receipt.cleared_taints),
        "issued_epoch": receipt.issued_epoch,
        "expires_epoch": receipt.expires_epoch,
    }


def receipt_from_record(record: Mapping[str, Any]) -> VerificationReceipt:
    if not isinstance(record, Mapping):
        raise ProvenanceError("receipt record must be a mapping")
    _require_exact_keys(record, _RECEIPT_KEYS, "receipt")
    if record["schema"] != RECEIPT_SCHEMA:
        raise ProvenanceError("unsupported receipt schema")
    expires = record["expires_epoch"]
    if expires is not None:
        expires = _int(expires, "expires_epoch")
    try:
        cleared = frozenset(
            Taint(value) for value in _str_list(record["cleared_taints"], "cleared_taints")
        )
    except ValueError as exc:
        raise ProvenanceError("unknown taint value") from exc
    receipt = VerificationReceipt(
        receipt_id=str(record["receipt_id"]),
        verifier_id=str(record["verifier_id"]),
        artifact_id=str(record["artifact_id"]),
        added_assurances=frozenset(_str_list(record["added_assurances"], "added_assurances")),
        cleared_taints=cleared,
        issued_epoch=_int(record["issued_epoch"], "issued_epoch"),
        expires_epoch=expires,
    )
    receipt_to_record(receipt)
    return receipt


def decision_to_record(decision: ReleaseDecision) -> dict[str, Any]:
    if decision.state not in {"ALLOW", "FREEZE"}:
        raise ProvenanceError("invalid release decision state")
    if decision.allowed != (decision.state == "ALLOW"):
        raise ProvenanceError("release decision allowed/state mismatch")
    if tuple(sorted(decision.reason_codes)) != decision.reason_codes:
        raise ProvenanceError("release decision reason_codes must be sorted")
    if decision.allowed and decision.reason_codes:
        raise ProvenanceError("ALLOW decision cannot contain reason codes")
    if not decision.allowed and not decision.reason_codes:
        raise ProvenanceError("FREEZE decision requires at least one reason code")
    return {
        "schema": DECISION_SCHEMA,
        "allowed": decision.allowed,
        "state": decision.state,
        "reason_codes": list(decision.reason_codes),
        "artifact_id": decision.artifact_id,
        "policy_id": decision.policy_id,
    }
