from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .diff import diff_capsules
from .errors import CapsuleError
from .io import compile_plan, dump_json, load_capsule, load_json
from .receipt import public_receipt
from .replay import replay, verify_integrity


def _print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexy-dcr",
        description="AI-proposal reference tool for deterministic NEXY decision capsules.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    compile_cmd = sub.add_parser("compile", help="Seal an unhashed plan into a decision capsule")
    compile_cmd.add_argument("plan", type=Path)
    compile_cmd.add_argument("output", type=Path)

    verify_cmd = sub.add_parser("verify", help="Verify capsule hashes and chain integrity")
    verify_cmd.add_argument("capsule", type=Path)

    replay_cmd = sub.add_parser("replay", help="Replay capsule state-machine semantics")
    replay_cmd.add_argument("capsule", type=Path)

    diff_cmd = sub.add_parser("diff", help="Compare two capsules structurally")
    diff_cmd.add_argument("left", type=Path)
    diff_cmd.add_argument("right", type=Path)

    receipt_cmd = sub.add_parser("receipt", help="Emit a payload-minimized public trust receipt")
    receipt_cmd.add_argument("capsule", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "compile":
            raw = load_json(args.plan)
            if not isinstance(raw, dict):
                raise CapsuleError("plan root must be an object")
            capsule = compile_plan(raw)
            replay(capsule)
            dump_json(capsule.to_dict(), args.output)
            _print_json({"status": "PASS", "capsule_id": capsule.capsule_id, "output": str(args.output)})
            return 0

        if args.command == "verify":
            capsule = load_capsule(args.capsule)
            verify_integrity(capsule)
            _print_json({"status": "PASS", "capsule_id": capsule.capsule_id})
            return 0

        if args.command == "replay":
            report = replay(load_capsule(args.capsule))
            _print_json({"status": "PASS", "replay": report.to_dict()})
            return 0

        if args.command == "diff":
            left = load_capsule(args.left)
            right = load_capsule(args.right)
            differences = [d.to_dict() for d in diff_capsules(left, right)]
            _print_json({"status": "PASS", "divergence_count": len(differences), "differences": differences})
            return 0

        if args.command == "receipt":
            receipt = public_receipt(load_capsule(args.capsule))
            _print_json({"status": "PASS", "receipt": receipt.to_dict()})
            return 0

        parser.error(f"unsupported command: {args.command}")
        return 2
    except (CapsuleError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
