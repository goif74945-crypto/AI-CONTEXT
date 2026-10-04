from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ARTIFACT_MANIFEST.json"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def json_semantic_sha256(path: Path) -> str:
    value = json.loads(path.read_text(encoding="utf-8"))
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures: list[str] = []

    for rel, expected in manifest["byte_exact_git_blobs"].items():
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"MISSING byte-exact file: {rel}")
            continue
        observed = git_blob_sha(path)
        if observed != expected:
            failures.append(f"BYTE DRIFT {rel}: expected {expected}, observed {observed}")

    for rel, expected in manifest["json_semantic_sha256"].items():
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"MISSING JSON file: {rel}")
            continue
        observed = json_semantic_sha256(path)
        if observed != expected:
            failures.append(f"JSON DRIFT {rel}: expected {expected}, observed {observed}")

    if failures:
        print("MANIFEST_VERIFY=FAIL")
        for failure in failures:
            print(failure)
        return 2

    print(
        "MANIFEST_VERIFY=PASS "
        f"byte_exact={len(manifest['byte_exact_git_blobs'])} "
        f"json_semantic={len(manifest['json_semantic_sha256'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
