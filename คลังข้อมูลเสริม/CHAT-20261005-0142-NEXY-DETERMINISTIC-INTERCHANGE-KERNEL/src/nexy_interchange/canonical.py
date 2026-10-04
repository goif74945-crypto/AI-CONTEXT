from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import unicodedata
from typing import Any

from .errors import (
    CycleError,
    DuplicateKeyError,
    InvalidJsonError,
    InvalidUnicodeError,
    NonStringKeyError,
    NormalizationCollisionError,
    ResourceLimitError,
    UnsafeIntegerError,
    UnsupportedTypeError,
)

JSONValue = None | bool | int | str | list["JSONValue"] | dict[str, "JSONValue"]


@dataclass(frozen=True, slots=True)
class CanonicalLimits:
    max_depth: int = 64
    max_nodes: int = 100_000
    max_output_bytes: int = 8 * 1024 * 1024
    min_integer: int = -(2**53 - 1)
    max_integer: int = 2**53 - 1

    def __post_init__(self) -> None:
        if self.max_depth < 0:
            raise ValueError("max_depth must be >= 0")
        if self.max_depth > 512:
            raise ValueError("max_depth must be <= 512 to preserve bounded recursion")
        if self.max_nodes < 1:
            raise ValueError("max_nodes must be >= 1")
        if self.max_output_bytes < 1:
            raise ValueError("max_output_bytes must be >= 1")
        if self.min_integer > self.max_integer:
            raise ValueError("min_integer must be <= max_integer")


DEFAULT_LIMITS = CanonicalLimits()


def _validate_unicode_scalar_sequence(value: str, *, path: str) -> None:
    for character in value:
        codepoint = ord(character)
        if 0xD800 <= codepoint <= 0xDFFF:
            raise InvalidUnicodeError(
                f"surrogate code point U+{codepoint:04X} is not a Unicode scalar value",
                path=path,
            )


def _normalize_string(value: str, *, path: str) -> str:
    _validate_unicode_scalar_sequence(value, path=path)
    normalized = unicodedata.normalize("NFC", value)
    _validate_unicode_scalar_sequence(normalized, path=path)
    return normalized


def _escape_json_string(value: str) -> str:
    # JSON encoder is used only for the string escape grammar; separators and
    # object ordering are controlled by this module.
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


def _path_key(path: str, key: str) -> str:
    return f"{path}[{json.dumps(key, ensure_ascii=True)}]"


