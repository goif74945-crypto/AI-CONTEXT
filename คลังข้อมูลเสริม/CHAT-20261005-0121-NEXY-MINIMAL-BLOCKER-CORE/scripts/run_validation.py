#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "blocker_core.py"
FIXTURE = ROOT / "fixtures" / "release_gate_example.json"
OUT = ROOT / "fixtures" / "release_gate_actual.json"


def run(command):
    print("$", " ".join(str(x) for x in command))
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])

    completed = subprocess.run(
        [sys.executable, str(SRC), "--input", str(FIXTURE), "--output", str(OUT), "--pretty"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    # A valid freeze result intentionally uses CLI exit 2; invalid input is 64.
    if completed.returncode not in {0, 2}:
        raise SystemExit(completed.returncode)

    result = json.loads(OUT.read_text(encoding="utf-8"))
    assert result["decision"] == "FREEZE"
    assert result["status"] in {"FAIL", "BLOCKED", "NOT_VERIFIED", "CONFLICT", "UNKNOWN"}
    assert result["recommended_repair_set"] is not None
    assert len(result["certificate_sha256"]) == 64
    print(
        json.dumps(
            {
                "fixture_status": result["status"],
                "decision": result["decision"],
                "recommended_repair_set": result["recommended_repair_set"]["evidence_ids"],
                "certificate_sha256": result["certificate_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
