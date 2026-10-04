from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Iterable

from .uncertainty import EpistemicStatus


class CompileError(ValueError):
    """Raised for malformed output compilation input."""


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_ref: str
    claim_id: str
    evidence_class: int
    passed: bool
    target_version: str


@dataclass(frozen=True)
class ClaimArtifact:
    claim_id: str
    text: str
    authority_digest: str
    uncertainty_status: EpistemicStatus
    target_version: str
    evidence_class_required: int
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class CompileResult:
    status: str
    output: str | None
    freeze_code: str | None
    blockers: tuple[str, ...]
    digest: str


class ProofCarryingOutputCompiler:
    """Releases user-visible output only from trusted seals and bound proof records."""

    def compile(
        self,
        claims: Iterable[ClaimArtifact],
        *,
        trusted_authority_digests: frozenset[str],
        evidence_catalog: Iterable[EvidenceRecord],
    ) -> CompileResult:
        items = list(claims)
        if not items:
            raise CompileError("at least one claim is required")
        if any(not digest.strip() for digest in trusted_authority_digests):
            raise CompileError("trusted authority digest cannot be empty")

        evidence_by_ref: dict[str, EvidenceRecord] = {}
        for record in evidence_catalog:
            self._validate_evidence(record)
            if record.evidence_ref in evidence_by_ref:
                raise CompileError(f"duplicate evidence_ref: {record.evidence_ref}")
            evidence_by_ref[record.evidence_ref] = record

        seen: set[str] = set()
        blockers: list[str] = []
        referenced_records: dict[str, EvidenceRecord] = {}

        for claim in items:
            self._validate_claim(claim)
            if claim.claim_id in seen:
                raise CompileError(f"duplicate claim_id: {claim.claim_id}")
            seen.add(claim.claim_id)

            if claim.authority_digest not in trusted_authority_digests:
                blockers.append(f"{claim.claim_id}:AUTHORITY_DIGEST_UNTRUSTED")
            if claim.uncertainty_status != EpistemicStatus.PASS:
                blockers.append(
                    f"{claim.claim_id}:EPISTEMIC_{claim.uncertainty_status.value}"
                )

            valid_classes: list[int] = []
            if len(set(claim.evidence_refs)) != len(claim.evidence_refs):
                blockers.append(f"{claim.claim_id}:EVIDENCE_REF_DUPLICATE")
            for ref in claim.evidence_refs:
                record = evidence_by_ref.get(ref)
                if record is None:
                    blockers.append(f"{claim.claim_id}:EVIDENCE_REF_UNKNOWN:{ref}")
                    continue
                referenced_records[ref] = record
                if record.claim_id != claim.claim_id:
                    blockers.append(f"{claim.claim_id}:EVIDENCE_BINDING_MISMATCH:{ref}")
                    continue
                if record.target_version != claim.target_version:
                    blockers.append(f"{claim.claim_id}:EVIDENCE_TARGET_MISMATCH:{ref}")
                    continue
                if not record.passed:
                    blockers.append(f"{claim.claim_id}:EVIDENCE_FAILED:{ref}")
                    continue
                valid_classes.append(record.evidence_class)

            observed = max(valid_classes, default=0)
            if claim.evidence_class_required > 0 and not claim.evidence_refs:
                blockers.append(f"{claim.claim_id}:EVIDENCE_REF_MISSING")
            if observed < claim.evidence_class_required:
                blockers.append(
                    f"{claim.claim_id}:EVIDENCE_E{observed}_LT_E{claim.evidence_class_required}"
                )

        canonical = {
            "claims": [self._canonical_claim(c) for c in sorted(items, key=lambda c: c.claim_id)],
            "evidence": [
                self._canonical_evidence(referenced_records[ref])
                for ref in sorted(referenced_records)
            ],
        }
        digest = hashlib.sha256(
            json.dumps(
                canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()

        if blockers:
            return CompileResult(
                status="FREEZE",
                output=None,
                freeze_code="PCOC_UNPROVEN_CLAIM",
                blockers=tuple(sorted(set(blockers))),
                digest=digest,
            )

        output = "\n".join(c.text for c in sorted(items, key=lambda c: c.claim_id))
        return CompileResult(
            status="PASS",
            output=output,
            freeze_code=None,
            blockers=(),
            digest=digest,
        )

    @staticmethod
    def _validate_claim(claim: ClaimArtifact) -> None:
        if not claim.claim_id.strip():
            raise CompileError("claim_id is empty")
        if not claim.text.strip():
            raise CompileError(f"claim {claim.claim_id}: text is empty")
        if not claim.authority_digest.strip():
            raise CompileError(f"claim {claim.claim_id}: authority_digest is empty")
        if not claim.target_version.strip():
            raise CompileError(f"claim {claim.claim_id}: target_version is empty")
        if not 0 <= claim.evidence_class_required <= 7:
            raise CompileError("evidence class must be in E0..E7")
        if any(not ref.strip() for ref in claim.evidence_refs):
            raise CompileError(f"claim {claim.claim_id}: empty evidence reference")

    @staticmethod
    def _validate_evidence(record: EvidenceRecord) -> None:
        if not record.evidence_ref.strip():
            raise CompileError("evidence_ref is empty")
        if not record.claim_id.strip():
            raise CompileError(f"evidence {record.evidence_ref}: claim_id is empty")
        if not 0 <= record.evidence_class <= 7:
            raise CompileError(f"evidence {record.evidence_ref}: invalid evidence class")
        if not record.target_version.strip():
            raise CompileError(f"evidence {record.evidence_ref}: target_version is empty")

    @staticmethod
    def _canonical_claim(claim: ClaimArtifact) -> dict[str, object]:
        return {
            "claim_id": claim.claim_id,
            "text": claim.text,
            "authority_digest": claim.authority_digest,
            "uncertainty_status": claim.uncertainty_status.value,
            "target_version": claim.target_version,
            "evidence_class_required": claim.evidence_class_required,
            "evidence_refs": list(claim.evidence_refs),
        }

    @staticmethod
    def _canonical_evidence(record: EvidenceRecord) -> dict[str, object]:
        return {
            "evidence_ref": record.evidence_ref,
            "claim_id": record.claim_id,
            "evidence_class": record.evidence_class,
            "passed": record.passed,
            "target_version": record.target_version,
        }
