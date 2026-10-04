from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .common import GateDecision, GateStatus, canonical_digest, require_nonempty


@dataclass(frozen=True, slots=True)
class EpochToken:
    session_id: str
    directive_id: str
    epoch: int
    directive_digest: str


@dataclass(frozen=True, slots=True)
class ActionLease:
    session_id: str
    directive_id: str
    epoch: int
    directive_digest: str
    action_digest: str
    lease_digest: str


class InterruptEpochGate:
    """Deterministically invalidates work from superseded user directives.

    No clock is used. A logical epoch advances whenever a directive is replaced or
    cancelled. Any action lease minted under an older epoch becomes invalid.
    """

    def __init__(self, session_id: str) -> None:
        self._session_id = require_nonempty("session_id", session_id)
        self._epoch = 0
        self._active: EpochToken | None = None
        self._committed_leases: set[str] = set()

    @property
    def current_epoch(self) -> int:
        return self._epoch

    @property
    def active_token(self) -> EpochToken | None:
        return self._active

    def begin_directive(self, directive_id: str, directive_payload: Any) -> EpochToken:
        directive_id = require_nonempty("directive_id", directive_id)
        self._epoch += 1
        token = EpochToken(
            session_id=self._session_id,
            directive_id=directive_id,
            epoch=self._epoch,
            directive_digest=canonical_digest(directive_payload),
        )
        self._active = token
        return token

    def cancel_active(self, reason: str) -> GateDecision:
        require_nonempty("reason", reason)
        self._epoch += 1
        previous = self._active
        self._active = None
        return GateDecision(
            GateStatus.PASS,
            "INTERRUPT_CANCELLED",
            "Active directive invalidated by logical epoch advance.",
            canonical_digest({"session": self._session_id, "epoch": self._epoch, "previous": previous, "reason": reason}),
        )

    def validate_token(self, token: EpochToken) -> GateDecision:
        fingerprint = canonical_digest(token)
        if token.session_id != self._session_id:
            return GateDecision(GateStatus.FREEZE, "INTERRUPT_SESSION_MISMATCH", "Token belongs to another session.", fingerprint)
        if self._active is None:
            return GateDecision(GateStatus.FREEZE, "INTERRUPT_NO_ACTIVE_DIRECTIVE", "No directive is currently active.", fingerprint)
        if token != self._active or token.epoch != self._epoch:
            return GateDecision(GateStatus.FREEZE, "INTERRUPT_STALE_EPOCH", "Token was superseded by a newer directive or cancellation.", fingerprint)
        return GateDecision(GateStatus.PASS, "INTERRUPT_EPOCH_CURRENT", "Token matches the current directive epoch.", fingerprint)

    def prepare_action(self, token: EpochToken, action: Any) -> ActionLease:
        decision = self.validate_token(token)
        if not decision.allowed:
            raise RuntimeError(decision.code)
        action_digest = canonical_digest(action)
        lease_material = {
            "session_id": token.session_id,
            "directive_id": token.directive_id,
            "epoch": token.epoch,
            "directive_digest": token.directive_digest,
            "action_digest": action_digest,
        }
        return ActionLease(
            session_id=token.session_id,
            directive_id=token.directive_id,
            epoch=token.epoch,
            directive_digest=token.directive_digest,
            action_digest=action_digest,
            lease_digest=canonical_digest(lease_material),
        )

    def commit_action(self, lease: ActionLease, action: Any) -> GateDecision:
        current = self._active
        fingerprint = canonical_digest({"lease": lease, "action": action})
        if current is None:
            return GateDecision(GateStatus.FREEZE, "INTERRUPT_NO_ACTIVE_DIRECTIVE", "Action cannot commit without an active directive.", fingerprint)
        expected_lease = canonical_digest({
            "session_id": lease.session_id,
            "directive_id": lease.directive_id,
            "epoch": lease.epoch,
            "directive_digest": lease.directive_digest,
            "action_digest": lease.action_digest,
        })
        if expected_lease != lease.lease_digest:
            return GateDecision(GateStatus.FREEZE, "INTERRUPT_LEASE_TAMPERED", "Action lease integrity check failed.", fingerprint)
        if lease.lease_digest in self._committed_leases:
            return GateDecision(GateStatus.REJECT, "INTERRUPT_LEASE_REPLAY", "Action lease is single-use and was already committed.", fingerprint)
        if (
            lease.session_id != current.session_id
            or lease.directive_id != current.directive_id
            or lease.epoch != current.epoch
            or lease.directive_digest != current.directive_digest
            or lease.epoch != self._epoch
        ):
            return GateDecision(GateStatus.FREEZE, "INTERRUPT_STALE_ACTION", "Action was prepared under a superseded directive.", fingerprint)
        if canonical_digest(action) != lease.action_digest:
            return GateDecision(GateStatus.FREEZE, "INTERRUPT_ACTION_CHANGED", "Prepared action changed before commit.", fingerprint)
        self._committed_leases.add(lease.lease_digest)
        return GateDecision(GateStatus.PASS, "INTERRUPT_ACTION_COMMITTED", "Action is current, untampered, and committed once.", fingerprint)
