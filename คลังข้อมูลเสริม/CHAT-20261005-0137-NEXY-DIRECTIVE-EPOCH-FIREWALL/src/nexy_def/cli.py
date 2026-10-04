from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import DirectiveEpochFirewall
from .model import ActionKind, DirectiveEvent, DirectiveOperation


def event_from_dict(data: dict) -> DirectiveEvent:
    return DirectiveEvent(
        event_id=data["event_id"],
        directive_id=data["directive_id"],
        operation=DirectiveOperation(data["operation"]),
        expected_epoch=data.get("expected_epoch"),
        allowed_actions=tuple(ActionKind(x) for x in data.get("allowed_actions", [])),
        constraints=data.get("constraints", {}),
        note=data.get("note"),
    )


def run_scenario(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    engine = DirectiveEpochFirewall()
    prepared = {}
    decisions = []

    for step in raw["steps"]:
        op = step["type"]
        if op == "directive":
            engine.apply(event_from_dict(step["event"]))
        elif op == "prepare":
            action = engine.prepare_action(
                step["action_id"],
                ActionKind(step["kind"]),
                step.get("payload", {}),
            )
            if step.get("attach_approval"):
                action = type(action)(
                    **{**action.__dict__, "approval_binding": engine.expected_approval_binding(action)}
                )
            prepared[step["save_as"]] = action
        elif op == "commit":
            d = engine.commit_gate(prepared[step["action"]])
            decisions.append({"status": d.status.value, "code": d.code, "reason": d.reason})
        else:
            raise ValueError(f"unknown step type: {op}")

    return {
        "final_state": engine.state.normalized(),
        "state_hash": engine.state.state_hash,
        "decisions": decisions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="NEXY Directive Epoch Firewall reference scenario runner")
    parser.add_argument("scenario", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_scenario(args.scenario), ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
