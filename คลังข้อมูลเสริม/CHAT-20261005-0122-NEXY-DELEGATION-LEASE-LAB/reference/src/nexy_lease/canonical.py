from __future__ import annotations

import hashlib
import json
from typing import Any

from .model import Plan


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def plan_fingerprint(plan: Plan) -> str:
    return sha256_hex(canonical_json(plan.to_dict()))
