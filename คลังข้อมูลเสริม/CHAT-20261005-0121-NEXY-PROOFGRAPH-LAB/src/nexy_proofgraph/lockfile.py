from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

LOCK_VERSION = 1


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_lock(root: Path, paths: Iterable[str]) -> dict[str, Any]:
    root = root.resolve()
    files: list[dict[str, Any]] = []
    normalized: set[str] = set()
    for raw in paths:
        candidate = str(raw).replace("\\", "/")
        pure = PurePosixPath(candidate)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError(f"path escapes root: {raw}")
        rel = pure.as_posix()
        if rel.startswith("./"):
            rel = rel[2:]
        if not rel or rel == ".":
            raise ValueError(f"invalid file path: {raw}")
        normalized.add(rel)

    for rel in sorted(normalized):
        full = (root / rel).resolve()
        try:
            full.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"path escapes root: {rel}") from exc
        if not full.is_file():
            raise FileNotFoundError(rel)
        files.append({"path": rel, "sha256": _sha256(full), "size": full.stat().st_size})
    return {"schema": "nexy-proofgraph/truth-lock", "version": LOCK_VERSION, "files": files}


def verify_lock(root: Path, lock: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    if lock.get("schema") != "nexy-proofgraph/truth-lock" or lock.get("version") != LOCK_VERSION:
        return {"ok": False, "invalid_lock": True, "changed": [], "missing": []}
    changed: list[dict[str, str]] = []
    missing: list[str] = []
    for item in lock.get("files", []):
        rel = str(item["path"])
        full = (root / rel).resolve()
        try:
            full.relative_to(root)
        except ValueError:
            changed.append({"path": rel, "reason": "path_escape"})
            continue
        if not full.is_file():
            missing.append(rel)
            continue
        observed = _sha256(full)
        if observed != item.get("sha256"):
            changed.append({"path": rel, "expected": str(item.get("sha256")), "observed": observed})
    return {"ok": not changed and not missing, "invalid_lock": False, "changed": changed, "missing": missing}


def dump_lock(lock: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(lock, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def load_lock(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
