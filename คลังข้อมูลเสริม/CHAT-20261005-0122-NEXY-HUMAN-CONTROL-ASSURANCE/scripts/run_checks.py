from __future__ import annotations

import json
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    return result


def main() -> int:
    for path in sorted(SRC.rglob("*.py")):
        py_compile.compile(str(path), doraise=True)
    print("E1 compile: PASS")

    unit = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    if unit.returncode != 0:
        return unit.returncode

    sys.path.insert(0, str(SRC))
    from hcas.validator import validate_manifest

    safe = json.loads((ROOT / "examples" / "safe_manifest.json").read_text(encoding="utf-8"))
    unsafe = json.loads((ROOT / "examples" / "unsafe_manifest.json").read_text(encoding="utf-8"))
    safe_report = validate_manifest(safe)
    unsafe_report = validate_manifest(unsafe)
    if not safe_report.passed or unsafe_report.passed:
        print("fixture expectation failed", file=sys.stderr)
        return 3
    print(f"E2 fixture validation: PASS (unsafe errors={len(unsafe_report.errors)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
