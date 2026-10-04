from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from integration.test_fabric import safe_payload
from integration.fabric import evaluate_execution


def main() -> int:
    iterations = 2000
    payload = safe_payload()
    started = time.perf_counter()
    last = None
    for _ in range(iterations):
        last = evaluate_execution(payload)
    elapsed = time.perf_counter() - started
    print(json.dumps({
        "status": "OBSERVED",
        "iterations": iterations,
        "elapsed_seconds": round(elapsed, 6),
        "decisions_per_second": round(iterations / elapsed, 2) if elapsed else None,
        "decision_id": last["decision_id"] if last else None,
        "environment_note": "local ephemeral container; not production performance evidence",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
