from __future__ import annotations

import argparse
import json
import sys

from .gate import evaluate_datasets
from .io import load_jsonl


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Compare stable and candidate NEXY-style decision records in shadow mode.")
    p.add_argument("stable", help="stable JSONL decision records")
    p.add_argument("candidate", help="candidate JSONL decision records")
    p.add_argument("--pretty", action="store_true", help="pretty-print JSON report")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = evaluate_datasets(load_jsonl(args.stable), load_jsonl(args.candidate))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    indent = 2 if args.pretty else None
    print(json.dumps(report.as_dict(), ensure_ascii=False, sort_keys=True, indent=indent))
    if report.status == "PASS":
        return 0
    if report.status == "NOT_VERIFIED":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
