from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .canonical import canonical_dumps
from .errors import NumericIntegrityError
from .evaluator import evaluate
from .fixed128 import project_exact
from .units import BUILTIN_REGISTRY

MAX_INPUT_BYTES = 1_048_576


def _load_json(path: Path):
    size = path.stat().st_size
    if size > MAX_INPUT_BYTES:
        raise ValueError(f"input JSON exceeds {MAX_INPUT_BYTES} byte safety limit")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_float=str, parse_int=str)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nnik", description="NEXY Numeric Integrity Kernel reference CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    evaluate_parser = sub.add_parser("evaluate", help="evaluate one contract + observation JSON document")
    evaluate_parser.add_argument("path", type=Path)
    sub.add_parser("registry", help="emit the built-in closed unit registry")
    projection = sub.add_parser("project-fixed128", help="prove exact signed-128 fixed-point representability")
    projection.add_argument("--value", required=True)
    projection.add_argument("--quantum", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "registry":
            print(canonical_dumps({"registry": BUILTIN_REGISTRY.to_record(), "registry_digest": BUILTIN_REGISTRY.digest}))
            return 0
        if args.command == "project-fixed128":
            try:
                print(canonical_dumps({"schema_version": "1", "verdict": "ACCEPT", "projection": project_exact(args.value, args.quantum)}))
            except NumericIntegrityError as exc:
                print(canonical_dumps({
                    "schema_version": "1",
                    "verdict": "FREEZE",
                    "reason_code": exc.code,
                    "message": exc.message,
                    "details": dict(exc.details or {}),
                }))
            return 0
        document = _load_json(args.path)
        if not isinstance(document, dict) or set(document) != {"contract", "observation"}:
            raise ValueError("input document must contain exactly contract and observation")
        print(canonical_dumps(evaluate(document["contract"], document["observation"])))
        return 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError, RecursionError) as exc:
        print(canonical_dumps({"schema_version": "1", "process_error": type(exc).__name__, "message": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
