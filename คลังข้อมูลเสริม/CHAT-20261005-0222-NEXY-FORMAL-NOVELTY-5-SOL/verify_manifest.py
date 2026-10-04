from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "MANIFEST.sha256"


def main() -> int:
    failures: list[str] = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"missing: {rel}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            failures.append(f"hash mismatch: {rel}")
    if failures:
        print("MANIFEST: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MANIFEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
