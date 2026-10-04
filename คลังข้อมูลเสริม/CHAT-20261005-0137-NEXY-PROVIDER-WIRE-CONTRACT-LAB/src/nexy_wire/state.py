from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .errors import WireContractError
from .model import CanonicalEvent, Direction, EventType


class StreamState(StrEnum):
    NEW = "new"
    OPEN = "open"
    TERMINATING = "terminating"
    CLOSED = "closed"


@dataclass(slots=True)
class _ToolState:
    arguments: list[str] = field(default_factory=list)
    ended: bool = False
    result_seen: bool = False


class StreamValidator:
    """Stateful fail-closed validator for a single canonical provider stream."""

    def __init__(self) -> None:
        self.state = StreamState.NEW
        self.stream_id: str | None = None
        self.next_sequence = 0
        self.messages_open: set[str] = set()
        self.messages_seen: set[str] = set()
        self.tools: dict[str, _ToolState] = {}
        self.usage_seen = False
        self.terminal_reason: EventType | None = None

    def apply(self, event: CanonicalEvent) -> None:
        self._check_identity_and_sequence(event)
        handler = getattr(self, f"_on_{event.event_type.value.replace('.', '_')}")
        handler(event)
        self.next_sequence += 1

    def _check_identity_and_sequence(self, event: CanonicalEvent) -> None:
        if event.sequence != self.next_sequence:
            raise WireContractError(
                "SEQUENCE_GAP",
                f"expected sequence {self.next_sequence}, got {event.sequence}",
                sequence=event.sequence,
            )
        if self.stream_id is not None and event.stream_id != self.stream_id:
            raise WireContractError("STREAM_ID_CHANGED", "stream_id changed mid-stream", sequence=event.sequence)
        if self.state is StreamState.CLOSED:
            raise WireContractError("EVENT_AFTER_CLOSE", "no events allowed after stream.close", sequence=event.sequence)
        if self.state is StreamState.NEW and event.event_type is not EventType.STREAM_OPEN:
            raise WireContractError("OPEN_REQUIRED", "stream.open must be the first event", sequence=event.sequence)
        if self.state is StreamState.TERMINATING and event.event_type is not EventType.STREAM_CLOSE:
            raise WireContractError(
                "TERMINAL_EVENT_REQUIRES_CLOSE",
                "refusal/error must be followed directly by stream.close",
                sequence=event.sequence,
            )

    def _require_provider_direction(self, event: CanonicalEvent) -> None:
        if event.direction is not Direction.PROVIDER_TO_CORE:
            raise WireContractError("DIRECTION_MISMATCH", f"{event.event_type.value} must be provider_to_core", sequence=event.sequence)

    def _on_stream_open(self, event: CanonicalEvent) -> None:
        if self.state is not StreamState.NEW:
            raise WireContractError("DUPLICATE_OPEN", "stream.open may occur only once", sequence=event.sequence)
        self._require_provider_direction(event)
        self.stream_id = event.stream_id
        self.state = StreamState.OPEN

    def _on_message_start(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        mid = self._require_message_id(event)
        if mid in self.messages_seen:
            raise WireContractError("DUPLICATE_MESSAGE", f"message {mid} already seen", sequence=event.sequence)
        self.messages_seen.add(mid)
        self.messages_open.add(mid)

    def _on_text_delta(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        mid = self._require_message_id(event)
        if mid not in self.messages_open:
            raise WireContractError("MESSAGE_NOT_OPEN", f"message {mid} is not open", sequence=event.sequence)
        delta = event.payload.get("text")
        if not isinstance(delta, str) or delta == "":
            raise WireContractError("INVALID_TEXT_DELTA", "text.delta payload.text must be a non-empty string", sequence=event.sequence)

    def _on_message_end(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        mid = self._require_message_id(event)
        if mid not in self.messages_open:
            raise WireContractError("MESSAGE_NOT_OPEN", f"message {mid} is not open", sequence=event.sequence)
        self.messages_open.remove(mid)

    def _on_tool_call_start(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        tid = self._require_tool_id(event)
        if tid in self.tools:
            raise WireContractError("DUPLICATE_TOOL_CALL", f"tool call {tid} already exists", sequence=event.sequence)
        name = event.payload.get("name")
        if not isinstance(name, str) or not name.strip():
            raise WireContractError("INVALID_TOOL_NAME", "tool.call.start payload.name must be non-empty", sequence=event.sequence)
        self.tools[tid] = _ToolState()

    def _on_tool_argument_delta(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        tid = self._require_tool_id(event)
        tool = self._tool(tid, event.sequence)
        if tool.ended:
            raise WireContractError("TOOL_ALREADY_ENDED", f"tool call {tid} already ended", sequence=event.sequence)
        fragment = event.payload.get("fragment")
        if not isinstance(fragment, str):
            raise WireContractError("INVALID_TOOL_FRAGMENT", "tool.argument.delta payload.fragment must be a string", sequence=event.sequence)
        tool.arguments.append(fragment)

    def _on_tool_call_end(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        tid = self._require_tool_id(event)
        tool = self._tool(tid, event.sequence)
        if tool.ended:
            raise WireContractError("TOOL_ALREADY_ENDED", f"tool call {tid} already ended", sequence=event.sequence)
        joined = "".join(tool.arguments)
        try:
            parsed = json.loads(joined or "{}")
        except json.JSONDecodeError as exc:
            raise WireContractError("INVALID_TOOL_JSON", f"tool arguments are not valid JSON: {exc.msg}", sequence=event.sequence) from exc
        if not isinstance(parsed, dict):
            raise WireContractError("TOOL_ARGS_NOT_OBJECT", "tool arguments must decode to a JSON object", sequence=event.sequence)
        tool.ended = True

    def _on_tool_result(self, event: CanonicalEvent) -> None:
        if event.direction is not Direction.CORE_TO_PROVIDER:
            raise WireContractError("DIRECTION_MISMATCH", "tool.result must be core_to_provider", sequence=event.sequence)
        tid = self._require_tool_id(event)
        tool = self._tool(tid, event.sequence)
        if not tool.ended:
            raise WireContractError("TOOL_NOT_ENDED", f"tool call {tid} has not ended", sequence=event.sequence)
        if tool.result_seen:
            raise WireContractError("DUPLICATE_TOOL_RESULT", f"tool call {tid} already has a result", sequence=event.sequence)
        if "result" not in event.payload and "error" not in event.payload:
            raise WireContractError("EMPTY_TOOL_RESULT", "tool.result must contain result or error", sequence=event.sequence)
        tool.result_seen = True

    def _on_usage(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        if self.usage_seen:
            raise WireContractError("DUPLICATE_USAGE", "usage may occur at most once", sequence=event.sequence)
        for key in ("input_tokens", "output_tokens"):
            value = event.payload.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise WireContractError("INVALID_USAGE", f"usage.{key} must be a non-negative integer", sequence=event.sequence)
        self.usage_seen = True

    def _on_refusal(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        reason = event.payload.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise WireContractError("INVALID_REFUSAL", "refusal payload.reason must be non-empty", sequence=event.sequence)
        self._enter_terminal(event)

    def _on_error(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        code = event.payload.get("code")
        if not isinstance(code, str) or not code.strip():
            raise WireContractError("INVALID_ERROR", "error payload.code must be non-empty", sequence=event.sequence)
        self._enter_terminal(event)

    def _enter_terminal(self, event: CanonicalEvent) -> None:
        if self.messages_open:
            raise WireContractError("OPEN_MESSAGE_AT_TERMINAL", "cannot enter terminal state with open messages", sequence=event.sequence)
        if any(not tool.ended for tool in self.tools.values()):
            raise WireContractError("OPEN_TOOL_AT_TERMINAL", "cannot enter terminal state with open tool calls", sequence=event.sequence)
        self.terminal_reason = event.event_type
        self.state = StreamState.TERMINATING

    def _on_stream_close(self, event: CanonicalEvent) -> None:
        self._require_provider_direction(event)
        if self.messages_open:
            raise WireContractError("OPEN_MESSAGE_AT_CLOSE", "cannot close with open messages", sequence=event.sequence)
        if any(not tool.ended for tool in self.tools.values()):
            raise WireContractError("OPEN_TOOL_AT_CLOSE", "cannot close with open tool calls", sequence=event.sequence)
        self.state = StreamState.CLOSED

    def _require_message_id(self, event: CanonicalEvent) -> str:
        if event.message_id is None:
            raise WireContractError("MESSAGE_ID_REQUIRED", f"{event.event_type.value} requires message_id", sequence=event.sequence)
        return event.message_id

    def _require_tool_id(self, event: CanonicalEvent) -> str:
        if event.tool_call_id is None:
            raise WireContractError("TOOL_CALL_ID_REQUIRED", f"{event.event_type.value} requires tool_call_id", sequence=event.sequence)
        return event.tool_call_id

    def _tool(self, tid: str, sequence: int) -> _ToolState:
        try:
            return self.tools[tid]
        except KeyError as exc:
            raise WireContractError("UNKNOWN_TOOL_CALL", f"tool call {tid} not started", sequence=sequence) from exc
