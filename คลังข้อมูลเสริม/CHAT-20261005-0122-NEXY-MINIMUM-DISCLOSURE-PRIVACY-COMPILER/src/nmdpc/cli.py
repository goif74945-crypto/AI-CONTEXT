from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .compiler import (
    Classification,
    DataRule,
    DisclosureCompiler,
    Recipient,
    RecipientTrust,
    TaskRequest,
    Transform,
)


def _load(path: Path) -> tuple[TaskRequest, list[DataRule]]:
    raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    t = raw["task"]
    recipient = Recipient(
        recipient_id=t["recipient"]["recipient_id"],
        trust=RecipientTrust(t["recipient"]["trust"]),
    )
    task = TaskRequest(
        purpose=t["purpose"],
        capabilities=frozenset(t["capabilities"]),
        recipient=recipient,
        requested_retention_seconds=int(t["requested_retention_seconds"]),
        consents=frozenset(t.get("consents", [])),
    )
    rules = [
        DataRule(
            field_name=r["field_name"],
            classification=Classification(r["classification"]),
            allowed_purposes=frozenset(r["allowed_purposes"]),
            required_for_capabilities=frozenset(r["required_for_capabilities"]),
            recipient_value_required_for=frozenset(r.get("recipient_value_required_for", [])),
            preferred_transform=Transform(r["preferred_transform"]),
            max_retention_seconds=int(r["max_retention_seconds"]),
        )
        for r in raw["rules"]
    ]
    return task, rules


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile an NMDPC disclosure policy into a deterministic plan.")
    parser.add_argument("policy", type=Path, help="JSON policy file; payload values are not accepted by this CLI")
    args = parser.parse_args(argv)

    task, rules = _load(args.policy)
    plan = DisclosureCompiler().compile(task, rules)
    print(json.dumps(plan.as_dict(), ensure_ascii=False, sort_keys=True, indent=2))
    return 2 if plan.decision.value == "FREEZE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
