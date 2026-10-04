from __future__ import annotations

from dataclasses import replace

from .canonical import sha256_hex
from .model import CommitmentState, LedgerEvent


GENESIS = "0" * 64


def append_event(
    ledger: tuple[LedgerEvent, ...],
    *,
    commitment_id: str,
    revision: int,
    event_type: str,
    state: CommitmentState,
    payload: dict[str, str] | None = None,
) -> tuple[LedgerEvent, ...]:
    previous_hash = ledger[-1].event_hash if ledger else GENESIS
    sequence = len(ledger) + 1
    base = {
        "sequence": sequence,
        "commitment_id": commitment_id,
        "revision": revision,
        "event_type": event_type,
        "state": state.value,
        "payload": payload or {},
        "previous_hash": previous_hash,
    }
    event_hash = sha256_hex(base)
    event = LedgerEvent(
        sequence=sequence,
        commitment_id=commitment_id,
        revision=revision,
        event_type=event_type,
        state=state,
        payload=payload or {},
        previous_hash=previous_hash,
        event_hash=event_hash,
    )
    return ledger + (event,)


def verify_ledger(ledger: tuple[LedgerEvent, ...]) -> bool:
    previous = GENESIS
    for expected_sequence, event in enumerate(ledger, start=1):
        if event.sequence != expected_sequence:
            return False
        if event.previous_hash != previous:
            return False
        base = {
            "sequence": event.sequence,
            "commitment_id": event.commitment_id,
            "revision": event.revision,
            "event_type": event.event_type,
            "state": event.state.value,
            "payload": dict(event.payload),
            "previous_hash": event.previous_hash,
        }
        if sha256_hex(base) != event.event_hash:
            return False
        previous = event.event_hash
    return True


def tamper_event(ledger: tuple[LedgerEvent, ...], index: int, *, event_type: str) -> tuple[LedgerEvent, ...]:
    items = list(ledger)
    items[index] = replace(items[index], event_type=event_type)
    return tuple(items)
