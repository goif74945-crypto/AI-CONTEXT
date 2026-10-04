from __future__ import annotations

import argparse
import time

from freeze_bridge import compile_mapping


PAYLOAD = {
    "protocol_version": "1.1",
    "event_id": "benchmark-event",
    "reason_code": "MISSING_REQUIRED_INPUT",
    "status": "FROZEN",
    "blocking_layer": "TASK_CONTRACT",
    "recovery_owner": "USER",
    "disclosure": "PUBLIC",
    "locale": "en",
    "dependency_recheck_safe": False,
    "missing_inputs": ["target_branch", "expected_head"],
    "evidence_refs": ["public:task-contract/42"],
    "authorized_recovery_intents": [
        "PROVIDE_REQUIRED_INPUT",
        "ADJUST_SCOPE",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=50_000)
    args = parser.parse_args()
    if args.iterations <= 0:
        parser.error("--iterations must be > 0")

    start = time.perf_counter()
    last = None
    for _ in range(args.iterations):
        last = compile_mapping(PAYLOAD)
    elapsed = time.perf_counter() - start
    rate = args.iterations / elapsed

    print(
        f"iterations={args.iterations} elapsed_seconds={elapsed:.6f} "
        f"ops_per_second={rate:.2f} "
        f"fingerprint={last['fingerprint'] if last else 'none'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
