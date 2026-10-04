from __future__ import annotations

from nexy_wire import CanonicalEvent, Direction, EventType, SourceRef

SOURCE = SourceRef(provider="fixture-provider", model="fixture-model", request_id="req-1")


def event(seq: int, kind: EventType, **kwargs) -> CanonicalEvent:
    return CanonicalEvent(
        stream_id="stream-1",
        sequence=seq,
        event_type=kind,
        direction=kwargs.pop("direction", Direction.PROVIDER_TO_CORE),
        source=SOURCE,
        **kwargs,
    )


def valid_text_transcript() -> list[CanonicalEvent]:
    return [
        event(0, EventType.STREAM_OPEN),
        event(1, EventType.MESSAGE_START, message_id="m1"),
        event(2, EventType.TEXT_DELTA, message_id="m1", payload={"text": "hello"}),
        event(3, EventType.TEXT_DELTA, message_id="m1", payload={"text": " world"}),
        event(4, EventType.MESSAGE_END, message_id="m1"),
        event(5, EventType.USAGE, payload={"input_tokens": 3, "output_tokens": 2}),
        event(6, EventType.STREAM_CLOSE),
    ]
