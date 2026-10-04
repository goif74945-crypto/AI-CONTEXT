from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .model import Event, Trace
from .profile import Profile


@dataclass(frozen=True, slots=True, order=True)
class Violation:
    code: str
    severity: str
    message: str
    event_seqs: tuple[int, ...]

    def to_raw(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "event_seqs": list(self.event_seqs),
        }


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    violations: tuple[Violation, ...]

    @property
    def passed(self) -> bool:
        return not self.violations

    def to_raw(self) -> dict[str, object]:
        return {
            "status": "PASS" if self.passed else "FAIL",
            "violations": [v.to_raw() for v in self.violations],
        }


def _sequence_violations(events: tuple[Event, ...]) -> Iterable[Violation]:
    for left, right in zip(events, events[1:]):
        if right.seq <= left.seq:
            yield Violation(
                code="INV_SEQUENCE_STRICT_INCREASE",
                severity="ERROR",
                message=f"seq must strictly increase: {left.seq} -> {right.seq}",
                event_seqs=(left.seq, right.seq),
            )


def _transition_violations(events: tuple[Event, ...], profile: Profile) -> Iterable[Violation]:
    for event in events:
        if event.kind != profile.transition_kind:
            continue
        if event.state_from is None or event.state_to is None:
            yield Violation(
                code="INV_TRANSITION_SHAPE",
                severity="ERROR",
                message="transition event requires state_from and state_to",
                event_seqs=(event.seq,),
            )
            continue
        pair = (event.state_from, event.state_to)
        if pair not in profile.allowed_transitions:
            yield Violation(
                code="INV_FSM_TRANSITION",
                severity="CRITICAL",
                message=f"transition not allowed by profile: {pair[0]} -> {pair[1]}",
                event_seqs=(event.seq,),
            )
        if event.state_to == profile.freeze_state and not event.incident_id:
            yield Violation(
                code="INV_FREEZE_INCIDENT_LINK",
                severity="CRITICAL",
                message="FREEZE transition must carry incident_id",
                event_seqs=(event.seq,),
            )
        if event.state_from == profile.stop_state:
            yield Violation(
                code="INV_STOP_TERMINAL",
                severity="CRITICAL",
                message="STOP is terminal; transition out of STOP is forbidden",
                event_seqs=(event.seq,),
            )


def _release_after_freeze(events: tuple[Event, ...], profile: Profile) -> Iterable[Violation]:
    freeze_by_scope: dict[tuple[str, str | None], Event] = {}
    for event in events:
        scope = (event.trace_id, event.run_id)
        if (
            event.kind == profile.transition_kind
            and event.state_to == profile.freeze_state
        ):
            freeze_by_scope.setdefault(scope, event)
            continue
        if event.kind in profile.release_kinds and scope in freeze_by_scope:
            frozen = freeze_by_scope[scope]
            yield Violation(
                code="INV_RELEASE_AFTER_FREEZE",
                severity="CRITICAL",
                message="release occurred after FREEZE in the same trace/run scope",
                event_seqs=(frozen.seq, event.seq),
            )


def _idempotency_violations(events: tuple[Event, ...], profile: Profile) -> Iterable[Violation]:
    first_by_key: dict[str, Event] = {}
    for event in events:
        if event.kind != profile.execution_start_kind or not event.idempotency_key:
            continue
        first = first_by_key.get(event.idempotency_key)
        if first is None:
            first_by_key[event.idempotency_key] = event
            continue
        if first.run_id != event.run_id:
            yield Violation(
                code="INV_IDEMPOTENCY_REUSE",
                severity="CRITICAL",
                message=(
                    "one idempotency_key started multiple run_ids: "
                    f"{first.run_id!r} vs {event.run_id!r}"
                ),
                event_seqs=(first.seq, event.seq),
            )


def analyze_events(events: Iterable[Event], profile: Profile) -> AnalysisResult:
    frozen = tuple(events)
    violations = [
        *_sequence_violations(frozen),
        *_transition_violations(frozen, profile),
        *_release_after_freeze(frozen, profile),
        *_idempotency_violations(frozen, profile),
    ]
    violations.sort(key=lambda v: (v.code, v.event_seqs, v.message))
    return AnalysisResult(tuple(violations))


def analyze_trace(trace: Trace, profile: Profile) -> AnalysisResult:
    return analyze_events(trace.events, profile)
