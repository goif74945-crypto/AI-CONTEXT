from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .canonical import canonical_json
from .model import SurfaceFormatError, load_surface
from .rules import RULES
from .validator import validate_surface


def _print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))


def cmd_validate(path: str) -> int:
    try:
        surface = load_surface(path)
        report = validate_surface(surface)
    except (OSError, SurfaceFormatError, ValueError) as exc:
        _print_json({"status": "FAIL", "format_error": str(exc)})
        return 1
    _print_json(report.as_dict())
    return {"PASS": 0, "PARTIAL": 2, "FAIL": 1}[report.status]


def cmd_rules() -> int:
    _print_json([
        {
            "rule_id": r.rule_id,
            "standard": r.standard,
            "requirement": r.requirement,
            "default_severity": r.default_severity,
            "claim_boundary": r.claim_boundary,
        }
        for r in RULES
    ])
    return 0


def cmd_digest(path: str) -> int:
    try:
        surface = load_surface(path)
    except (OSError, SurfaceFormatError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    from .canonical import sha256_json
    print(sha256_json(surface))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="naicv", description="Validate proposed NEXY abstract UI accessibility-integrity surfaces")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("surface")
    sub.add_parser("rules")
    digest = sub.add_parser("digest")
    digest.add_argument("surface")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        return cmd_validate(args.surface)
    if args.command == "rules":
        return cmd_rules()
    if args.command == "digest":
        return cmd_digest(args.surface)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
