#!/usr/bin/env python3
"""Decode verified AI.AI source snapshots into a NEW directory only.

Usage:
    python decode_snapshots.py --snapshot FULL-SOURCE-ARCHIVE.md --destination /tmp/restored-v0.4.0

The archive is a full source tree, not a runnable product installation.
No network access, elevated permissions, or third-party dependencies.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
from io import BytesIO
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
from zipfile import BadZipFile, ZipFile

DIGEST_RE = re.compile(r"^- Decoded ZIP SHA-256: `([a-f0-9]{64})`$", re.MULTILINE)
BASE64_RE = re.compile(r"^```base64\s*\n([A-Za-z0-9+/=\s]+)\n```", re.MULTILINE)
PROTECTED = "โค้ดโปรเจคปัจจุบัน"
MAX_COMPRESSED = 10_000_000
MAX_UNCOMPRESSED = 40_000_000
MAX_ENTRIES = 500


class SnapshotError(ValueError):
    """The snapshot is invalid or unsafe to restore."""


def restore(snapshot: Path, destination: Path) -> tuple[int, str]:
    """Verify bytes and all paths before moving a new tree into place.

    The final destination must not exist; rollback deletes only our own temp dir.
    """
    destination = destination.absolute()
    if PROTECTED in destination.parts or destination.exists() or destination.is_symlink():
        raise SnapshotError("Destination is protected or already exists")
    if destination.parent.is_symlink() or not destination.parent.is_dir():
        raise SnapshotError("Destination parent must be an existing real directory")
    if any(part in ("", ".", "..") for part in destination.parts):
        raise SnapshotError("Invalid destination")

    text = snapshot.read_text(encoding="utf-8")
    hash_match = DIGEST_RE.search(text)
    encoded_match = BASE64_RE.search(text)
    if not hash_match or not encoded_match:
        raise SnapshotError("Missing SHA-256 or Base64 payload")
    encoded = "".join(encoded_match.group(1).split())
    try:
        data = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SnapshotError("Invalid Base64 content") from exc
    if not data or len(data) > MAX_COMPRESSED:
        raise SnapshotError("ZIP exceeds supported size")
    digest = hashlib.sha256(data).hexdigest()
    if digest != hash_match.group(1):
        raise SnapshotError("ZIP SHA-256 mismatch")

    try:
        with ZipFile(BytesIO(data)) as archive:
            files = [info for info in archive.infolist() if not info.is_dir()]
            if not 1 <= len(files) <= MAX_ENTRIES:
                raise SnapshotError("Invalid source-file count")
            if sum(info.file_size for info in files) > MAX_UNCOMPRESSED:
                raise SnapshotError("Uncompressed content exceeds safety limit")
            seen: set[str] = set()
            for info in files:
                raw_name = info.filename
                path = PurePosixPath(raw_name)
                if (len(path.parts) < 2 or path.parts[0] != "AI.AI"
                        or any(part in ("", ".", "..", PROTECTED) for part in path.parts)
                        or "\\" in raw_name or ":" in raw_name or raw_name.startswith("/")):
                    raise SnapshotError("Disallowed entry path")
                if stat.S_ISLNK(info.external_attr >> 16):
                    raise SnapshotError("Symbolic links are forbidden")
                normalized = str(path).casefold()
                if normalized in seen:
                    raise SnapshotError("Case-insensitive duplicate entry")
                seen.add(normalized)
            if archive.testzip() is not None:
                raise SnapshotError("ZIP CRC mismatch")
            temp = Path(tempfile.mkdtemp(prefix=".ai-ai-import-", dir=destination.parent))
            try:
                for info in files:
                    rel = PurePosixPath(info.filename)
                    p = temp.joinpath(*rel.parts)
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(archive.read(info))
                if destination.exists():
                    raise SnapshotError("Destination appeared during import")
                temp.rename(destination)
            finally:
                if temp.exists():
                    shutil.rmtree(temp)
            return len(files), digest
    except BadZipFile as exc:
        raise SnapshotError("Invalid ZIP payload") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()
    files, digest = restore(args.snapshot, args.destination)
    print(f"PASS: restored {files} source files; archive sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())