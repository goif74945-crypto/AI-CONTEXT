from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "conformance" / "truth_surface_checker.py"
SPEC = importlib.util.spec_from_file_location("truth_surface_checker", MODULE)
assert SPEC and SPEC.loader
m = importlib.util.module_from_spec(SPEC)
sys.modules["truth_surface_checker"] = m
SPEC.loader.exec_module(m)


def main() -> int:
    corpus = ROOT / "corpus" / "truth_surface_scenarios.jsonl"
    total = matched = 0
    failures = []
    for line_no, line in enumerate(corpus.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        total += 1
        row = json.loads(line)
        report = m.audit_surface(row["backend"], row["surface"], row["role"])
        got_codes = {v.code for v in report.violations}
        ok = report.conformant is row["expected_conformant"]
        expected = row.get("expected_violation")
        if expected is not None:
            ok = ok and expected in got_codes
        if ok:
            matched += 1
        else:
            failures.append({"line": line_no, "id": row.get("id"), "expected": expected, "got": sorted(got_codes), "conformant": report.conformant})
    print(json.dumps({"total": total, "matched": matched, "failures": len(failures)}, sort_keys=True))
    if failures:
        for f in failures[:20]:
            print(json.dumps(f, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
