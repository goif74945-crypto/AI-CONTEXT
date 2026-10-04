from __future__ import annotations

import hashlib
import json
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


class NCWError(ValueError):
    """Base fail-closed NCW1 error."""


class ValidationError(NCWError):
    pass


class DecodeError(NCWError):
    pass


class StrictJSONError(NCWError):
    pass


@dataclass(frozen=True, slots=True)
class Policy:
    max_depth: int = 64
    max_container_items: int = 100_000
    max_string_bytes: int = 16 * 1024 * 1024
    max_total_wire_bytes: int = 64 * 1024 * 1024
    max_json_text_bytes: int = 64 * 1024 * 1024

    def __post_init__(self) -> None:
        if self.max_depth < 0:
            raise ValueError("max_depth must be >= 0")
        if self.max_container_items < 0:
            raise ValueError("max_container_items must be >= 0")
        if self.max_string_bytes < 0:
            raise ValueError("max_string_bytes must be >= 0")
        if self.max_total_wire_bytes <= 0 or self.max_json_text_bytes <= 0:
            raise ValueError("byte limits must be > 0")


I128_MIN = -(1 << 127)
I128_MAX = (1 << 127) - 1
MAGIC = b"NCW1"
HASH_DOMAIN = b"NEXY-CANONICAL-WIRE-LAB-v1\x00"
T_NULL, T_FALSE, T_TRUE, T_I128, T_STR, T_LIST, T_MAP = range(7)


def _u32(value: int, context: str) -> bytes:
    if not 0 <= value <= 0xFFFFFFFF:
        raise ValidationError(f"{context} does not fit u32")
    return value.to_bytes(4, "big")


def _text_bytes(value: str, policy: Policy, context: str) -> bytes:
    if unicodedata.normalize("NFC", value) != value:
        raise ValidationError(f"{context} is not NFC-normalized")
    try:
        raw = value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise ValidationError(f"{context} is not valid Unicode scalar text") from exc
    if len(raw) > policy.max_string_bytes:
        raise ValidationError(f"{context} exceeds max_string_bytes")
    return raw


def _enc(value: object, policy: Policy, depth: int) -> bytes:
    if depth > policy.max_depth:
        raise ValidationError("max_depth exceeded")
    if value is None:
        return bytes((T_NULL,))
    if value is False:
        return bytes((T_FALSE,))
    if value is True:
        return bytes((T_TRUE,))
    if isinstance(value, int):
        if not I128_MIN <= value <= I128_MAX:
            raise ValidationError("integer outside signed 128-bit range")
        return bytes((T_I128,)) + value.to_bytes(16, "big", signed=True)
    if isinstance(value, float):
        raise ValidationError("floating point is forbidden")
    if isinstance(value, str):
        raw = _text_bytes(value, policy, "string")
        return bytes((T_STR,)) + _u32(len(raw), "string length") + raw
    if isinstance(value, list):
        if len(value) > policy.max_container_items:
            raise ValidationError("list exceeds max_container_items")
        body = bytearray((T_LIST,)) + bytearray(_u32(len(value), "list count"))
        for child in value:
            body += _enc(child, policy, depth + 1)
        return bytes(body)
    if isinstance(value, Mapping):
        if len(value) > policy.max_container_items:
            raise ValidationError("map exceeds max_container_items")
        entries: list[tuple[bytes, object]] = []
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValidationError("map keys must be strings")
            entries.append((_text_bytes(key, policy, "map key"), child))
        entries.sort(key=lambda pair: pair[0])
        for i in range(1, len(entries)):
            if entries[i - 1][0] == entries[i][0]:
                raise ValidationError("duplicate map key")
        body = bytearray((T_MAP,)) + bytearray(_u32(len(entries), "map count"))
        for key_raw, child in entries:
            body += _u32(len(key_raw), "map key length") + key_raw
            body += _enc(child, policy, depth + 1)
        return bytes(body)
    raise ValidationError(f"unsupported type: {type(value).__name__}")


def encode(value: object, policy: Policy | None = None) -> bytes:
    active = policy or Policy()
    wire = MAGIC + _enc(value, active, 0)
    if len(wire) > active.max_total_wire_bytes:
        raise ValidationError("wire output exceeds max_total_wire_bytes")
    return wire


def canonical_sha256(value: object, policy: Policy | None = None) -> str:
    return hashlib.sha256(HASH_DOMAIN + encode(value, policy)).hexdigest()


def _parse_i128(raw: str) -> int:
    value = int(raw, 10)
    if not I128_MIN <= value <= I128_MAX:
        raise StrictJSONError("JSON integer outside signed 128-bit range")
    return value


def _reject_float(raw: str) -> Any:
    raise StrictJSONError(f"floating-point JSON number forbidden: {raw}")


def _reject_constant(raw: str) -> Any:
    raise StrictJSONError(f"non-standard JSON constant forbidden: {raw}")


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    normalized: dict[str, str] = {}
    for key, value in pairs:
        if key in out:
            raise StrictJSONError(f"duplicate JSON key: {key!r}")
        nfc = unicodedata.normalize("NFC", key)
        prior = normalized.get(nfc)
        if prior is not None and prior != key:
            raise StrictJSONError("JSON keys collide under NFC normalization")
        normalized[nfc] = key
        out[key] = value
    return out


