from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from .codec import canonical_json, sha256_hex
from .errors import WireContractError

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_PROTOCOL_VERSION = "nexy.wire.v1"


class Direction(StrEnum):
    PROVIDER_TO_CORE = "provider_to_core"
    CORE_TO_PROVIDER = "core_to_provider"


class EventType(StrEnum):
    STREAM_OPEN = "stream.open"
    MESSAGE_START = "message.start"
    TEXT_DELTA = "text.delta"
    MESSAGE_END = "message.end"
    TOOL_CALL_START = "tool.call.start"
    TOOL_ARGUMENT_DELTA = "tool.argument.delta"
    TOOL_CALL_END = "tool.call.end"
    TOOL_RESULT = "tool.result"
    USAGE = "usage"
    REFUSAL = "refusal"
    ERROR = "error"
    STREAM_CLOSE = "stream.close"


@dataclass(frozen=True, slots=True)
class SourceRef:
    provider: str
    model: str | None = None
    request_id: str | None = None

    def __post_init__(self) -> None:
        _validate_id("provider", self.provider)
        if self.model is not None:
            _validate_id("model", self.model)
        if self.request_id is not None:
            _validate_id("request_id", self.request_id)

    def to_dict(self) -> dict[str, str]:
        out = {"provider": self.provider}
        if self.model is not None:
            out["model"] = self.model
        if self.request_id is not None:
            out["request_id"] = self.request_id
        return out


def _validate_id(name: str, value: str) -> None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise WireContractError("INVALID_ID", f"{name} must match {_ID_RE.pattern}")


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_json(nested) for key, nested in value.items()})
    if isinstance(value, list | tuple):
        return tuple(_freeze_json(nested) for nested in value)
    return value


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(nested) for nested in value]
    return value


def _freeze_mapping(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    canonical_json(payload)
    return _freeze_json(payload)


@dataclass(frozen=True, slots=True)
class CanonicalEvent:
    stream_id: str
    sequence: int
    event_type: EventType
    direction: Direction
    source: SourceRef
    payload: Mapping[str, Any] = field(default_factory=dict)
    message_id: str | None = None
    tool_call_id: str | None = None
    raw_digest: str | None = None
    protocol_version: str = _PROTOCOL_VERSION

    def __post_init__(self) -> None:
        _validate_id("stream_id", self.stream_id)
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool) or self.sequence < 0:
            raise WireContractError("INVALID_SEQUENCE", "sequence must be a non-negative integer")
        if self.protocol_version != _PROTOCOL_VERSION:
            raise WireContractError("UNSUPPORTED_PROTOCOL", f"expected {_PROTOCOL_VERSION}")
        if self.message_id is not None:
            _validate_id("message_id", self.message_id)
        if self.tool_call_id is not None:
            _validate_id("tool_call_id", self.tool_call_id)
        if self.raw_digest is not None and not re.fullmatch(r"[0-9a-f]{64}", self.raw_digest):
            raise WireContractError("INVALID_RAW_DIGEST", "raw_digest must be lowercase SHA-256 hex")
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))

    def semantic_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "protocol_version": self.protocol_version,
            "stream_id": self.stream_id,
            "sequence": self.sequence,
            "event_type": self.event_type.value,
            "direction": self.direction.value,
            "source": self.source.to_dict(),
            "payload": _thaw_json(self.payload),
        }
        if self.message_id is not None:
            out["message_id"] = self.message_id
        if self.tool_call_id is not None:
            out["tool_call_id"] = self.tool_call_id
        if self.raw_digest is not None:
            out["raw_digest"] = self.raw_digest
        return out

    def fingerprint(self) -> str:
        return sha256_hex(canonical_json(self.semantic_dict()))
