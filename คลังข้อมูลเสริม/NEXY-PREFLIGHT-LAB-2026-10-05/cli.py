from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from nexy_preflight import TaskContract, evaluate_contract


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a NEXY PREFLIGHT task contract")
    parser.add_argument("contract", type=Path)
    args = parser.parse_args(argv)
    raw = json.loads(args.contract.read_text(encoding="utf-8"))
    envelope = evaluate_contract(TaskContract.from_mapping(raw))
    print(json.dumps(envelope.to_primitive(), ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if envelope.decision.value == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
