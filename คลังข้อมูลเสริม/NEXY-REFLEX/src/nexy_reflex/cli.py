"""Command-line interface for NEXY-REFLEX."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .engine import evaluate_snapshot
from .impact import diff_snapshots
from .models import Snapshot, TruthStatus


EXIT_PASS = 0
EXIT_FREEZE = 2
EXIT_REPLAY_MISMATCH = 3
EXIT_INPUT_ERROR = 4


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return raw


def _write_json(payload: dict[str, Any], output: Path | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if output is None:
        sys.stdout.write(text)
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")


def _cmd_evaluate(args: argparse.Namespace) -> int:
    snapshot = Snapshot.from_dict(_read_json(args.input))
    decision = evaluate_snapshot(snapshot)
    _write_json(decision.to_dict(), args.output)
    return EXIT_PASS if decision.verdict is TruthStatus.PASS else EXIT_FREEZE


def _cmd_replay(args: argparse.Namespace) -> int:
    snapshot = Snapshot.from_dict(_read_json(args.input))
    decision = evaluate_snapshot(snapshot)
    payload = decision.to_dict()
    payload["replay_expected_digest"] = args.expect_digest
    payload["replay_match"] = decision.decision_digest == args.expect_digest
    _write_json(payload, args.output)
    return EXIT_PASS if payload["replay_match"] else EXIT_REPLAY_MISMATCH


def _cmd_diff(args: argparse.Namespace) -> int:
    before = Snapshot.from_dict(_read_json(args.before))
    after = Snapshot.from_dict(_read_json(args.after))
    report = diff_snapshots(before, after)
    _write_json(report.to_dict(), args.output)
    return EXIT_PASS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexy-reflex", description="Deterministic NEXY shadow verification lab")
    sub = parser.add_subparsers(dest="command", required=True)

    evaluate = sub.add_parser("evaluate", help="evaluate one exported snapshot")
    evaluate.add_argument("input", type=Path)
    evaluate.add_argument("--output", type=Path)
    evaluate.set_defaults(func=_cmd_evaluate)

    replay = sub.add_parser("replay", help="recompute and compare a known decision digest")
    replay.add_argument("input", type=Path)
    replay.add_argument("--expect-digest", required=True)
    replay.add_argument("--output", type=Path)
    replay.set_defaults(func=_cmd_replay)

    diff = sub.add_parser("diff", help="compute change impact between two snapshots")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.add_argument("--output", type=Path)
    diff.set_defaults(func=_cmd_diff)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        sys.stderr.write(f"INPUT_ERROR: {exc}\n")
        return EXIT_INPUT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
