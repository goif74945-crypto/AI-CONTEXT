from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .compress import compress_milestones
from .debt import AckRecord, build_ack_debt
from .delta import compile_outcome_delta
from .models import OperatorSignal
from .routing import route_signal
from .salience import classify_salience


def _load(path: str | None) -> Any:
    text = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    return json.loads(text)


def _emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nexy-signal")
    parser.add_argument("command", choices=("classify", "route", "compress", "delta", "debt"))
    parser.add_argument("--input", help="JSON file; stdin when omitted")
    args = parser.parse_args(argv)
    try:
        raw = _load(args.input)
        if args.command == "classify":
            result = classify_salience(OperatorSignal.from_dict(raw)).as_dict()
        elif args.command == "route":
            signal = OperatorSignal.from_dict(raw["signal"])
            quiet = raw.get("quiet_mode", False)
            if not isinstance(quiet, bool):
                raise ValueError("quiet_mode must be boolean")
            result = route_signal(signal, quiet_mode=quiet).as_dict()
        elif args.command == "compress":
            result = compress_milestones(OperatorSignal.from_dict(x) for x in raw["signals"]).as_dict()
        elif args.command == "delta":
            redactions = raw.get("redact_paths", [])
            if not isinstance(redactions, list):
                raise ValueError("redact_paths must be a list")
            result = compile_outcome_delta(raw["before"], raw["after"], redact_paths=redactions).as_dict()
        else:
            signals = [OperatorSignal.from_dict(x) for x in raw["signals"]]
            acks = [AckRecord.from_dict(x) for x in raw.get("acknowledgements", [])]
            result = build_ack_debt(signals, acks, current_sequence=raw["current_sequence"]).as_dict()
        _emit({"status": "PASS", "result": result})
        return 0
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        _emit({"error": str(exc), "status": "FREEZE"})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
