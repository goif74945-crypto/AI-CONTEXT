from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_def import ActionKind, DirectiveEpochFirewall, DirectiveEvent, DirectiveOperation  # noqa: E402

N = 20000


def main() -> int:
    fw = DirectiveEpochFirewall()
    start = time.perf_counter()
    fw.apply(
        DirectiveEvent(
            event_id="e0",
            directive_id="d0",
            operation=DirectiveOperation.NEW,
            allowed_actions=(ActionKind.READ, ActionKind.REVERSIBLE_WRITE),
        )
    )
    for i in range(1, N + 1):
        fw.apply(
            DirectiveEvent(
                event_id=f"e{i}",
                directive_id=f"d{i}",
                operation=DirectiveOperation.REPLACE,
                expected_epoch=i,
                allowed_actions=(ActionKind.READ, ActionKind.REVERSIBLE_WRITE),
                constraints={"revision": i},
            )
        )
    build_seconds = time.perf_counter() - start

    replay_start = time.perf_counter()
    replayed = DirectiveEpochFirewall.replay_journal(fw.journal)
    replay_seconds = time.perf_counter() - replay_start

    assert replayed.state.state_hash == fw.state.state_hash
    assert replayed.journal_head == fw.journal_head
    print(f"events={N + 1}")
    print(f"build_seconds={build_seconds:.6f}")
    print(f"replay_seconds={replay_seconds:.6f}")
    print(f"build_events_per_second={(N + 1) / build_seconds:.2f}")
    print(f"replay_events_per_second={(N + 1) / replay_seconds:.2f}")
    print(f"journal_records={len(fw.journal)}")
    print("final_replay_match=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
