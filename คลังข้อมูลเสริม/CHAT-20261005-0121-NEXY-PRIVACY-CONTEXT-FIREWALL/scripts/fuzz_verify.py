"""Deterministic malformed-input robustness verification for NEXY PCF."""

from __future__ import annotations

import copy
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from nexy_pcf.compiler import compile_context  # noqa: E402

SEED = 20261005
CASES = 3000
TEST_KEY = b"fuzz-verification-key-32-bytes-minimum"


def load(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def main() -> int:
    rng = random.Random(SEED)
    weird = [None, True, False, 0, -1, 1.5, "", "MYSTERY", [], ["x"], {}, {"x": 1}]
    keys = [
        ("env", "policy_version"),
        ("env", "purpose"),
        ("env", "destination"),
        ("env", "decision_time"),
        ("env", "required_fields"),
        ("env", "fields"),
        ("dest", "id"),
        ("dest", "boundary"),
        ("dest", "allowed_purposes"),
        ("dest", "max_classification"),
        ("dest", "max_retention_seconds"),
        ("dest", "can_retain"),
        ("policy", "version"),
        ("policy", "known_purposes"),
        ("policy", "default_retention_seconds"),
        ("policy", "max_retention_seconds"),
        ("policy", "deny_external_classifications"),
    ]
    failures: list[dict[str, object]] = []

    for case_id in range(CASES):
        env = load("envelope-allow.json")
        dest = load("provider-alpha.json")
        policy = load("policy.json")

        for _ in range(rng.randint(1, 4)):
            target, key = rng.choice(keys)
            value = copy.deepcopy(rng.choice(weird))
            {"env": env, "dest": dest, "policy": policy}[target][key] = value

        fields = env.get("fields")
        if isinstance(fields, list) and fields and rng.random() < 0.75:
            field = rng.choice(fields)
            if isinstance(field, dict):
                field_key = rng.choice(
                    ["id", "value", "classification", "purposes", "allowed_destinations", "retention_seconds"]
                )
                field[field_key] = copy.deepcopy(rng.choice(weird))

        try:
            result = compile_context(env, dest, policy, receipt_key=TEST_KEY)
            json.dumps(result, allow_nan=False)
            if result.get("decision") not in {"ALLOW", "FREEZE"}:
                failures.append({"case": case_id, "kind": "BAD_DECISION"})
            if result.get("decision") == "FREEZE" and result.get("payload") is not None:
                failures.append({"case": case_id, "kind": "FREEZE_WITH_PAYLOAD"})
        except Exception as exc:  # verification harness records unexpected escapes
            failures.append({"case": case_id, "kind": type(exc).__name__, "detail": str(exc)})

        if len(failures) >= 20:
            break

    summary = {
        "seed": SEED,
        "cases": CASES,
        "failure_count": len(failures),
        "failures": failures,
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
