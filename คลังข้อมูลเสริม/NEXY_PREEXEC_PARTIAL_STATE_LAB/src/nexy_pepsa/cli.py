from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .canonical import CanonicalizationError, canonical_json
from .engine import PlanStructureError, analyze
from .models import Verdict
from .parser import InputValidationError, load_plan, load_policy


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexy-pepsa",
        description="Deterministic pre-execution partial-state analyzer. It never executes the plan.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze_parser = subparsers.add_parser("analyze", help="analyze a plan against an authority policy")
    analyze_parser.add_argument("--plan", required=True, type=Path)
    analyze_parser.add_argument("--policy", required=True, type=Path)
    analyze_parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "analyze":
        return 3

    try:
        plan = load_plan(args.plan)
        policy = load_policy(args.policy)
        report = analyze(plan, policy)
    except (InputValidationError, PlanStructureError, CanonicalizationError) as exc:
        payload = {"status": "INVALID_INPUT", "error": str(exc)}
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), file=sys.stderr)
        return 3

    if args.pretty:
        print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(canonical_json(report.to_dict()))
    return 0 if report.verdict is Verdict.READY else 2


if __name__ == "__main__":
    raise SystemExit(main())
