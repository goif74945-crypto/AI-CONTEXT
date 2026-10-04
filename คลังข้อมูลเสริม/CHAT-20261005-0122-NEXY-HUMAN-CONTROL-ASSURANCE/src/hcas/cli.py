from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .validator import validate_manifest


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hcas",
        description="Validate an advisory NEXY human-control-surface manifest.",
    )
    parser.add_argument("manifest", type=Path, help="Path to manifest JSON")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print deterministic JSON report")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        raw = args.manifest.read_text(encoding="utf-8")
        manifest = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 64

    report = validate_manifest(manifest)
    print(
        json.dumps(
            report.to_dict(),
            ensure_ascii=False,
            sort_keys=True,
            indent=2 if args.pretty else None,
        )
    )
    return 0 if report.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
