from __future__ import annotations

import argparse
import time

from nexy_dcr.builder import CapsuleBuilder
from nexy_dcr.model import AuthorityRef, EventKind, TerminalState
from nexy_dcr.replay import replay


def refs() -> list[AuthorityRef]:
    return [AuthorityRef(path="kernel", sha="a" * 64, role="KERNEL", rank=1)]


def make_capsule(index: int):
    builder = CapsuleBuilder(project_target="benchmark", authority_refs=refs())
    builder.append(EventKind.REQUEST, {"request_id": f"r-{index}", "objective": "benchmark"})
    builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["kernel"]})
    builder.append_authority_resolved()
    builder.append(EventKind.DECISION, {"decision": "ALLOW"})
    builder.append(EventKind.VERIFICATION, {"status": "PASS", "claim": "benchmark"})
    builder.append_final(status=TerminalState.PASS, output={"index": index})
    return builder.build(terminal_state=TerminalState.PASS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10000)
    args = parser.parse_args()
    if args.count <= 0:
        raise SystemExit("--count must be > 0")

    started = time.perf_counter()
    capsules = [make_capsule(i) for i in range(args.count)]
    build_seconds = time.perf_counter() - started

    started = time.perf_counter()
    for capsule in capsules:
        replay(capsule)
    replay_seconds = time.perf_counter() - started

    print(
        {
            "count": args.count,
            "events_per_capsule": 6,
            "build_seconds": round(build_seconds, 6),
            "replay_seconds": round(replay_seconds, 6),
            "build_capsules_per_second": round(args.count / build_seconds, 2),
            "replay_capsules_per_second": round(args.count / replay_seconds, 2),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
