from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .errors import ValidationError

_ALLOWED_EVENT_FIELDS = {
    "seq",
    "kind",
    "trace_id",
    "request_id",
    "run_id",
    "idempotency_key",
    "state_from",
    "state_to",
    "incident_id",
    "metadata",
}


def _required_nonempty_string(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"event.{key} must be a non-empty string")
    return value


def _optional_string(raw: Mapping[str, Any], key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"event.{key} must be null or a non-empty string")
    return value


@dataclass(frozen=True, slots=True)
class Event:
    seq: int
    kind: str
    trace_id: str
    request_id: str
    run_id: str | None = None
    idempotency_key: str | None = None
    state_from: str | None = None
    state_to: str | None = None
    incident_id: str | None = None
    metadata: Mapping[str, Any] | None = None

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any]) -> "Event":
        if not isinstance(raw, Mapping):
            raise ValidationError("each event must be an object")
        unknown = set(raw) - _ALLOWED_EVENT_FIELDS
        if unknown:
            raise ValidationError(
                "unknown event fields: " + ", ".join(sorted(str(x) for x in unknown))
            )
        seq = raw.get("seq")
        if isinstance(seq, bool) or not isinstance(seq, int) or seq < 0:
            raise ValidationError("event.seq must be an integer >= 0")
        metadata = raw.get("metadata")
        if metadata is not None and not isinstance(metadata, Mapping):
            raise ValidationError("event.metadata must be an object or null")
        return cls(
            seq=seq,
            kind=_required_nonempty_string(raw, "kind"),
            trace_id=_required_nonempty_string(raw, "trace_id"),
            request_id=_required_nonempty_string(raw, "request_id"),
            run_id=_optional_string(raw, "run_id"),
            idempotency_key=_optional_string(raw, "idempotency_key"),
            state_from=_optional_string(raw, "state_from"),
            state_to=_optional_string(raw, "state_to"),
            incident_id=_optional_string(raw, "incident_id"),
            metadata=dict(metadata) if metadata is not None else None,
        )

    def to_raw(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "seq": self.seq,
            "kind": self.kind,
            "trace_id": self.trace_id,
            "request_id": self.request_id,
        }
        for key in (
            "run_id",
            "idempotency_key",
            "state_from",
            "state_to",
            "incident_id",
        ):
            value = getattr(self, key)
            if value is not None:
                out[key] = value
        if self.metadata is not None:
            out["metadata"] = dict(self.metadata)
        return out


@dataclass(frozen=True, slots=True)
class Trace:
    schema_version: str
    events: tuple[Event, ...]

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any]) -> "Trace":
        if not isinstance(raw, Mapping):
            raise ValidationError("trace must be an object")
        unknown = set(raw) - {"schema_version", "events"}
        if unknown:
            raise ValidationError(
                "unknown trace fields: " + ", ".join(sorted(str(x) for x in unknown))
            )
        schema_version = raw.get("schema_version")
        if schema_version != "nfwm.trace.v1":
            raise ValidationError("trace.schema_version must equal 'nfwm.trace.v1'")
        events_raw = raw.get("events")
        if not isinstance(events_raw, Sequence) or isinstance(events_raw, (str, bytes)):
            raise ValidationError("trace.events must be an array")
        return cls(
            schema_version=schema_version,
            events=tuple(Event.from_raw(e) for e in events_raw),
        )

    def to_raw(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "events": [event.to_raw() for event in self.events],
        }
