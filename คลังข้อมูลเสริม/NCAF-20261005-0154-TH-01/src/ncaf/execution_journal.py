from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .common import ContractError, sha256_hex, require_nonempty


class StepState(str, Enum):
    PLANNED = "PLANNED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


_ALLOWED = {
    None: {StepState.PLANNED},
    StepState.PLANNED: {StepState.RUNNING},
    StepState.RUNNING: {StepState.SUCCEEDED, StepState.FAILED},
    StepState.FAILED: {StepState.RUNNING},
    StepState.SUCCEEDED: set(),
}


@dataclass(frozen=True)
class JournalEvent:
    seq: int
    step_id: str
    state: StepState
    idempotency_key: str
    previous_hash: str
    event_hash: str


class ResumableExecutionJournal:
    """Append-only hash-chained step journal with transition and idempotency enforcement."""

    GENESIS = "0" * 64

    def __init__(self, events: Iterable[JournalEvent] = ()): 
        self._events: list[JournalEvent] = []
        self._latest: dict[str, StepState] = {}
        self._keys: dict[str, str] = {}
        for event in events:
            self._replay(event)

    @property
    def events(self) -> tuple[JournalEvent, ...]:
        return tuple(self._events)

    def _payload_hash(self, seq: int, step_id: str, state: StepState, key: str, previous_hash: str) -> str:
        return sha256_hex({
            "seq": seq,
            "step_id": step_id,
            "state": state.value,
            "idempotency_key": key,
            "previous_hash": previous_hash,
        })

    def _replay(self, event: JournalEvent) -> None:
        expected_seq = len(self._events) + 1
        expected_prev = self._events[-1].event_hash if self._events else self.GENESIS
        if event.seq != expected_seq or event.previous_hash != expected_prev:
            raise ContractError("journal sequence/hash chain is invalid")
        if event.event_hash != self._payload_hash(event.seq, event.step_id, event.state, event.idempotency_key, event.previous_hash):
            raise ContractError("journal event hash is invalid")
        self._accept_transition(event.step_id, event.state, event.idempotency_key)
        self._events.append(event)

    def _accept_transition(self, step_id: str, state: StepState, key: str) -> None:
        require_nonempty(step_id, "step_id")
        require_nonempty(key, "idempotency_key")
        old = self._latest.get(step_id)
        if state not in _ALLOWED[old]:
            raise ContractError(f"illegal transition for {step_id}: {old} -> {state}")
        owner = self._keys.get(key)
        if owner is not None and owner != step_id:
            raise ContractError("idempotency key reused by another step")
        self._keys[key] = step_id
        self._latest[step_id] = state

    def append(self, step_id: str, state: StepState, idempotency_key: str) -> JournalEvent:
        # Validate on a copy of mutable state first to avoid partial mutation when rejected.
        old_latest = dict(self._latest)
        old_keys = dict(self._keys)
        try:
            self._accept_transition(step_id, state, idempotency_key)
        except Exception:
            self._latest = old_latest
            self._keys = old_keys
            raise
        seq = len(self._events) + 1
        previous_hash = self._events[-1].event_hash if self._events else self.GENESIS
        event_hash = self._payload_hash(seq, step_id, state, idempotency_key, previous_hash)
        event = JournalEvent(seq, step_id, state, idempotency_key, previous_hash, event_hash)
        self._events.append(event)
        return event

    def resumable_steps(self) -> tuple[str, ...]:
        return tuple(sorted(step for step, state in self._latest.items() if state in {StepState.PLANNED, StepState.RUNNING, StepState.FAILED}))
