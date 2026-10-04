from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .engine import verify_plan
from .model import canonical_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic bounded interleaving verifier")
    parser.add_argument("input", type=Path, help="JSON plan file")
    parser.add_argument("--output", type=Path, help="write report JSON to this path")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report = {
            "report_version": "1.0",
            "verification_status": "NOT_VERIFIED",
            "decision": "FREEZE_IO_OR_JSON",
            "diagnostics": [{"code": "INPUT_READ_ERROR", "message": str(exc)}],
        }
        payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2 if args.pretty else None)
        if args.output:
            try:
                args.output.write_text(payload + "\n", encoding="utf-8")
            except OSError:
                pass
        else:
            print(payload)
        return 3

    report = verify_plan(raw)
    payload = (
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)
        if args.pretty
        else canonical_json(report)
    )
    if args.output:
        try:
            args.output.write_text(payload + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"output write failed: {exc}", file=sys.stderr)
            return 3
    else:
        print(payload)

    if report["verification_status"] == "PASS":
        return 0
    if report["verification_status"] == "FAIL":
        return 2
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
