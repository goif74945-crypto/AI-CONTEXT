from __future__ import annotations

import itertools
import json
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    compile_ok = True
    for path in [ROOT / "nexy_preflight.py", ROOT / "cli.py"]:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError:
            compile_ok = False

    unit = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])

    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    from nexy_preflight import TaskContract, evaluate_contract, sha256_identity

    observed = {name: evaluate_contract(TaskContract.from_mapping(raw)).decision.value for name, raw in fixtures.items()}
    expected = {
        "task-safe": "PASS",
        "task-protected-write": "CONFLICT",
        "task-evidence-gap": "NOT_VERIFIED",
    }

    representative = {"target": "repo", "scope": ["a"], "claims": ["c"], "approval": False}
    hashes = {
        sha256_identity({key: representative[key] for key in order})
        for order in itertools.permutations(representative)
    }

    checks = {
        "compile": compile_ok,
        "unit_tests": unit.returncode == 0,
        "acceptance_vectors": observed == expected,
        "canonical_permutation_stability": len(hashes) == 1,
    }
    summary = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "python": sys.version.split()[0],
        "checks": checks,
        "observed_vectors": observed,
        "unique_hashes_for_24_permutations": len(hashes),
        "limitations": [
            "Reference implementation only; NEXY.AI integration not executed.",
            "No tool-broker interception or deployment proof.",
            "Logical path normalization is not an OS/filesystem sandbox."
        ]
    }
    (ROOT / "evidence" / "verification-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    if unit.returncode != 0:
        print(unit.stdout)
        print(unit.stderr, file=sys.stderr)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
