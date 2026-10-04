from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .canonical import dumps, sha256
from .composition import compose
from .corrections import compile_corrections
from .emergence import analyze_plan
from .integration import distill_emergent_risk
from .portability import assess_portability


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _input_error(exc: Exception) -> dict[str, object]:
    result: dict[str, object] = {
        "status": "FREEZE",
        "reason": "INPUT_ERROR",
        "error_type": type(exc).__name__,
        "message": str(exc),
    }
    result["fingerprint"] = sha256(result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nexy-aux")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("compose")
    p.add_argument("input")
    p = sub.add_parser("risk")
    p.add_argument("input")
    p = sub.add_parser("portability")
    p.add_argument("input")
    p = sub.add_parser("corrections")
    p.add_argument("input")
    p = sub.add_parser("distill-risk")
    p.add_argument("input")
    p.add_argument("finding_code")

    args = parser.parse_args(argv)
    try:
        data = load(args.input)
        if args.cmd == "compose":
            result = compose(data["components"], data.get("initial_facts", []))
        elif args.cmd == "risk":
            result = analyze_plan(data)
        elif args.cmd == "portability":
            result = assess_portability(data["evidence"], data["target"], data["policy"])
        elif args.cmd == "corrections":
            result = compile_corrections(data["corrections"])
        else:
            result = distill_emergent_risk(data, args.finding_code)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        result = _input_error(exc)

    sys.stdout.write(dumps(result) + "\n")
    # REVERIFY is intentionally a blocking exit status: a shell/CI caller must not
    # mistake "proof needs refreshing" for permission to proceed.
    return 0 if result.get("status") in {"PASS", "PORTABLE", "NOT_APPLICABLE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