def loads_strict(text: str, policy: Policy | None = None) -> object:
    active = policy or Policy()
    try:
        raw_len = len(text.encode("utf-8", "strict"))
    except UnicodeEncodeError as exc:
        raise StrictJSONError("JSON text contains invalid Unicode scalar data") from exc
    if raw_len > active.max_json_text_bytes:
        raise StrictJSONError("JSON text exceeds max_json_text_bytes")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_int=_parse_i128,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except StrictJSONError:
        raise
    except (json.JSONDecodeError, RecursionError, ValueError) as exc:
        raise StrictJSONError(f"invalid JSON: {exc}") from exc
    try:
        encode(value, active)
    except ValidationError as exc:
        raise StrictJSONError(str(exc)) from exc
    return value


@dataclass(frozen=True, slots=True)
class WireMutation:
    mutation_id: str
    data: bytes
    should_decode: bool
    rationale: str


def malformed_mutations(valid_wire: bytes) -> tuple[WireMutation, ...]:
    """Deterministic negative-path mutations; no RNG or hidden state."""
    if not valid_wire.startswith(MAGIC) or len(valid_wire) < 5:
        raise ValueError("valid_wire must be a complete NCW1 value")
    cases = [
        WireMutation("baseline", valid_wire, True, "control"),
        WireMutation("bad-magic", b"BAD!" + valid_wire[4:], False, "version mismatch"),
        WireMutation("unknown-root-tag", valid_wire[:4] + b"\xff" + valid_wire[5:], False, "unknown tag"),
        WireMutation("trailing-zero", valid_wire + b"\x00", False, "trailing data"),
        WireMutation("trailing-junk", valid_wire + b"JUNK", False, "trailing data"),
    ]
    for cut in sorted({0, 1, 2, 3, 4, 5, len(valid_wire)//2, len(valid_wire)-1}):
        if 0 <= cut < len(valid_wire):
            cases.append(WireMutation(f"truncate-{cut}", valid_wire[:cut], False, "truncated frame"))
    return tuple(cases)


@dataclass(slots=True)
class _Reader:
    data: bytes
    policy: Policy
    pos: int

    def take(self, count: int, context: str) -> bytes:
        if count < 0 or self.pos + count > len(self.data):
            raise DecodeError(f"truncated {context}")
        out = self.data[self.pos:self.pos + count]
        self.pos += count
        return out

    def u8(self, context: str) -> int:
        return self.take(1, context)[0]

    def u32(self, context: str) -> int:
        return int.from_bytes(self.take(4, context), "big")


def _dec_text(raw: bytes, policy: Policy, context: str) -> str:
    if len(raw) > policy.max_string_bytes:
        raise DecodeError(f"{context} exceeds max_string_bytes")
    try:
        value = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise DecodeError(f"{context} is not valid UTF-8") from exc
    if unicodedata.normalize("NFC", value) != value:
        raise DecodeError(f"{context} is not NFC-normalized")
    try:
        value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise DecodeError(f"{context} contains invalid scalar text") from exc
    return value


def _dec(reader: _Reader, depth: int) -> object:
    if depth > reader.policy.max_depth:
        raise DecodeError("max_depth exceeded")
    tag = reader.u8("value tag")
    if tag == T_NULL:
        return None
    if tag == T_FALSE:
        return False
    if tag == T_TRUE:
        return True
    if tag == T_I128:
        return int.from_bytes(reader.take(16, "i128"), "big", signed=True)
    if tag == T_STR:
        n = reader.u32("string length")
        return _dec_text(reader.take(n, "string bytes"), reader.policy, "string")
    if tag == T_LIST:
        count = reader.u32("list count")
        if count > reader.policy.max_container_items:
            raise DecodeError("list exceeds max_container_items")
        return [_dec(reader, depth + 1) for _ in range(count)]
    if tag == T_MAP:
        count = reader.u32("map count")
        if count > reader.policy.max_container_items:
            raise DecodeError("map exceeds max_container_items")
        out: dict[str, object] = {}
        previous: bytes | None = None
        for _ in range(count):
            n = reader.u32("map key length")
            raw_key = reader.take(n, "map key bytes")
            key = _dec_text(raw_key, reader.policy, "map key")
            if previous is not None and raw_key <= previous:
                raise DecodeError("map keys duplicate or not in canonical byte order")
            previous = raw_key
            out[key] = _dec(reader, depth + 1)
        return out
    raise DecodeError(f"unknown tag: 0x{tag:02x}")


def decode(data: bytes, policy: Policy | None = None) -> object:
    active = policy or Policy()
    if not isinstance(data, bytes):
        raise DecodeError("wire input must be immutable bytes")
    if len(data) > active.max_total_wire_bytes:
        raise DecodeError("wire input exceeds max_total_wire_bytes")
    if not data.startswith(MAGIC):
        raise DecodeError("invalid wire magic/version")
    reader = _Reader(data, active, len(MAGIC))
    value = _dec(reader, 0)
    if reader.pos != len(data):
        raise DecodeError("trailing bytes are forbidden")
    return value
