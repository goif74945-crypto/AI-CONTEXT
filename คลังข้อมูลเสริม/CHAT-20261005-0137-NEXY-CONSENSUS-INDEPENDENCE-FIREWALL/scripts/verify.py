from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


def run(name: str, command: list[str], expected_codes: tuple[int, ...] = (0,)) -> dict:
    proc = subprocess.run(command, cwd=ROOT, env=ENV, text=True, capture_output=True, check=False)
    return {
        "name": name,
        "command": command,
        "returncode": proc.returncode,
        "expected_codes": list(expected_codes),
        "status": "PASS" if proc.returncode in expected_codes else "FAIL",
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    }


def main() -> int:
    checks = [
        run("compileall", [sys.executable, "-m", "compileall", "-q", "src", "tests", "scripts"]),
        run("unit-and-adversarial", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        run("bounded-audit", [sys.executable, "scripts/bounded_audit.py"]),
        run("stress-audit", [sys.executable, "scripts/stress_audit.py"]),
        run(
            "cli-independent",
            [sys.executable, "-m", "ncif.cli", "fixtures/independent_consensus.json", "--min-support-groups", "2"],
        ),
        run(
            "cli-correlated-freeze",
            [sys.executable, "-m", "ncif.cli", "fixtures/correlated_false_consensus.json", "--min-support-groups", "2"],
            (2,),
        ),
    ]
    schema_files = sorted((ROOT / "schema").glob("*.json"))
    fixture_files = sorted((ROOT / "fixtures").glob("*.json"))
    parse_failures = []
    for path in schema_files + fixture_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - verification harness record
            parse_failures.append({"path": str(path.relative_to(ROOT)), "error": repr(exc)})
    checks.append(
        {
            "name": "json-parse",
            "command": ["stdlib-json-load", "schema/*.json", "fixtures/*.json"],
            "returncode": 0 if not parse_failures else 1,
            "expected_codes": [0],
            "status": "PASS" if not parse_failures else "FAIL",
            "stdout_tail": json.dumps({"parsed": len(schema_files) + len(fixture_files), "failures": parse_failures}),
            "stderr_tail": "",
        }
    )
    overall = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    report = {
        "artifact": "NCIF local verification receipt",
        "environment": {"python": sys.version, "platform": sys.platform},
        "overall_status": overall,
        "checks": checks,
        "claim_boundary": "E1/E2/local-tooling evidence for this standalone reference artifact only; not NEXY.AI integration/runtime/deployment proof.",
    }
    path = ROOT / "evidence" / "verification.json"
    path.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall_status": overall, "check_count": len(checks)}, sort_keys=True))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
