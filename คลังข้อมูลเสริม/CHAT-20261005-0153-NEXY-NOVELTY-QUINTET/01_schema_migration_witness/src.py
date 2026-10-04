"""AI-PROPOSED: deterministic witness engine for reversible data migrations."""
from __future__ import annotations

import copy
import json
from typing import Any, Iterable, Mapping


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def apply_plan(record: Mapping[str, Any], plan: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Apply a closed set of deterministic migration operations to one record.

    Unknown operations fail closed. Input is never mutated.
    """
    out = copy.deepcopy(dict(record))
    for step_index, step in enumerate(plan):
        op = step.get("op")
        if op == "rename":
            src = step.get("from")
            dst = step.get("to")
            if not isinstance(src, str) or not isinstance(dst, str) or not src or not dst:
                raise ValueError(f"invalid rename at step {step_index}")
            if src in out:
                if dst in out and dst != src:
                    raise ValueError(f"rename collision: {src!r} -> {dst!r}")
                out[dst] = out.pop(src)
        elif op == "drop":
            field = step.get("field")
            if not isinstance(field, str) or not field:
                raise ValueError(f"invalid drop at step {step_index}")
            out.pop(field, None)
        elif op == "add_default":
            field = step.get("field")
            if not isinstance(field, str) or not field:
                raise ValueError(f"invalid add_default at step {step_index}")
            if field not in out:
                out[field] = copy.deepcopy(step.get("value"))
        elif op == "copy":
            src = step.get("from")
            dst = step.get("to")
            if not isinstance(src, str) or not isinstance(dst, str) or not src or not dst:
                raise ValueError(f"invalid copy at step {step_index}")
            if src in out:
                if dst in out and not step.get("overwrite", False):
                    raise ValueError(f"copy collision: {src!r} -> {dst!r}")
                out[dst] = copy.deepcopy(out[src])
        elif op == "cast":
            field = step.get("field")
            target = step.get("to")
            if not isinstance(field, str) or field not in out:
                continue
            value = out[field]
            if target == "str":
                out[field] = str(value)
            elif target == "int":
                if isinstance(value, bool):
                    raise ValueError("bool-to-int cast forbidden")
                out[field] = int(value)
            elif target == "float":
                if isinstance(value, bool):
                    raise ValueError("bool-to-float cast forbidden")
                out[field] = float(value)
            else:
                raise ValueError(f"unsupported cast target: {target!r}")
        else:
            raise ValueError(f"unsupported migration operation: {op!r}")
    return out


def evaluate_round_trip(
    records: Iterable[Mapping[str, Any]],
    forward_plan: Iterable[Mapping[str, Any]],
    reverse_plan: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Prove or refute losslessness over an explicit witness corpus."""
    forward = list(forward_plan)
    reverse = list(reverse_plan)
    mismatches: list[dict[str, Any]] = []
    migrated: list[dict[str, Any]] = []

    for index, record in enumerate(records):
        before = copy.deepcopy(dict(record))
        after_forward = apply_plan(before, forward)
        after_reverse = apply_plan(after_forward, reverse)
        migrated.append(after_forward)
        if _canonical(before) != _canonical(after_reverse):
            mismatches.append(
                {
                    "index": index,
                    "before": before,
                    "after_round_trip": after_reverse,
                }
            )

    witness_count = len(migrated)
    if witness_count == 0:
        status = "NOT_VERIFIED"
        lossless = False
    else:
        status = "PASS" if not mismatches else "FAIL"
        lossless = not mismatches

    return {
        "lossless": lossless,
        "status": status,
        "witness_count": witness_count,
        "mismatches": mismatches,
        "forward_outputs": migrated,
    }
