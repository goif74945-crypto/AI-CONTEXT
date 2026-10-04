from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .canonical import ZERO_HASH, sha256_hex
from .model import (
    AuthorityRef,
    Capsule,
    Event,
    EventKind,
    TerminalState,
    authority_fingerprint,
    normalize_authority_refs,
)


@dataclass(slots=True)
class CapsuleBuilder:
    project_target: str
    authority_refs: tuple[AuthorityRef, ...]
    _events: list[Event] = field(default_factory=list)

    def __init__(self, *, project_target: str, authority_refs: Iterable[AuthorityRef]) -> None:
        self.project_target = project_target
        self.authority_refs = normalize_authority_refs(authority_refs)
        self._events = []

    @property
    def fingerprint(self) -> str:
        return authority_fingerprint(self.authority_refs)

    @property
    def next_sequence(self) -> int:
        return len(self._events)

    @property
    def previous_hash(self) -> str:
        return self._events[-1].event_hash if self._events else ZERO_HASH

    def append(self, kind: EventKind | str, payload: dict[str, Any]) -> Event:
        event = Event.create(
            sequence=self.next_sequence,
            kind=kind,
            payload=payload,
            prev_hash=self.previous_hash,
        )
        self._events.append(event)
        return event

    def append_authority_resolved(self, *, mode: str = "EXPLICIT") -> Event:
        return self.append(
            EventKind.AUTHORITY_RESOLVED,
            {"fingerprint": self.fingerprint, "mode": mode},
        )

    def append_final(
        self,
        *,
        status: TerminalState | str,
        output: Any = None,
        reason: str | None = None,
    ) -> Event:
        state = TerminalState(status)
        payload: dict[str, Any] = {
            "status": state.value,
            "output": output,
            "output_digest": sha256_hex(output),
        }
        if reason is not None:
            payload["reason"] = reason
        return self.append(EventKind.FINAL, payload)

    def build(self, *, terminal_state: TerminalState | str) -> Capsule:
        return Capsule(
            project_target=self.project_target,
            authority_refs=self.authority_refs,
            authority_fingerprint=self.fingerprint,
            events=tuple(self._events),
            terminal_state=TerminalState(terminal_state),
        )
