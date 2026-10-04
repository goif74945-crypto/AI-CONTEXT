from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .model import Case, Observation
from .canonical import stable_hash


def _validate_fixture(data: dict[str, Any]) -> dict[str, Any]:
    required = {"case", "observation"}
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError(f"missing fixture keys: {missing}")
    case = Case(**data["case"])
    observation = Observation(**data["observation"])
    return {
        "case_hash": stable_hash(case),
        "observation_hash": stable_hash(observation),
        "status": "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NEXY Metamorphic Verification Kernel utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate-fixture", help="Validate and hash a Case/Observation JSON fixture")
    validate.add_argument("path", type=Path)
    args = parser.parse_args(argv)

    try:
        if args.command == "validate-fixture":
            data = json.loads(args.path.read_text(encoding="utf-8"))
            result = _validate_fixture(data)
            print(json.dumps(result, sort_keys=True, ensure_ascii=False))
            return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
