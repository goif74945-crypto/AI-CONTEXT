from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .canonical import canonical_json
from .diffing import diff_snapshots
from .engine import build_snapshot, validate_snapshot, verify_drift
from .policy import Policy, PolicyError


def _load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_policy(path: str | None) -> Policy:
    return Policy.from_dict(_load_json(path)) if path else Policy()


def _emit(payload: dict[str, Any], output: str | None) -> None:
    data = canonical_json(payload) + "\n"
    if output:
        Path(output).write_text(data, encoding="utf-8")
    else:
        sys.stdout.write(data)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nscs", description="NEXY Supply-Chain Sentinel")
    sub = parser.add_subparsers(dest="command", required=True)

    snap = sub.add_parser("snapshot", help="create a sealed dependency snapshot")
    snap.add_argument("--input", required=True)
    snap.add_argument("--policy")
    snap.add_argument("--output")

    diff = sub.add_parser("diff", help="classify drift between two sealed snapshots")
    diff.add_argument("--baseline", required=True)
    diff.add_argument("--candidate", required=True)
    diff.add_argument("--output")

    verify = sub.add_parser("verify", help="snapshot candidate input and enforce drift policy")
    verify.add_argument("--baseline", required=True)
    verify.add_argument("--input", required=True)
    verify.add_argument("--policy")
    verify.add_argument("--output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "snapshot":
            policy = _load_policy(args.policy)
            payload = build_snapshot(args.input, policy=policy)
            _emit(payload, args.output)
            return 0 if payload["decision"] == "ALLOW" else 2
        if args.command == "diff":
            baseline = _load_json(args.baseline)
            candidate = _load_json(args.candidate)
            baseline_valid, baseline_reasons = validate_snapshot(baseline)
            candidate_valid, candidate_reasons = validate_snapshot(candidate)
            reasons = sorted(
                [f"BASELINE_{r}" for r in baseline_reasons]
                + [f"CANDIDATE_{r}" for r in candidate_reasons]
            )
            payload = {
                "schema_version": "nscs.diff.v1",
                "decision": "FREEZE" if reasons else "ALLOW",
                "events": diff_snapshots(baseline, candidate) if baseline_valid and candidate_valid else [],
                "reason_codes": reasons,
            }
            _emit(payload, args.output)
            return 0 if payload["decision"] == "ALLOW" else 2
        if args.command == "verify":
            policy = _load_policy(args.policy)
            baseline = _load_json(args.baseline)
            candidate = build_snapshot(args.input, policy=policy)
            payload = verify_drift(baseline, candidate, policy=policy)
            _emit(payload, args.output)
            return 0 if payload["decision"] == "ALLOW" else 2
    except (OSError, UnicodeError, json.JSONDecodeError, PolicyError, ValueError) as exc:
        payload = {
            "schema_version": "nscs.error.v1",
            "decision": "FREEZE",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }
        _emit(payload, getattr(args, "output", None))
        return 2
    raise AssertionError("unreachable")
