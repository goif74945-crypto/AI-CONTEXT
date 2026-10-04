from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .common import ContractError, canonical_json
from .counterexample import distill
from .example_linter import lint_examples
from .freshness import plan_revalidation
from .recovery import plan_recovery
from .unsat_core import find_minimal_core

_COMMANDS = {
    "counterexample": distill,
    "unsat-core": find_minimal_core,
    "freshness": plan_revalidation,
    "lint-examples": lint_examples,
    "recovery": plan_recovery,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nexy-aqt")
    parser.add_argument("command", choices=sorted(_COMMANDS))
    parser.add_argument("input", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = _COMMANDS[args.command](payload)
    except (OSError, json.JSONDecodeError, ContractError, TypeError, ValueError) as exc:
        sys.stderr.write(canonical_json({"status": "FREEZE", "reason_codes": ["INVALID_INPUT"], "error": str(exc)}) + "\n")
        return 2
    sys.stdout.write(canonical_json(result) + "\n")
    return 0 if result.get("status") in {"PASS", "FREEZE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
