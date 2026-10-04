from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analyzer import analyze_contract
from .model import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="interaction-contract",
        description="Deterministically analyze a structured user↔AI interaction contract.",
    )
    parser.add_argument("input", type=Path, help="Path to contract JSON")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print report JSON")
    parser.add_argument(
        "--fail-on-block",
        action="store_true",
        help="Exit with code 2 when completion_gate is BLOCK",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        report = analyze_contract(raw)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(json.dumps(report, ensure_ascii=False, separators=(",", ":"), sort_keys=True))

    if args.fail_on_block and report["completion_gate"] == "BLOCK":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
