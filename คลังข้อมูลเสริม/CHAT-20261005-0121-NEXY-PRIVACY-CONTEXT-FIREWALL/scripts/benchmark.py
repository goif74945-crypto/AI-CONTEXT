"""Small deterministic-shape benchmark for the PCF reference implementation.

This is diagnostic evidence only, not a production SLO benchmark.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from nexy_pcf.compiler import compile_context  # noqa: E402

TEST_KEY = b"benchmark-verification-key-32bytes!!"


def load(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def make_envelope(count: int) -> dict:
    fields = []
    required = []
    for index in range(count):
        field_id = f"f{index:06d}"
        required.append(field_id)
        fields.append(
            {
                "id": field_id,
                "value": "x" * 24,
                "classification": "INTERNAL",
                "purposes": ["code_review"],
                "allowed_destinations": ["provider-alpha"],
                "retention_seconds": 120,
            }
        )
    return {
        "policy_version": "pcf-0.1",
        "purpose": "code_review",
        "destination": "provider-alpha",
        "decision_time": "2026-10-05T01:30:00+07:00",
        "required_fields": required,
        "fields": fields,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", type=int, nargs="+", default=[100, 1000, 10000])
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()
    if args.runs < 1 or any(n < 1 for n in args.fields):
        raise SystemExit("fields and runs must be positive")

    policy = load("policy.json")
    destination = load("provider-alpha.json")
    rows = []
    for count in args.fields:
        envelope = make_envelope(count)
        samples = []
        decision = None
        for _ in range(args.runs):
            started = time.perf_counter()
            result = compile_context(envelope, destination, policy, receipt_key=TEST_KEY)
            samples.append((time.perf_counter() - started) * 1000)
            decision = result.get("decision")
        rows.append(
            {
                "fields": count,
                "runs": args.runs,
                "decision": decision,
                "median_ms": round(statistics.median(samples), 3),
                "min_ms": round(min(samples), 3),
                "max_ms": round(max(samples), 3),
            }
        )
    print(json.dumps({"benchmark": rows}, sort_keys=True))
    return 0 if all(row["decision"] == "ALLOW" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
