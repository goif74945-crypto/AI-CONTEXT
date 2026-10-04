from __future__ import annotations

import random
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_def import (  # noqa: E402
    ActionKind,
    DecisionStatus,
    DirectiveEpochFirewall,
    DirectiveEvent,
    DirectiveOperation,
)

SEED = 20261005
TRIALS = 5000
KINDS = tuple(ActionKind)


def choose_nonempty_subset(rng: random.Random, base: tuple[ActionKind, ...] = KINDS) -> tuple[ActionKind, ...]:
    chosen = tuple(k for k in base if rng.choice([True, False]))
    return chosen or (rng.choice(base),)


def main() -> int:
    rng = random.Random(SEED)
    stale_attempts = 0
    current_attempts = 0
    for i in range(TRIALS):
        fw = DirectiveEpochFirewall()
        allowed = choose_nonempty_subset(rng)
        fw.apply(
            DirectiveEvent(
                event_id=f"t{i}-e1",
                directive_id=f"t{i}-d1",
                operation=DirectiveOperation.NEW,
                allowed_actions=allowed,
                constraints={"trial": i, "mode": "strict"},
            )
        )
        kind = rng.choice(allowed)
        action = fw.prepare_action(f"t{i}-a1", kind, {"trial": i, "op": kind.value})
        if kind is ActionKind.IRREVERSIBLE_WRITE and rng.choice([True, False]):
            action = replace(action, approval_binding=fw.expected_approval_binding(action))

        mutation = rng.choice(["none", "replace", "narrow", "revoke"])
        if mutation == "replace":
            fw.apply(
                DirectiveEvent(
                    event_id=f"t{i}-e2",
                    directive_id=f"t{i}-d2",
                    operation=DirectiveOperation.REPLACE,
                    expected_epoch=1,
                    allowed_actions=choose_nonempty_subset(rng),
                    constraints={"trial": i, "revision": 2},
                )
            )
        elif mutation == "narrow":
            fw.apply(
                DirectiveEvent(
                    event_id=f"t{i}-e2",
                    directive_id=f"t{i}-d1-n",
                    operation=DirectiveOperation.NARROW,
                    expected_epoch=1,
                    allowed_actions=choose_nonempty_subset(rng, allowed),
                    constraints={"trial": i, "narrowed": True},
                )
            )
        elif mutation == "revoke":
            fw.apply(
                DirectiveEvent(
                    event_id=f"t{i}-e2",
                    directive_id=f"t{i}-d1",
                    operation=DirectiveOperation.REVOKE,
                    expected_epoch=1,
                )
            )

        decision = fw.commit_gate(action)
        if mutation == "none":
            current_attempts += 1
            if kind is ActionKind.IRREVERSIBLE_WRITE and action.approval_binding is None:
                assert decision.status is DecisionStatus.REJECT
            else:
                assert decision.status is DecisionStatus.ALLOW
        else:
            stale_attempts += 1
            assert decision.status is not DecisionStatus.ALLOW, (i, mutation, decision)

        replayed = DirectiveEpochFirewall.replay_journal(fw.journal)
        assert replayed.state.state_hash == fw.state.state_hash
        assert replayed.journal_head == fw.journal_head

    print(
        f"PASS adversarial trials={TRIALS} seed={SEED} "
        f"stale_attempts={stale_attempts} current_attempts={current_attempts}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
