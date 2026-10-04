from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SUITES = [
    "01_requirement_unsat_core",
    "02_absence_evidence_planner",
    "03_semantic_namespace_collision_guard",
    "04_trace_invariant_candidate_miner",
    "05_requirement_delta_revalidation_compiler",
]


def main() -> int:
    failures = []
    for suite in SUITES:
        path = ROOT / suite
        tests = sorted(path.glob("test_*.py"))
        if not tests:
            failures.append(f"{suite}: no test files")
            continue
        for test_file in tests:
            print(f"== {suite}/{test_file.name} ==", flush=True)
            proc = subprocess.run(
                [sys.executable, test_file.name, "-v"],
                cwd=path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            print(proc.stdout, end="")
            if proc.returncode != 0:
                failures.append(f"{suite}/{test_file.name}: exit={proc.returncode}")
    if failures:
        print("FINAL: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
