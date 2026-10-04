from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import hashlib
import json
from typing import Iterable, Mapping


class AuthorityError(ValueError):
    """Raised when authority provenance is structurally invalid."""


class AuthorityLevel(IntEnum):
    MODEL_PROPOSAL = 10
    EXTERNAL_REFERENCE = 20
    PROJECT_CONTEXT = 30
    CURRENT_SPEC = 40
    CANON = 50
    USER_DIRECTIVE = 60


@dataclass(frozen=True)
class PromotionReceipt:
    receipt_id: str
    from_level: AuthorityLevel
    to_level: AuthorityLevel
    approver_level: AuthorityLevel
    authority_ref: str

    def validate_shape(self) -> None:
        if not self.receipt_id.strip():
            raise AuthorityError("promotion receipt_id is empty")
        if not self.authority_ref.strip():
            raise AuthorityError("promotion authority_ref is empty")
        if self.to_level <= self.from_level:
            raise AuthorityError("promotion must increase authority")
        if self.approver_level < self.to_level:
            raise AuthorityError("promotion approver lacks sufficient authority")


@dataclass(frozen=True)
class AuthorityClaim:
    claim_id: str
    statement: str
    level: AuthorityLevel
    source_ref: str
    parent_claim_id: str | None = None
    promotion_receipt: PromotionReceipt | None = None

    def validate_shape(self) -> None:
        if not self.claim_id.strip():
            raise AuthorityError("claim_id is empty")
        if not self.statement.strip():
            raise AuthorityError(f"claim {self.claim_id}: statement is empty")
        if not self.source_ref.strip():
            raise AuthorityError(f"claim {self.claim_id}: source_ref is empty")


@dataclass(frozen=True)
class SealResult:
    target_claim_id: str
    chain: tuple[str, ...]
    digest: str
    valid: bool


class AuthorityProvenanceSeal:
    """Detects authority laundering and seals a validated claim lineage.

    Caller-provided trusted roots are the only authority anchors. A claim cannot become
    authoritative merely by labelling itself CANON/USER. Upward transitions additionally
    require a receipt anchored to a trusted authority reference.
    """

    def __init__(self, trusted_roots: Mapping[str, AuthorityLevel]) -> None:
        if not trusted_roots:
            raise AuthorityError("trusted_roots cannot be empty")
        normalized: dict[str, AuthorityLevel] = {}
        for source_ref, level in trusted_roots.items():
            if not source_ref.strip():
                raise AuthorityError("trusted root source_ref is empty")
            normalized[source_ref] = AuthorityLevel(level)
        self._trusted_roots = normalized

    def seal(self, claims: Iterable[AuthorityClaim], target_claim_id: str) -> SealResult:
        by_id: dict[str, AuthorityClaim] = {}
        for claim in claims:
            claim.validate_shape()
            if claim.claim_id in by_id:
                raise AuthorityError(f"duplicate claim_id: {claim.claim_id}")
            by_id[claim.claim_id] = claim

        if target_claim_id not in by_id:
            raise AuthorityError(f"unknown target claim: {target_claim_id}")

        chain_ids: list[str] = []
        seen: set[str] = set()
        current = by_id[target_claim_id]

        while True:
            if current.claim_id in seen:
                raise AuthorityError(f"authority lineage cycle at {current.claim_id}")
            seen.add(current.claim_id)
            chain_ids.append(current.claim_id)

            parent_id = current.parent_claim_id
            if parent_id is None:
                if current.promotion_receipt is not None:
                    raise AuthorityError(
                        f"claim {current.claim_id}: root cannot carry a promotion receipt"
                    )
                self._validate_root(current)
                break
            if parent_id not in by_id:
                raise AuthorityError(
                    f"claim {current.claim_id}: missing parent {parent_id}"
                )

            parent = by_id[parent_id]
            if current.level > parent.level:
                receipt = current.promotion_receipt
                if receipt is None:
                    raise AuthorityError(
                        f"claim {current.claim_id}: authority escalation without receipt"
                    )
                self._validate_receipt(receipt, parent.level, current.level)
            elif current.promotion_receipt is not None:
                raise AuthorityError(
                    f"claim {current.claim_id}: receipt present without authority escalation"
                )
            current = parent

        chain_ids.reverse()
        canonical = [self._canonical_claim(by_id[cid]) for cid in chain_ids]
        payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return SealResult(target_claim_id, tuple(chain_ids), digest, True)

    def _validate_root(self, claim: AuthorityClaim) -> None:
        trusted_level = self._trusted_roots.get(claim.source_ref)
        if trusted_level is None:
            raise AuthorityError(
                f"claim {claim.claim_id}: untrusted root source {claim.source_ref}"
            )
        if trusted_level != claim.level:
            raise AuthorityError(
                f"claim {claim.claim_id}: trusted root level mismatch"
            )

    def _validate_receipt(
        self,
        receipt: PromotionReceipt,
        parent_level: AuthorityLevel,
        current_level: AuthorityLevel,
    ) -> None:
        receipt.validate_shape()
        if receipt.from_level != parent_level or receipt.to_level != current_level:
            raise AuthorityError("promotion receipt levels do not match lineage")
        trusted_approver = self._trusted_roots.get(receipt.authority_ref)
        if trusted_approver is None:
            raise AuthorityError("promotion receipt authority_ref is not trusted")
        if trusted_approver < receipt.approver_level:
            raise AuthorityError("promotion receipt overstates trusted approver authority")
        if trusted_approver < current_level:
            raise AuthorityError("trusted approver cannot authorize target authority")

    @staticmethod
    def _canonical_claim(claim: AuthorityClaim) -> Mapping[str, object]:
        receipt = claim.promotion_receipt
        return {
            "claim_id": claim.claim_id,
            "statement": claim.statement,
            "level": int(claim.level),
            "source_ref": claim.source_ref,
            "parent_claim_id": claim.parent_claim_id,
            "promotion_receipt": None
            if receipt is None
            else {
                "receipt_id": receipt.receipt_id,
                "from_level": int(receipt.from_level),
                "to_level": int(receipt.to_level),
                "approver_level": int(receipt.approver_level),
                "authority_ref": receipt.authority_ref,
            },
        }
