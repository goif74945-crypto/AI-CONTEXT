from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

from .model import Document

TEXT_SUFFIXES = {".md", ".markdown", ".json", ".yaml", ".yml", ".txt", ".toml"}
SKIP_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}


def normalize_rel(path: Path) -> str:
    return path.as_posix().lstrip("./")


def iter_text_paths(root: Path, max_bytes: int = 2_000_000) -> Iterable[Path]:
    root = root.resolve()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            if path.stat().st_size > max_bytes:
                continue
        except OSError:
            continue
        yield path


def load_document(root: Path, path: Path) -> Document:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    rel = normalize_rel(path.resolve().relative_to(root.resolve()))
    return Document(
        path=rel,
        sha256=hashlib.sha256(raw).hexdigest(),
        size=len(raw),
        kind=path.suffix.lower().lstrip(".") or "text",
        text=text,
    )


def load_documents(root: Path, max_bytes: int = 2_000_000) -> list[Document]:
    docs: list[Document] = []
    for path in iter_text_paths(root, max_bytes=max_bytes):
        try:
            docs.append(load_document(root, path))
        except (UnicodeDecodeError, OSError):
            continue
    return docs