def canonical_text(value: Any, *, limits: CanonicalLimits = DEFAULT_LIMITS) -> str:
    """Return NDIK-v1 canonical JSON text for a strict JSON-compatible value.

    Rules intentionally favor cross-runtime reproducibility over convenience:
    floats are rejected, integers are bounded to the JavaScript-safe range by
    default, strings/keys are NFC-normalized, object keys are ordered by Unicode
    scalar-value order, invalid surrogate code points are rejected, and
    normalization-induced key collisions are rejected.
    """

    chunks: list[str] = []
    active_container_ids: set[int] = set()
    node_count = 0
    output_bytes = 0

    def append(chunk: str) -> None:
        nonlocal output_bytes
        output_bytes += len(chunk.encode("utf-8"))
        if output_bytes > limits.max_output_bytes:
            raise ResourceLimitError(
                f"canonical output exceeds max_output_bytes={limits.max_output_bytes}",
                path="$",
            )
        chunks.append(chunk)

    def walk(node: Any, *, depth: int, path: str) -> None:
        nonlocal node_count
        node_count += 1
        if node_count > limits.max_nodes:
            raise ResourceLimitError(
                f"node count exceeds max_nodes={limits.max_nodes}", path=path
            )
        if depth > limits.max_depth:
            raise ResourceLimitError(
                f"depth exceeds max_depth={limits.max_depth}", path=path
            )

        if node is None:
            append("null")
            return
        if type(node) is bool:
            append("true" if node else "false")
            return
        if type(node) is int:
            if not (limits.min_integer <= node <= limits.max_integer):
                raise UnsafeIntegerError(
                    f"integer {node} outside [{limits.min_integer}, {limits.max_integer}]",
                    path=path,
                )
            append(str(node))
            return
        if type(node) is str:
            append(_escape_json_string(_normalize_string(node, path=path)))
            return
        if type(node) is float:
            raise UnsupportedTypeError(
                "float is forbidden; encode an exact decimal as a tagged string/object",
                path=path,
            )

        if type(node) is list:
            object_id = id(node)
            if object_id in active_container_ids:
                raise CycleError("cyclic list detected", path=path)
            active_container_ids.add(object_id)
            try:
                append("[")
                for index, item in enumerate(node):
                    if index:
                        append(",")
                    walk(item, depth=depth + 1, path=f"{path}[{index}]")
                append("]")
            finally:
                active_container_ids.remove(object_id)
            return

        if type(node) is dict:
            object_id = id(node)
            if object_id in active_container_ids:
                raise CycleError("cyclic object detected", path=path)
            active_container_ids.add(object_id)
            try:
                normalized_items: list[tuple[str, Any]] = []
                seen: dict[str, str] = {}
                for raw_key, item in node.items():
                    if type(raw_key) is not str:
                        raise NonStringKeyError(
                            f"object key type {type(raw_key).__name__} is not str", path=path
                        )
                    normalized_key = _normalize_string(raw_key, path=path)
                    prior = seen.get(normalized_key)
                    if prior is not None and prior != raw_key:
                        raise NormalizationCollisionError(
                            f"keys {prior!r} and {raw_key!r} normalize to {normalized_key!r}",
                            path=path,
                        )
                    seen[normalized_key] = raw_key
                    normalized_items.append((normalized_key, item))

                normalized_items.sort(key=lambda pair: tuple(ord(ch) for ch in pair[0]))
                append("{")
                for index, (key, item) in enumerate(normalized_items):
                    if index:
                        append(",")
                    append(_escape_json_string(key))
                    append(":")
                    walk(item, depth=depth + 1, path=_path_key(path, key))
                append("}")
            finally:
                active_container_ids.remove(object_id)
            return

        raise UnsupportedTypeError(
            f"type {type(node).__name__} is not permitted", path=path
        )

    walk(value, depth=0, path="$")
    return "".join(chunks)


def canonical_bytes(value: Any, *, limits: CanonicalLimits = DEFAULT_LIMITS) -> bytes:
    return canonical_text(value, limits=limits).encode("utf-8")


def fingerprint(
    value: Any,
    *,
    domain: str = "NEXY-NDIK-V1",
    limits: CanonicalLimits = DEFAULT_LIMITS,
) -> str:
    if not domain or "\x00" in domain:
        raise ValueError("domain must be non-empty and must not contain NUL")
    _validate_unicode_scalar_sequence(domain, path="$.domain")
    digest = hashlib.sha256()
    digest.update(domain.encode("utf-8"))
    digest.update(b"\x00")
    digest.update(canonical_bytes(value, limits=limits))
    return f"sha256:{digest.hexdigest()}"


def _reject_float(raw: str) -> None:
    raise UnsupportedTypeError(
        f"JSON float {raw!r} is forbidden; use an exact tagged representation", path="$"
    )


def _reject_constant(raw: str) -> None:
    raise InvalidJsonError(f"non-standard JSON constant {raw!r} is forbidden", path="$")


def _pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise DuplicateKeyError(f"duplicate raw JSON key {key!r}", path="$")
        obj[key] = value
    return obj


def loads_strict(
    text: str, *, limits: CanonicalLimits = DEFAULT_LIMITS
) -> JSONValue:
    """Parse JSON while rejecting duplicate keys, floats, and non-standard constants."""

    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs_hook,
            parse_int=int,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except (DuplicateKeyError, UnsupportedTypeError, InvalidJsonError):
        raise
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise InvalidJsonError(str(exc), path="$" ) from exc
    # Canonicalization performs normalized-key collision, Unicode, numeric, and
    # resource-limit checks on the parsed value.
    canonical_text(value, limits=limits)
    return value


def canonicalize_json_text(
    text: str, *, limits: CanonicalLimits = DEFAULT_LIMITS
) -> str:
    value = loads_strict(text, limits=limits)
    return canonical_text(value, limits=limits)
