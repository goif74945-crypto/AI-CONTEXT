from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable

from .canonical import fingerprint


class DeltaKind(str, Enum):
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    CHANGED = "CHANGED"
    UNKNOWN = "UNKNOWN"


UNKNOWN_MARKERS = {"UNKNOWN", "NOT_VERIFIED", "CONFLICT"}


@dataclass(frozen=True)
class DeltaEntry:
    path: str
    kind: DeltaKind
    before: Any
    after: Any

    def as_dict(self) -> dict[str, Any]:
        return {"after": self.after, "before": self.before, "kind": self.kind.value, "path": self.path}


@dataclass(frozen=True)
class DeltaResult:
    before_hash: str
    after_hash: str
    entries: tuple[DeltaEntry, ...]
    fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "after_hash": self.after_hash,
            "before_hash": self.before_hash,
            "entries": [e.as_dict() for e in self.entries],
            "fingerprint": self.fingerprint,
        }


def _ptr(path: tuple[str, ...]) -> str:
    if not path:
        return ""
    def esc(token: str) -> str:
        return token.replace("~", "~0").replace("/", "~1")
    return "/" + "/".join(esc(x) for x in path)


def _is_unknown(value: Any) -> bool:
    return isinstance(value, dict) and set(value) == {"$nexy_state"} and value["$nexy_state"] in UNKNOWN_MARKERS


def _redact(path: str, value: Any, redactions: set[str]) -> Any:
    if "" in redactions or any(path == root or path.startswith(root + "/") for root in redactions if root):
        return "[REDACTED]"
    return value


def compile_outcome_delta(before: Any, after: Any, *, redact_paths: Iterable[str] = ()) -> DeltaResult:
    redactions = set(redact_paths)
    if any(not isinstance(p, str) or (p and not p.startswith("/")) for p in redactions):
        raise ValueError("redact paths must be JSON pointers or empty root")
    entries: list[DeltaEntry] = []

    def walk(left: Any, right: Any, path: tuple[str, ...]) -> None:
        pointer = _ptr(path)
        if _is_unknown(left) or _is_unknown(right):
            if left != right:
                entries.append(DeltaEntry(pointer, DeltaKind.UNKNOWN, _redact(pointer, left, redactions), _redact(pointer, right, redactions)))
            return
        if isinstance(left, dict) and isinstance(right, dict):
            for key in sorted(set(left) | set(right)):
                child = path + (str(key),)
                child_ptr = _ptr(child)
                if key not in left:
                    entries.append(DeltaEntry(child_ptr, DeltaKind.ADDED, None, _redact(child_ptr, right[key], redactions)))
                elif key not in right:
                    entries.append(DeltaEntry(child_ptr, DeltaKind.REMOVED, _redact(child_ptr, left[key], redactions), None))
                else:
                    walk(left[key], right[key], child)
            return
        if isinstance(left, list) and isinstance(right, list):
            max_len = max(len(left), len(right))
            for idx in range(max_len):
                child = path + (str(idx),)
                child_ptr = _ptr(child)
                if idx >= len(left):
                    entries.append(DeltaEntry(child_ptr, DeltaKind.ADDED, None, _redact(child_ptr, right[idx], redactions)))
                elif idx >= len(right):
                    entries.append(DeltaEntry(child_ptr, DeltaKind.REMOVED, _redact(child_ptr, left[idx], redactions), None))
                else:
                    walk(left[idx], right[idx], child)
            return
        if left != right:
            entries.append(DeltaEntry(pointer, DeltaKind.CHANGED, _redact(pointer, left, redactions), _redact(pointer, right, redactions)))

    walk(before, after, ())
    before_hash = fingerprint(before)
    after_hash = fingerprint(after)
    data = {
        "after_hash": after_hash,
        "before_hash": before_hash,
        "entries": [e.as_dict() for e in entries],
    }
    return DeltaResult(before_hash, after_hash, tuple(entries), fingerprint(data))
