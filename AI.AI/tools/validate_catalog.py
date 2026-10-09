#!/usr/bin/env python3
"""Offline static collision and patch-integrity gate; not an E2E test runner."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath

REQUIRED = {"id", "title", "critique_signature", "fingerprint", "target_revision",
            "target_zip_sha256", "patch_sha256", "status", "observed_tests"}
STATES = {"PROPOSED", "IMPLEMENTED_UNTESTED", "TESTED_ON_PINNED_REVISION",
          "MERGE_READY", "MERGED", "BLOCKED", "REJECTED_DUPLICATE", "REJECTED_INVALID"}

def normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())

def safe_path(value: str) -> bool:
    if not value or value.startswith(("/", "\\")) or "\\" in value or "\x00" in value or ":" in value:
        return False
    pieces = value.split("/")
    return (all(x not in ("", ".", "..", "โค้ดโปรเจคปัจจุบัน", "NEXY.AI-") for x in pieces)
            and not value.startswith(".git/") and not PurePosixPath(value).is_absolute())

def validate(root: Path) -> list[str]:
    errors = []
    registry = root / "REGISTRY.md"
    if not registry.is_file():
        return ["missing registry"]
    index = registry.read_text(encoding="utf-8")
    seen = {name: set() for name in ("id", "title", "critique_signature", "fingerprint")}
    proposals = root / "PROPOSALS"
    if not proposals.is_dir():
        return ["missing proposal directory"]
    folders = sorted(x for x in proposals.iterdir() if x.is_dir())
    if not folders:
        return ["no proposals"]
    for folder in folders:
        label = folder.name
        try:
            obj = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError):
            errors.append(label + ": unreadable manifest")
            continue
        if not isinstance(obj, dict) or REQUIRED - obj.keys():
            errors.append(label + ": missing manifest fields")
            continue
        if any(not isinstance(obj[k], str) or not obj[k].strip() for k in REQUIRED - {"observed_tests"}):
            errors.append(label + ": invalid text field")
            continue
        if not isinstance(obj["observed_tests"], dict):
            errors.append(label + ": invalid test metadata")
        ident = obj["id"]
        if not re.fullmatch(r"AAI-\d{8}-\d{3}", ident) or not label.startswith(ident + "-"):
            errors.append(label + ": ID/folder mismatch")
        if ident not in index:
            errors.append(label + ": unregistered ID")
        if obj["status"] not in STATES:
            errors.append(label + ": invalid state")
        for key, uniques in seen.items():
            val = normalized(obj[key])
            if val in uniques:
                errors.append(label + ": duplicate " + key)
            uniques.add(val)
        for field in ("target_zip_sha256", "patch_sha256"):
            if not re.fullmatch(r"[a-f0-9]{64}", obj[field]):
                errors.append(label + ": bad " + field)
        if not (folder / "README.md").is_file() or not (folder / "TEST_EVIDENCE.md").is_file():
            errors.append(label + ": missing design or evidence")
        try:
            buf = (folder / "integration.patch").read_bytes()
            code = buf.decode("utf-8")
        except (OSError, UnicodeError):
            errors.append(label + ": unreadable patch")
            continue
        if hashlib.sha256(buf).hexdigest() != obj["patch_sha256"]:
            errors.append(label + ": patch SHA mismatch")
        changed = set()
        has_hunk = False
        for line in code.splitlines():
            if line.startswith("diff --git "):
                match = re.fullmatch(r"diff --git a/(\S+) b/(\S+)", line)
                if not match or match[1] != match[2] or not safe_path(match[1]):
                    errors.append(label + ": unsafe diff")
                else:
                    changed.add(match[1])
            elif line.startswith(("--- ", "+++ ")):
                p = line[4:]
                if p != "/dev/null" and not (p.startswith(("a/", "b/")) and safe_path(p[2:])):
                    errors.append(label + ": unsafe patch header")
            elif line.startswith("@@ "):
                has_hunk = True
            elif line.startswith(("GIT binary patch", "Binary files ", "rename from ", "rename to ", "new file mode 120000")):
                errors.append(label + ": forbidden patch operation")
        if not changed or not has_hunk or not any(x.startswith("tests/") for x in changed):
            errors.append(label + ": missing source change, hunk, or automated test")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    problems = validate(args.root)
    if problems:
        for item in problems:
            print("FAIL:", item, file=sys.stderr)
        return 1
    print("PASS: registry, unique normalized fields, safe patch paths and SHA-256")
    print("LIMIT: semantic uniqueness and runtime proof must be independently checked")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
