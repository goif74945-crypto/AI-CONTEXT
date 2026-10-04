from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from common import ContractError, canonical_json
from integration.fabric import evaluate_execution


EXIT_CODES = {"READY": 0, "ASK": 2, "FREEZE": 3}


def _load(argv: list[str]) -> Any:
    if len(argv) > 2:
        raise ContractError("usage: python cli.py [payload.json]")
    if len(argv) == 2:
        return json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv if argv is None else argv)
    try:
        payload = _load(argv)
        result = evaluate_execution(payload)
    except (ContractError, json.JSONDecodeError, OSError) as exc:
        error = {"kind": "NEXY_EIF_ERROR_V1", "status": "FREEZE", "reason": "INVALID_INPUT", "detail": str(exc)}
        sys.stdout.write(canonical_json(error) + "\n")
        return 64
    sys.stdout.write(canonical_json(result) + "\n")
    return EXIT_CODES[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
