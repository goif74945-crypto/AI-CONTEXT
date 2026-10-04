from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

from .analyzer import Violation, analyze_events
from .canonical import sha256_canonical
from .model import Event
from .profile import Profile


@dataclass(frozen=True, slots=True)
class Witness:
    violation_code: str
    source_event_count: int
    witness_events: tuple[Event, ...]
    source_hash: str
    witness_hash: str
    minimality: str = "DETERMINISTIC_1_MINIMAL"

    def to_raw(self) -> dict[str, object]:
        return {
            "schema_version": "nfwm.witness.v1",
            "violation_code": self.violation_code,
            "source_event_count": self.source_event_count,
            "witness_event_count": len(self.witness_events),
            "minimality": self.minimality,
            "source_hash": self.source_hash,
            "witness_hash": self.witness_hash,
            "events": [e.to_raw() for e in self.witness_events],
        }


def _partition(items: Sequence[Event], n: int) -> list[list[Event]]:
    length = len(items)
    n = max(1, min(n, length))
    q, r = divmod(length, n)
    chunks: list[list[Event]] = []
    start = 0
    for i in range(n):
        size = q + (1 if i < r else 0)
        end = start + size
        chunks.append(list(items[start:end]))
        start = end
    return [chunk for chunk in chunks if chunk]


def _ddmin(events: Sequence[Event], predicate: Callable[[Sequence[Event]], bool]) -> list[Event]:
    current = list(events)
    if not current or not predicate(current):
        return current

    granularity = 2
    while len(current) >= 2:
        chunks = _partition(current, granularity)
        reduced = False

        for chunk in chunks:
            if predicate(chunk):
                current = chunk
                granularity = 2
                reduced = True
                break
        if reduced:
            continue

        for chunk in chunks:
            chunk_ids = {id(e) for e in chunk}
            complement = [e for e in current if id(e) not in chunk_ids]
            if complement and predicate(complement):
                current = complement
                granularity = max(2, granularity - 1)
                reduced = True
                break
        if reduced:
            continue

        if granularity >= len(current):
            break
        granularity = min(len(current), granularity * 2)

    # Deterministic single-deletion closure ensures 1-minimality.
    changed = True
    while changed and len(current) > 1:
        changed = False
        for index in range(len(current)):
            candidate = current[:index] + current[index + 1 :]
            if candidate and predicate(candidate):
                current = candidate
                changed = True
                break
    return current


def minimize_violation(
    events: Iterable[Event],
    profile: Profile,
    violation_code: str,
) -> Witness:
    source = tuple(events)
    full = analyze_events(source, profile)
    if violation_code not in {v.code for v in full.violations}:
        raise ValueError(f"violation code not present in source trace: {violation_code}")

    def predicate(candidate: Sequence[Event]) -> bool:
        result = analyze_events(candidate, profile)
        return violation_code in {v.code for v in result.violations}

    minimized = tuple(_ddmin(source, predicate))
    source_raw = [e.to_raw() for e in source]
    witness_raw = [e.to_raw() for e in minimized]
    return Witness(
        violation_code=violation_code,
        source_event_count=len(source),
        witness_events=minimized,
        source_hash=sha256_canonical(source_raw),
        witness_hash=sha256_canonical(witness_raw),
    )


def witness_is_one_minimal(witness: Witness, profile: Profile) -> bool:
    events = witness.witness_events
    base = analyze_events(events, profile)
    codes = {v.code for v in base.violations}
    if witness.violation_code not in codes:
        return False
    for index in range(len(events)):
        candidate = events[:index] + events[index + 1 :]
        if not candidate:
            continue
        result = analyze_events(candidate, profile)
        if witness.violation_code in {v.code for v in result.violations}:
            return False
    return True
