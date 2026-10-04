from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(name: str, command: list[str]) -> dict[str, object]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        "name": name,
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def main() -> int:
    checks = [
        run("compileall", [sys.executable, "-m", "compileall", "-q", "."]),
        run("unittest", [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py", "-v"]),
        run("determinism_fuzz", [sys.executable, "scripts/fuzz_determinism.py"]),
    ]
    status = "PASS" if all(check["returncode"] == 0 for check in checks) else "FAIL"
    print(json.dumps({"status": status, "checks": checks}, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
