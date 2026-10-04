from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .compiler import compile_mapping
from .model import FreezeBridgeError


def _read_payload(path: str | None) -> Any:
    if path is None or path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexy-freeze-bridge",
        description="Normalize authoritative freeze metadata into a deterministic freeze explanation contract.",
    )
    parser.add_argument("input", nargs="?", default="-", help="JSON input file, or - for stdin")
    parser.add_argument("--compact", action="store_true", help="Emit compact canonical JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = _read_payload(args.input)
        if not isinstance(payload, dict):
            raise FreezeBridgeError("top-level JSON must be an object")
        result = compile_mapping(payload)
    except (FreezeBridgeError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2

    if args.compact:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
