from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .builder import CapsuleBuilder
from .canonical import sha256_hex
from .errors import SchemaError
from .model import AuthorityRef, Capsule, EventKind, TerminalState


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(value: Any, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")


def load_capsule(path: str | Path) -> Capsule:
    raw = load_json(path)
    if not isinstance(raw, dict):
        raise SchemaError("capsule JSON root must be an object")
    return Capsule.from_dict(raw)


def compile_plan(plan: dict[str, Any]) -> Capsule:
    required = {"project_target", "authority_refs", "events", "terminal_state"}
    missing = required - plan.keys()
    if missing:
        raise SchemaError(f"plan missing fields: {sorted(missing)}")

    refs = [AuthorityRef.from_dict(item) for item in list(plan["authority_refs"])]
    builder = CapsuleBuilder(project_target=str(plan["project_target"]), authority_refs=refs)

    for item in list(plan["events"]):
        if not isinstance(item, dict):
            raise SchemaError("plan events must be objects")
        if "kind" not in item or "payload" not in item:
            raise SchemaError("plan event requires kind and payload")
        kind = EventKind(str(item["kind"]))
        payload = dict(item["payload"])
        if kind is EventKind.AUTHORITY_RESOLVED and payload.get("fingerprint") in {None, "$AUTHORITY_FINGERPRINT"}:
            payload["fingerprint"] = builder.fingerprint
        if kind is EventKind.FINAL and payload.get("output_digest") in {None, "$AUTO"}:
            payload["output_digest"] = sha256_hex(payload.get("output"))
        builder.append(kind, payload)

    return builder.build(terminal_state=TerminalState(str(plan["terminal_state"])))
