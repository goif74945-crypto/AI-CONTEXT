"""Collision-safe path identity extension for experimental RECERT.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from frontier_assurance_lab import (
    FreezeError,
    RecoveryCertifier,
    RecoveryPolicy,
    stable_hash,
)

_MISSING = object()
_ALLOWED_MODES = frozenset({"EXACT", "NONDECREASING", "PRESENT", "ABSENT", "ANY"})


def _encode_token(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def _decode_pointer(pointer: str) -> tuple[str, ...]:
    if pointer == "":
        return ()
    if not pointer.startswith("/"):
        raise FreezeError(f"invalid JSON Pointer: {pointer!r}")
    tokens: list[str] = []
    for raw in pointer[1:].split("/"):
        decoded: list[str] = []
        index = 0
        while index < len(raw):
            character = raw[index]
            if character != "~":
                decoded.append(character)
                index += 1
                continue
            if index + 1 >= len(raw) or raw[index + 1] not in {"0", "1"}:
                raise FreezeError(f"invalid JSON Pointer escape: {pointer!r}")
            decoded.append("~" if raw[index + 1] == "0" else "/")
            index += 2
        tokens.append("".join(decoded))
    canonical = "".join("/" + _encode_token(token) for token in tokens)
    if canonical != pointer:
        raise FreezeError(f"non-canonical JSON Pointer: {pointer!r}")
    return tuple(tokens)


def _under(pointer: str, prefix: str) -> bool:
    return pointer == prefix or pointer.startswith(prefix + "/")


def _validate_leaf(value: Any, pointer: str) -> None:
    try:
        stable_hash(value)
    except (TypeError, ValueError) as error:
        raise FreezeError(f"unsupported recovery value at {pointer!r}") from error


def _flatten_pointer(
    value: Any,
    pointer: str = "",
    active_mappings: set[int] | None = None,
) -> dict[str, Any]:
    if active_mappings is None:
        active_mappings = set()
    if not isinstance(value, Mapping):
        _validate_leaf(value, pointer)
        return {pointer: value}

    identity = id(value)
    if identity in active_mappings:
        raise FreezeError(f"cyclic recovery state at {pointer!r}")
    active_mappings.add(identity)
    try:
        if not value:
            _validate_leaf({}, pointer)
            return {pointer: {}}
        if any(not isinstance(key, str) for key in value):
            raise FreezeError(f"non-string recovery key at {pointer!r}")
        output: dict[str, Any] = {}
        for key in sorted(value):
            child = pointer + "/" + _encode_token(key)
            child_values = _flatten_pointer(value[key], child, active_mappings)
            overlap = set(output).intersection(child_values)
            if overlap:
                raise FreezeError(f"recovery path collision: {sorted(overlap)!r}")
            output.update(child_values)
        return output
    finally:
        active_mappings.remove(identity)


@dataclass(frozen=True)
class PointerRecoveryPolicy:
    modes: Mapping[str, str] = field(default_factory=dict)
    ignore_prefixes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for pointer, mode in self.modes.items():
            if not isinstance(pointer, str) or mode not in _ALLOWED_MODES:
                raise FreezeError("invalid pointer recovery policy")
            _decode_pointer(pointer)
        for prefix in self.ignore_prefixes:
            if not isinstance(prefix, str):
                raise FreezeError("ignore prefix must be a JSON Pointer")
            _decode_pointer(prefix)
            if prefix == "":
                raise FreezeError("root-wide recovery ignore is forbidden")
        for pointer in self.modes:
            if any(_under(pointer, prefix) for prefix in self.ignore_prefixes):
                raise FreezeError(f"policy path {pointer!r} is hidden by ignore prefix")


class PointerRecoveryCertifier:
    @staticmethod
    def _ignored(pointer: str, prefixes: tuple[str, ...]) -> bool:
        return any(_under(pointer, prefix) for prefix in prefixes)

    def certify(
        self,
        before: Mapping[str, Any],
        after: Mapping[str, Any],
        policy: PointerRecoveryPolicy,
    ) -> dict[str, Any]:
        if not isinstance(before, Mapping) or not isinstance(after, Mapping):
            raise FreezeError("recovery states must be mappings")

        pre = _flatten_pointer(before)
        post = _flatten_pointer(after)
        modes = dict(policy.modes)
        pointers = sorted(set(pre) | set(post) | set(modes))
        mismatches: list[dict[str, Any]] = []

        for pointer in pointers:
            if self._ignored(pointer, policy.ignore_prefixes):
                continue
            mode = modes.get(pointer, "EXACT")
            left = pre.get(pointer, _MISSING)
            right = post.get(pointer, _MISSING)

            if mode == "ANY":
                valid = True
            elif mode == "EXACT":
                valid = (
                    left is not _MISSING
                    and right is not _MISSING
                    and stable_hash(left) == stable_hash(right)
                )
            elif mode == "PRESENT":
                valid = right is not _MISSING
            elif mode == "ABSENT":
                valid = right is _MISSING
            else:
                valid = (
                    left is not _MISSING
                    and right is not _MISSING
                    and isinstance(left, int)
                    and not isinstance(left, bool)
                    and isinstance(right, int)
                    and not isinstance(right, bool)
                    and right >= left
                )

            if not valid:
                mismatches.append(
                    {
                        "pointer": pointer,
                        "mode": mode,
                        "before": "<MISSING>" if left is _MISSING else left,
                        "after": "<MISSING>" if right is _MISSING else right,
                    }
                )

        result: dict[str, Any] = {
            "status": "CERTIFIED" if not mismatches else "FREEZE",
            "mismatches": mismatches,
            "compared_pointer_count": sum(
                1
                for pointer in pointers
                if not self._ignored(pointer, policy.ignore_prefixes)
            ),
        }
        result["result_hash"] = stable_hash(result)
        return result


class RecertPathIntegrityAssurance:
    """Conservative integration of original and collision-safe RECERT checks."""

    def __init__(self) -> None:
        self.original = RecoveryCertifier()
        self.pointer_safe = PointerRecoveryCertifier()

    def assess(
        self,
        before: Mapping[str, Any],
        after: Mapping[str, Any],
        original_policy: RecoveryPolicy,
        pointer_policy: PointerRecoveryPolicy,
    ) -> dict[str, Any]:
        original = self.original.certify(before, after, original_policy)
        pointer_safe = self.pointer_safe.certify(before, after, pointer_policy)

        original_pass = original["status"] == "CERTIFIED"
        pointer_pass = pointer_safe["status"] == "CERTIFIED"
        if original_pass and pointer_pass:
            status = "CERTIFIED"
            reason = "BOTH_CERTIFIERS_AGREE"
        elif original_pass and not pointer_pass:
            status = "FREEZE"
            reason = "PATH_ALIAS_OR_STRICTNESS_DISAGREEMENT"
        elif not original_pass and pointer_pass:
            status = "FREEZE"
            reason = "CERTIFIER_DISAGREEMENT"
        else:
            status = "FREEZE"
            reason = "RECOVERY_MISMATCH"

        result: dict[str, Any] = {
            "status": status,
            "reason": reason,
            "original": original,
            "pointer_safe": pointer_safe,
        }
        result["result_hash"] = stable_hash(result)
        return result
