from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any

from .model import CompiledExperiment


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {k: _jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_jsonable(v) for v in value)
    return value


def canonical_contract_json(contract: CompiledExperiment) -> str:
    return json.dumps(_jsonable(contract), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def contract_hash(contract: CompiledExperiment) -> str:
    payload = canonical_contract_json(contract).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def pretty_contract_json(contract: CompiledExperiment) -> str:
    return json.dumps(_jsonable(contract), ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
