from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes
from .model import Trace


def load_trace(path: str | Path) -> Trace:
    with Path(path).open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return Trace.from_raw(raw)


def write_canonical_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(canonical_json_bytes(value) + b"\n")
