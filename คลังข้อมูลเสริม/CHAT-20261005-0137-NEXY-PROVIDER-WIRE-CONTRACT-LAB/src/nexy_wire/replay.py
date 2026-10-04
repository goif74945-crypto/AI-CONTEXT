from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .codec import sha256_hex
from .errors import WireContractError
from .model import CanonicalEvent
from .state import StreamState, StreamValidator

_CHAIN_SEED = sha256_hex(b"NEXY-WIRE-TRANSCRIPT-v1")


@dataclass(frozen=True, slots=True)
class ReplayReport:
    stream_id: str
    event_count: int
    transcript_hash: str
    closed: bool


class TranscriptReplayer:
    def replay(self, events: Iterable[CanonicalEvent]) -> ReplayReport:
        validator = StreamValidator()
        chain = _CHAIN_SEED
        count = 0
        stream_id: str | None = None
        for event in events:
            validator.apply(event)
            stream_id = event.stream_id
            chain = sha256_hex(bytes.fromhex(chain) + bytes.fromhex(event.fingerprint()))
            count += 1
        if stream_id is None:
            raise WireContractError("EMPTY_TRANSCRIPT", "canonical transcript is empty")
        return ReplayReport(
            stream_id=stream_id,
            event_count=count,
            transcript_hash=chain,
            closed=validator.state is StreamState.CLOSED,
        )
