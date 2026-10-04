from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .compiler import ValidationError, compile_payload


def _load(path: str | None) -> object:
    if path is None or path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nxts", description="Compile evidence-aware internal claims into a deterministic user-facing Result Capsule.")
    parser.add_argument("input", nargs="?", default="-", help="Input JSON path, or '-' for stdin")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON")
    args = parser.parse_args(argv)

    try:
        payload = _load(args.input)
        result = compile_payload(payload)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 64

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["decision"] == "RELEASE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
