from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .canonical import approval_binding as compute_approval_binding
from .canonical import chained_hash, sha256_hex
from .model import (
    ActionKind,
    AppliedEvent,
    CommitDecision,
    DecisionStatus,
    DirectiveEvent,
    DirectiveOperation,
    DirectiveState,
    EngineStatus,
    JournalKind,
    JournalRecord,
    PreparedAction,
    ProtocolError,
    validate_event_shape,
)


class DirectiveEpochFirewall:
    """Deterministic reference engine for directive supersession safety.

    It consumes structured events. Natural-language interpretation, identity,
    signatures, authorization, persistence, and tool execution belong outside
    this reference core.
    """

    ZERO_HASH = "0" * 64

    def __init__(self) -> None:
        self._state = DirectiveState()
        self._events_by_id: dict[str, str] = {}
        self._applied: list[AppliedEvent] = []
        self._journal: list[JournalRecord] = []
        self._journal_head = self.ZERO_HASH

    @property
    def state(self) -> DirectiveState:
        return self._state

    @property
    def applied_events(self) -> tuple[AppliedEvent, ...]:
        return tuple(self._applied)

    @property
    def journal(self) -> tuple[JournalRecord, ...]:
        return tuple(self._journal)

    @property
    def journal_head(self) -> str:
        return self._journal_head

    def _record(self, kind: JournalKind, payload: dict, outcome_code: str) -> JournalRecord:
        material = {
            "index": len(self._journal),
            "kind": kind.value,
            "payload": payload,
            "outcome_code": outcome_code,
            "resulting_state_hash": self._state.state_hash,
            "previous_record_hash": self._journal_head,
        }
        record_hash = sha256_hex(material)
        record = JournalRecord(
            index=material["index"],
            kind=kind,
            payload=payload,
            outcome_code=outcome_code,
            resulting_state_hash=material["resulting_state_hash"],
            previous_record_hash=self._journal_head,
            record_hash=record_hash,
        )
        self._journal.append(record)
        self._journal_head = record_hash
        return record

    def _freeze(self, code: str) -> DirectiveState:
        self._state = replace(self._state, status=EngineStatus.FROZEN, freeze_reason=code)
        return self._state

    def _freeze_directive(self, event: DirectiveEvent, digest: str, code: str) -> DirectiveState:
        self._freeze(code)
        self._applied.append(AppliedEvent(event, digest, self._state.state_hash))
        self._record(JournalKind.DIRECTIVE, event.normalized(), code)
        return self._state

    def _require_expected_epoch(self, event: DirectiveEvent) -> bool:
        return event.expected_epoch == self._state.epoch

    def apply(self, event: DirectiveEvent) -> DirectiveState:
        validate_event_shape(event)
        digest = event.digest

        previous_digest = self._events_by_id.get(event.event_id)
        if previous_digest is not None:
            if previous_digest == digest:
                self._record(JournalKind.DIRECTIVE, event.normalized(), "IDEMPOTENT_DUPLICATE")
                return self._state
            return self._freeze_directive(event, digest, "EVENT_ID_REUSE_WITH_DIFFERENT_CONTENT")

        if self._state.status is EngineStatus.FROZEN:
            raise ProtocolError("engine is FROZEN; use recover_with_replacement")

        if event.operation is DirectiveOperation.NEW:
            if self._state.status not in (EngineStatus.EMPTY, EngineStatus.REVOKED):
                return self._freeze_directive(event, digest, "NEW_WHILE_DIRECTIVE_ACTIVE")
            next_state = self._activate(event)

        elif event.operation is DirectiveOperation.REPLACE:
            if self._state.status is not EngineStatus.ACTIVE:
                return self._freeze_directive(event, digest, "REPLACE_WITHOUT_ACTIVE_DIRECTIVE")
            if not self._require_expected_epoch(event):
                return self._freeze_directive(event, digest, "EXPECTED_EPOCH_MISMATCH")
            next_state = self._activate(event)

        elif event.operation is DirectiveOperation.NARROW:
            if self._state.status is not EngineStatus.ACTIVE:
                return self._freeze_directive(event, digest, "NARROW_WITHOUT_ACTIVE_DIRECTIVE")
            if not self._require_expected_epoch(event):
                return self._freeze_directive(event, digest, "EXPECTED_EPOCH_MISMATCH")
            old = set(self._state.allowed_actions)
            new = set(event.allowed_actions)
            if not new.issubset(old):
                return self._freeze_directive(event, digest, "NARROW_ATTEMPTED_SCOPE_EXPANSION")
            next_state = self._activate(event)

        elif event.operation is DirectiveOperation.REVOKE:
            if self._state.status not in (EngineStatus.ACTIVE, EngineStatus.REVOKED):
                return self._freeze_directive(event, digest, "REVOKE_WITHOUT_ACTIVE_DIRECTIVE")
            if event.expected_epoch is not None and not self._require_expected_epoch(event):
                return self._freeze_directive(event, digest, "EXPECTED_EPOCH_MISMATCH")
            next_epoch = self._state.epoch + 1
            lineage = chained_hash(self._state.lineage_hash, digest, next_epoch)
            next_state = DirectiveState(
                epoch=next_epoch,
                status=EngineStatus.REVOKED,
                active_directive_id=None,
                directive_hash="",
                lineage_hash=lineage,
                allowed_actions=(),
                constraints={},
                freeze_reason=None,
            )
        else:  # pragma: no cover
            raise ProtocolError(f"unsupported operation: {event.operation}")

        self._state = next_state
        self._events_by_id[event.event_id] = digest
        self._applied.append(AppliedEvent(event, digest, self._state.state_hash))
        self._record(JournalKind.DIRECTIVE, event.normalized(), "APPLIED")
        return self._state

    def _activate(self, event: DirectiveEvent) -> DirectiveState:
        next_epoch = self._state.epoch + 1
        lineage = chained_hash(self._state.lineage_hash, event.digest, next_epoch)
        return DirectiveState(
            epoch=next_epoch,
            status=EngineStatus.ACTIVE,
            active_directive_id=event.directive_id,
            directive_hash=event.digest,
            lineage_hash=lineage,
            allowed_actions=tuple(sorted(set(event.allowed_actions), key=lambda a: a.value)),
            constraints=dict(event.constraints),
            freeze_reason=None,
        )

    def prepare_action(
        self,
        action_id: str,
        kind: ActionKind,
        payload: dict,
        *,
        approval_binding: str | None = None,
    ) -> PreparedAction:
        if self._state.status is not EngineStatus.ACTIVE:
            raise ProtocolError("cannot prepare action unless directive state is ACTIVE")
        if kind not in self._state.allowed_actions:
            raise ProtocolError(f"action kind {kind.value} is outside current directive scope")
        digest = PreparedAction.compute_digest(action_id, kind, payload)
        return PreparedAction(
            action_id=action_id,
            kind=kind,
            payload=dict(payload),
            action_digest=digest,
            prepared_epoch=self._state.epoch,
            directive_hash=self._state.directive_hash,
            lineage_hash=self._state.lineage_hash,
            approval_binding=approval_binding,
        )

    def expected_approval_binding(self, action: PreparedAction) -> str:
        return compute_approval_binding(
            action.action_id,
            action.prepared_epoch,
            action.action_digest,
            action.lineage_hash,
        )

    def commit_gate(self, action: PreparedAction) -> CommitDecision:
        def finish(status: DecisionStatus, code: str, reason: str) -> CommitDecision:
            decision = CommitDecision(status, code, reason, self._state.epoch, self._state.state_hash)
            self._record(JournalKind.COMMIT, action.normalized(), code)
            return decision

        state = self._state
        if state.status is EngineStatus.FROZEN:
            return finish(DecisionStatus.FREEZE, "ENGINE_FROZEN", state.freeze_reason or "engine frozen")
        if state.status is EngineStatus.REVOKED:
            self._freeze("DIRECTIVE_REVOKED")
            return finish(DecisionStatus.FREEZE, "DIRECTIVE_REVOKED", "directive was revoked after action preparation")
        if state.status is not EngineStatus.ACTIVE:
            return finish(DecisionStatus.REJECT, "NO_ACTIVE_DIRECTIVE", "no active directive authorizes a commit")

        recomputed = PreparedAction.compute_digest(action.action_id, action.kind, action.payload)
        if recomputed != action.action_digest:
            self._freeze("ACTION_DIGEST_MISMATCH")
            return finish(DecisionStatus.FREEZE, "ACTION_DIGEST_MISMATCH", "prepared action payload was altered")
        if action.prepared_epoch != state.epoch:
            self._freeze("STALE_DIRECTIVE_EPOCH")
            return finish(DecisionStatus.FREEZE, "STALE_DIRECTIVE_EPOCH", "prepared action belongs to a superseded directive epoch")
        if action.directive_hash != state.directive_hash:
            self._freeze("DIRECTIVE_HASH_MISMATCH")
            return finish(DecisionStatus.FREEZE, "DIRECTIVE_HASH_MISMATCH", "prepared action is bound to a different directive")
        if action.lineage_hash != state.lineage_hash:
            self._freeze("AUTHORITY_LINEAGE_MISMATCH")
            return finish(DecisionStatus.FREEZE, "AUTHORITY_LINEAGE_MISMATCH", "authority lineage changed after preparation")
        if action.kind not in state.allowed_actions:
            self._freeze("ACTION_SCOPE_REVOKED")
            return finish(DecisionStatus.FREEZE, "ACTION_SCOPE_REVOKED", "current directive no longer authorizes this action kind")

        if action.kind is ActionKind.IRREVERSIBLE_WRITE:
            expected = self.expected_approval_binding(action)
            if action.approval_binding != expected:
                return finish(
                    DecisionStatus.REJECT,
                    "EXPLICIT_APPROVAL_REQUIRED",
                    "irreversible action lacks approval bound to this exact action/epoch/lineage",
                )

        return finish(DecisionStatus.ALLOW, "CURRENT_AND_AUTHORIZED", "prepared action matches the current directive epoch and lineage")

    def recover_with_replacement(self, event: DirectiveEvent) -> DirectiveState:
        if self._state.status is not EngineStatus.FROZEN:
            raise ProtocolError("recovery is only legal from FROZEN")
        if event.operation is not DirectiveOperation.REPLACE:
            raise ProtocolError("recovery requires a REPLACE event; stale work is never resumed")
        if event.expected_epoch != self._state.epoch:
            raise ProtocolError("recovery replacement must target the exact frozen epoch")

        digest = event.digest
        previous_digest = self._events_by_id.get(event.event_id)
        if previous_digest is not None and previous_digest != digest:
            raise ProtocolError("recovery event_id collides with different content")
        next_epoch = self._state.epoch + 1
        lineage = chained_hash(self._state.lineage_hash, digest, next_epoch)
        self._state = DirectiveState(
            epoch=next_epoch,
            status=EngineStatus.ACTIVE,
            active_directive_id=event.directive_id,
            directive_hash=digest,
            lineage_hash=lineage,
            allowed_actions=tuple(sorted(set(event.allowed_actions), key=lambda a: a.value)),
            constraints=dict(event.constraints),
            freeze_reason=None,
        )
        self._events_by_id[event.event_id] = digest
        self._applied.append(AppliedEvent(event, digest, self._state.state_hash))
        self._record(JournalKind.RECOVERY, event.normalized(), "RECOVERED_WITH_REPLACEMENT")
        return self._state

    @classmethod
    def replay(cls, events: Iterable[DirectiveEvent]) -> "DirectiveEpochFirewall":
        engine = cls()
        for event in events:
            engine.apply(event)
        return engine

    @classmethod
    def replay_journal(cls, records: Iterable[JournalRecord]) -> "DirectiveEpochFirewall":
        engine = cls()
        for original in records:
            if original.index != len(engine._journal):
                raise ProtocolError("journal index discontinuity")
            if original.previous_record_hash != engine.journal_head:
                raise ProtocolError("journal previous hash mismatch")

            if original.kind is JournalKind.DIRECTIVE:
                event = DirectiveEvent.from_normalized(original.payload)
                engine.apply(event)
            elif original.kind is JournalKind.COMMIT:
                action = PreparedAction.from_normalized(original.payload)
                engine.commit_gate(action)
            elif original.kind is JournalKind.RECOVERY:
                event = DirectiveEvent.from_normalized(original.payload)
                engine.recover_with_replacement(event)
            else:  # pragma: no cover
                raise ProtocolError(f"unsupported journal kind: {original.kind}")

            produced = engine._journal[-1]
            if produced.outcome_code != original.outcome_code:
                raise ProtocolError("journal outcome mismatch")
            if produced.resulting_state_hash != original.resulting_state_hash:
                raise ProtocolError("journal resulting state mismatch")
            if produced.record_hash != original.record_hash:
                raise ProtocolError("journal record hash mismatch")
        return engine
