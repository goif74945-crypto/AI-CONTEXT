from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from typing import Iterable, Mapping, Sequence

from .model import (
    Artifact,
    PROTECTED_TAINTS,
    ReleaseDecision,
    ReleasePolicy,
    SourceSpec,
    Taint,
    TransformContract,
    VerificationReceipt,
)


class ProvenanceError(ValueError):
    """Raised when a provenance invariant is violated."""


class IntegrityError(ProvenanceError):
    """Raised when an artifact's content-addressed identity does not match its fields."""


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _normalize_metadata(metadata: Mapping[str, str] | None) -> tuple[tuple[str, str], ...]:
    if not metadata:
        return ()
    normalized: list[tuple[str, str]] = []
    for key, value in metadata.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ProvenanceError("metadata keys and values must be strings")
        normalized.append((key, value))
    return tuple(sorted(normalized))


def _artifact_identity_payload(
    *,
    payload_digest: str,
    operation_id: str,
    parent_ids: Sequence[str],
    root_origins: Sequence[str],
    authority_floor: int,
    assurances: Iterable[str],
    taints: Iterable[Taint],
    created_epoch: int,
    metadata: Sequence[tuple[str, str]],
    applied_receipts: Sequence[str],
) -> dict[str, object]:
    return {
        "payload_digest": payload_digest,
        "operation_id": operation_id,
        "parent_ids": list(parent_ids),
        "root_origins": list(root_origins),
        "authority_floor": authority_floor,
        "assurances": sorted(assurances),
        "taints": sorted(t.value for t in taints),
        "created_epoch": created_epoch,
        "metadata": [list(item) for item in metadata],
        "applied_receipts": list(applied_receipts),
    }


def compute_artifact_id(**kwargs: object) -> str:
    return _digest_bytes(_canonical_json(_artifact_identity_payload(**kwargs)))


def _receipt_identity_payload(
    *,
    verifier_id: str,
    artifact_id: str,
    added_assurances: Iterable[str],
    cleared_taints: Iterable[Taint],
    issued_epoch: int,
    expires_epoch: int | None,
) -> dict[str, object]:
    return {
        "verifier_id": verifier_id,
        "artifact_id": artifact_id,
        "added_assurances": sorted(added_assurances),
        "cleared_taints": sorted(t.value for t in cleared_taints),
        "issued_epoch": issued_epoch,
        "expires_epoch": expires_epoch,
    }


def compute_receipt_id(**kwargs: object) -> str:
    return _digest_bytes(_canonical_json(_receipt_identity_payload(**kwargs)))


