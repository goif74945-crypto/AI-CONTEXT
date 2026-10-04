from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import DeltaEngine, ValidationError, canonical_json


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic authority/context delta analyzer")
    parser.add_argument("base", type=Path)
    parser.add_argument("current", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-change", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        base = _load(args.base)
        current = _load(args.current)
        report = DeltaEngine().compare(base, current)
    except ValidationError as exc:
        print(f"FREEZE: {exc}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        return 3

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "
"
    try:
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except OSError as exc:
        print(f"OUTPUT_ERROR: {exc}", file=sys.stderr)
        return 3

    if args.fail_on_change and report["summary"]["change_count"]:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
