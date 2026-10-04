from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .canonical import sha256_hex
from .gate import evaluate_bundle


def _load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(value: Any) -> None:
    json.dump(value, sys.stdout, ensure_ascii=False, sort_keys=True, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ncvg", description="NEXY Companion Verification Gate")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Evaluate a verification bundle using fail-closed semantics")
    validate.add_argument("bundle", help="Path to bundle JSON or '-' for stdin")

    manifest = sub.add_parser("manifest", help="Compute deterministic SHA-256 for a JSON bundle")
    manifest.add_argument("bundle", help="Path to bundle JSON or '-' for stdin")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        bundle = _load_json(args.bundle)
    except (OSError, json.JSONDecodeError) as exc:
        _write_json({"status": "FAIL", "decision": "FREEZE", "error": f"INPUT_ERROR: {exc}"})
        return 64

    if args.command == "manifest":
        _write_json({"sha256": sha256_hex(bundle)})
        return 0

    decision = evaluate_bundle(bundle)
    _write_json(decision.to_dict())
    return 0 if decision.allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