class ProvenanceEngine:
    """Deterministic reference engine for lineage-preserving release decisions."""

    def source(
        self,
        payload: bytes | str,
        spec: SourceSpec,
        *,
        metadata: Mapping[str, str] | None = None,
    ) -> Artifact:
        self._validate_source_spec(spec)
        payload_bytes = payload.encode("utf-8") if isinstance(payload, str) else bytes(payload)
        payload_digest = _digest_bytes(payload_bytes)
        taints = set(spec.taints)
        if not spec.origin_id.strip():
            taints.add(Taint.UNKNOWN_ORIGIN)
        if "verified" not in spec.assurance_tags:
            taints.add(Taint.UNVERIFIED)

        artifact_fields = dict(
            payload_digest=payload_digest,
            operation_id=f"source:{spec.source_kind}",
            parent_ids=(),
            root_origins=(spec.origin_id,),
            authority_floor=spec.authority_rank,
            assurances=frozenset(spec.assurance_tags),
            taints=frozenset(taints),
            created_epoch=spec.epoch,
            metadata=_normalize_metadata(metadata),
            applied_receipts=(),
        )
        artifact_id = compute_artifact_id(**artifact_fields)
        return Artifact(artifact_id=artifact_id, **artifact_fields)

    def derive(
        self,
        payload: bytes | str,
        parents: Sequence[Artifact],
        contract: TransformContract,
        *,
        epoch: int,
        metadata: Mapping[str, str] | None = None,
    ) -> Artifact:
        if not parents:
            raise ProvenanceError("derive requires at least one parent")
        if not contract.contract_id.strip():
            raise ProvenanceError("transform contract_id must be non-empty")
        if epoch < 0:
            raise ProvenanceError("epoch must be >= 0")

        for parent in parents:
            self.assert_integrity(parent)

        missing_by_parent = [
            sorted(contract.required_assurances - parent.assurances)
            for parent in parents
        ]
        if any(missing_by_parent):
            raise ProvenanceError(
                "required assurances missing: "
                + json.dumps(missing_by_parent, separators=(",", ":"))
            )

        authority_floor = min(parent.authority_floor for parent in parents)
        inherited_assurances = set(parents[0].assurances)
        for parent in parents[1:]:
            inherited_assurances.intersection_update(parent.assurances)
        inherited_assurances.intersection_update(contract.preserved_assurances)

        taints: set[Taint] = set(contract.introduced_taints)
        root_origins: set[str] = set()
        for parent in parents:
            taints.update(parent.taints)
            root_origins.update(parent.root_origins)
        if not contract.deterministic:
            taints.add(Taint.NONDETERMINISTIC)

        payload_bytes = payload.encode("utf-8") if isinstance(payload, str) else bytes(payload)
        artifact_fields = dict(
            payload_digest=_digest_bytes(payload_bytes),
            operation_id=f"transform:{contract.contract_id}",
            parent_ids=tuple(parent.artifact_id for parent in parents),
            root_origins=tuple(sorted(root_origins)),
            authority_floor=authority_floor,
            assurances=frozenset(inherited_assurances),
            taints=frozenset(taints),
            created_epoch=epoch,
            metadata=_normalize_metadata(metadata),
            applied_receipts=(),
        )
        artifact_id = compute_artifact_id(**artifact_fields)
        return Artifact(artifact_id=artifact_id, **artifact_fields)

    def issue_verification(
        self,
        artifact: Artifact,
        *,
        verifier_id: str,
        added_assurances: Iterable[str] = (),
        cleared_taints: Iterable[Taint] = (),
        issued_epoch: int,
        expires_epoch: int | None = None,
    ) -> VerificationReceipt:
        self.assert_integrity(artifact)
        if not verifier_id.strip():
            raise ProvenanceError("verifier_id must be non-empty")
        if issued_epoch < 0:
            raise ProvenanceError("issued_epoch must be >= 0")
        if expires_epoch is not None and expires_epoch < issued_epoch:
            raise ProvenanceError("expires_epoch cannot precede issued_epoch")
        fields = dict(
            verifier_id=verifier_id,
            artifact_id=artifact.artifact_id,
            added_assurances=frozenset(added_assurances),
            cleared_taints=frozenset(cleared_taints),
            issued_epoch=issued_epoch,
            expires_epoch=expires_epoch,
        )
        return VerificationReceipt(receipt_id=compute_receipt_id(**fields), **fields)

    def apply_verification(
        self,
        artifact: Artifact,
        receipt: VerificationReceipt,
        *,
        current_epoch: int,
    ) -> Artifact:
        self.assert_integrity(artifact)
        expected_receipt_id = compute_receipt_id(
            verifier_id=receipt.verifier_id,
            artifact_id=receipt.artifact_id,
            added_assurances=receipt.added_assurances,
            cleared_taints=receipt.cleared_taints,
            issued_epoch=receipt.issued_epoch,
            expires_epoch=receipt.expires_epoch,
        )
        if receipt.receipt_id != expected_receipt_id:
            raise ProvenanceError("receipt identity mismatch")
        if receipt.artifact_id != artifact.artifact_id:
            raise ProvenanceError("receipt artifact_id does not match artifact")
        if not receipt.verifier_id.strip():
            raise ProvenanceError("verifier_id must be non-empty")
        if receipt.issued_epoch < 0 or current_epoch < 0:
            raise ProvenanceError("epochs must be >= 0")
        if receipt.issued_epoch > current_epoch:
            raise ProvenanceError("receipt is from the future")
        if receipt.expires_epoch is not None and current_epoch > receipt.expires_epoch:
            raise ProvenanceError("receipt expired")
        illegal_clear = receipt.cleared_taints & PROTECTED_TAINTS
        if illegal_clear:
            raise ProvenanceError(
                "receipt cannot clear protected taints: "
                + ",".join(sorted(t.value for t in illegal_clear))
            )

        assurances = frozenset(set(artifact.assurances) | set(receipt.added_assurances))
        taints = set(artifact.taints) - set(receipt.cleared_taints)
        if "verified" in assurances:
            taints.discard(Taint.UNVERIFIED)

        fields = dict(
            payload_digest=artifact.payload_digest,
            operation_id=artifact.operation_id,
            parent_ids=artifact.parent_ids,
            root_origins=artifact.root_origins,
            authority_floor=artifact.authority_floor,
            assurances=assurances,
            taints=frozenset(taints),
            created_epoch=artifact.created_epoch,
            metadata=artifact.metadata,
            applied_receipts=artifact.applied_receipts + (receipt.receipt_id,),
        )
        return Artifact(artifact_id=compute_artifact_id(**fields), **fields)

    def release_decision(
        self,
        artifact: Artifact,
        policy: ReleasePolicy,
        *,
        current_epoch: int,
    ) -> ReleaseDecision:
        self.assert_integrity(artifact)
        if current_epoch < 0:
            raise ProvenanceError("current_epoch must be >= 0")
        reasons: set[str] = set()

        if artifact.authority_floor < policy.min_authority_rank:
            reasons.add("AUTHORITY_BELOW_MINIMUM")

        missing = policy.required_assurances - artifact.assurances
        for tag in missing:
            reasons.add(f"MISSING_ASSURANCE:{tag}")

        forbidden_present = policy.forbidden_taints & artifact.taints
        for taint in forbidden_present:
            reasons.add(f"FORBIDDEN_TAINT:{taint.value}")

        if policy.allowed_root_origins is not None:
            disallowed = set(artifact.root_origins) - set(policy.allowed_root_origins)
            for origin in disallowed:
                reasons.add(f"DISALLOWED_ROOT:{origin}")

        if policy.max_age_epochs is not None:
            if policy.max_age_epochs < 0:
                raise ProvenanceError("max_age_epochs must be >= 0")
            age = current_epoch - artifact.created_epoch
            if age < 0:
                reasons.add("ARTIFACT_FROM_FUTURE")
            elif age > policy.max_age_epochs:
                reasons.add("ARTIFACT_STALE")

        if policy.require_deterministic_lineage and Taint.NONDETERMINISTIC in artifact.taints:
            reasons.add("NONDETERMINISTIC_LINEAGE")

        ordered = tuple(sorted(reasons))
        return ReleaseDecision(
            allowed=not ordered,
            state="ALLOW" if not ordered else "FREEZE",
            reason_codes=ordered,
            artifact_id=artifact.artifact_id,
            policy_id=policy.policy_id,
        )

    def assert_integrity(self, artifact: Artifact) -> None:
        expected = compute_artifact_id(
            payload_digest=artifact.payload_digest,
            operation_id=artifact.operation_id,
            parent_ids=artifact.parent_ids,
            root_origins=artifact.root_origins,
            authority_floor=artifact.authority_floor,
            assurances=artifact.assurances,
            taints=artifact.taints,
            created_epoch=artifact.created_epoch,
            metadata=artifact.metadata,
            applied_receipts=artifact.applied_receipts,
        )
        if artifact.artifact_id != expected:
            raise IntegrityError("artifact identity mismatch")
        if artifact.artifact_id in artifact.parent_ids:
            raise IntegrityError("direct self-cycle detected")
        if artifact.authority_floor < 0:
            raise IntegrityError("authority_floor must be >= 0")
        if artifact.created_epoch < 0:
            raise IntegrityError("created_epoch must be >= 0")
        if tuple(sorted(set(artifact.root_origins))) != artifact.root_origins:
            raise IntegrityError("root_origins must be sorted and unique")
        if tuple(sorted(artifact.metadata)) != artifact.metadata:
            raise IntegrityError("metadata must be canonicalized")

    @staticmethod
    def _validate_source_spec(spec: SourceSpec) -> None:
        if spec.authority_rank < 0:
            raise ProvenanceError("authority_rank must be >= 0")
        if spec.epoch < 0:
            raise ProvenanceError("epoch must be >= 0")
        if not spec.source_kind.strip():
            raise ProvenanceError("source_kind must be non-empty")
