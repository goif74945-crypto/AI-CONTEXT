from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Optional

from .canonical import canonical_json, sha256_hex


GENESIS_HASH = "0" * 64


@dataclass(frozen=True, slots=True)
class JournalEvent:
    sequence: int
    logical_tick: int
    event_type: str
    lease_id: str
    payload_hash: str
    previous_hash: str
    record_hash: str

    def unsigned_dict(self) -> dict[str, object]:
        return {
            "sequence": self.sequence,
            "logical_tick": self.logical_tick,
            "event_type": self.event_type,
            "lease_id": self.lease_id,
            "payload_hash": self.payload_hash,
            "previous_hash": self.previous_hash,
        }


class HashChainJournal:
    def __init__(self) -> None:
        self._events: list[JournalEvent] = []

    @property
    def events(self) -> tuple[JournalEvent, ...]:
        return tuple(self._events)

    def append(self, *, logical_tick: int, event_type: str, lease_id: str, payload: object) -> JournalEvent:
        if logical_tick < 0:
            raise ValueError("logical_tick must be >= 0")
        if not event_type or not lease_id:
            raise ValueError("event_type and lease_id are required")
        previous_hash = self._events[-1].record_hash if self._events else GENESIS_HASH
        payload_hash = sha256_hex(canonical_json(payload))
        event = JournalEvent(
            sequence=len(self._events),
            logical_tick=logical_tick,
            event_type=event_type,
            lease_id=lease_id,
            payload_hash=payload_hash,
            previous_hash=previous_hash,
            record_hash="",
        )
        record_hash = sha256_hex(canonical_json(event.unsigned_dict()))
        event = replace(event, record_hash=record_hash)
        self._events.append(event)
        return event

    @staticmethod
    def verify(events: Iterable[JournalEvent]) -> bool:
        previous_hash = GENESIS_HASH
        for expected_sequence, event in enumerate(events):
            if event.sequence != expected_sequence:
                return False
            if event.previous_hash != previous_hash:
                return False
            expected_hash = sha256_hex(canonical_json(event.unsigned_dict()))
            if event.record_hash != expected_hash:
                return False
            previous_hash = event.record_hash
        return True
