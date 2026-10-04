from __future__ import annotations

from typing import Any

from .errors import ContractError


def resolve_path(document: Any, path: str) -> tuple[bool, Any]:
    """Resolve a deliberately small, deterministic path grammar.

    Grammar: dot-separated object keys and decimal list indexes, e.g.
    ``data.answer`` or ``evidence.0.hash``. Arbitrary expressions are forbidden.
    """
    if path == "":
        return True, document
    if path.startswith(".") or path.endswith(".") or ".." in path:
        raise ContractError(f"invalid path: {path!r}")
    current = document
    for segment in path.split("."):
        if not segment:
            raise ContractError(f"invalid path segment in {path!r}")
        if isinstance(current, dict):
            if segment not in current:
                return False, None
            current = current[segment]
            continue
        if isinstance(current, list):
            if not segment.isdecimal():
                raise ContractError(f"list segment must be a decimal index: {segment!r}")
            index = int(segment)
            if index >= len(current):
                return False, None
            current = current[index]
            continue
        return False, None
    return True, current
