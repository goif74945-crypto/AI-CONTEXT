from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping

from .contracts import Evaluation
from .q64 import Q64


def canonical_input(concept_id: str, values: Mapping[str, Q64]) -> bytes:
    payload = {
        "concept_id": concept_id,
        "inputs_raw_q64": {k: values[k].raw for k in sorted(values)},
        "schema": "lo4q64.input.v1",
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_evaluation(result: Evaluation) -> bytes:
    return json.dumps(result.as_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
