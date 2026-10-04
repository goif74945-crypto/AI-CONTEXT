from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(SRC)
    return subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)


def main() -> int:
    results = {}
    compile_result = run([sys.executable, "-m", "compileall", "-q", "src", "tests", "scripts"])
    results["compileall"] = {
        "returncode": compile_result.returncode,
        "stdout": compile_result.stdout,
        "stderr": compile_result.stderr,
    }

    test_result = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    results["unit_tests"] = {
        "returncode": test_result.returncode,
        "stdout": test_result.stdout,
        "stderr": test_result.stderr,
    }

    scenario_result = run([sys.executable, "-m", "nexy_def.cli", "fixtures/scenarios.json"])
    results["scenario"] = {
        "returncode": scenario_result.returncode,
        "stdout": scenario_result.stdout,
        "stderr": scenario_result.stderr,
    }

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(x["returncode"] == 0 for x in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
