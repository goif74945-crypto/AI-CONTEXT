from __future__ import annotations

import hashlib
import json
from typing import Any


class ContractError(ValueError):
    """Raised when a declarative input contract is invalid."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def pointer_tokens(pointer: str) -> list[str]:
    if pointer == "":
        return []
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ContractError(f"invalid JSON pointer: {pointer!r}")
    return [token.replace("~1", "/").replace("~0", "~") for token in pointer[1:].split("/")]


def resolve_pointer(document: Any, pointer: str, *, missing: Any = None) -> Any:
    current = document
    for token in pointer_tokens(pointer):
        if isinstance(current, dict):
            if token not in current:
                return missing
            current = current[token]
        elif isinstance(current, list):
            try:
                index = int(token)
            except (TypeError, ValueError) as exc:
                raise ContractError(f"list pointer token must be integer: {token!r}") from exc
            if index < 0 or index >= len(current):
                return missing
            current = current[index]
        else:
            return missing
    return current


def count_nodes(value: Any, *, limit: int | None = None) -> int:
    count = 0
    stack = [value]
    while stack:
        item = stack.pop()
        count += 1
        if limit is not None and count > limit:
            return count
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return count
