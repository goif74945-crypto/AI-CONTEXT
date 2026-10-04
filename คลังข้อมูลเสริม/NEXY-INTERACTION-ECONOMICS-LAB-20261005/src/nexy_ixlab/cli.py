from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .compare import compare_plans
from .model import InteractionPlan, ValidationError
from .optimizer import optimize_plan
from .planner import DecisionContext, decide_action
from .scorer import assess_plan


def _load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexy-ixlab")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze an interaction plan")
    analyze.add_argument("path")
    optimize = sub.add_parser("optimize", help="Apply safe-only optimization")
    optimize.add_argument("path")
    decision = sub.add_parser("decision", help="Route an explicit decision context")
    decision.add_argument("path")
    compare = sub.add_parser("compare", help="Compare baseline and candidate interaction plans")
    compare.add_argument("baseline")
    compare.add_argument("candidate")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "compare":
            baseline = InteractionPlan.from_mapping(_load_json(args.baseline))
            candidate = InteractionPlan.from_mapping(_load_json(args.candidate))
            result = compare_plans(baseline, candidate).to_mapping()
        else:
            raw = _load_json(args.path)
        if args.command == "analyze":
            result = assess_plan(InteractionPlan.from_mapping(raw)).to_mapping()
        elif args.command == "optimize":
            opt = optimize_plan(InteractionPlan.from_mapping(raw))
            result = {
                "removed_step_ids": list(opt.removed_step_ids),
                "suggestions": list(opt.suggestions),
                "original": opt.original.to_mapping(),
                "optimized": opt.optimized.to_mapping(),
                "optimized_plan": opt.optimized_plan.to_mapping(),
            }
        elif args.command == "decision":
            result = decide_action(DecisionContext.from_mapping(raw)).to_mapping()
    except (OSError, json.JSONDecodeError, ValidationError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps({"status": "OK", "result": result}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
