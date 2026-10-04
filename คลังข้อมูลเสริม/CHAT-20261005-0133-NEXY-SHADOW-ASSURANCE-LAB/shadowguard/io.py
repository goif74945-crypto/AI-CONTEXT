from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import DecisionRecord


def load_jsonl(path: str | Path) -> tuple[DecisionRecord, ...]:
    p = Path(path)
    records: list[DecisionRecord] = []
    with p.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
                if not isinstance(raw, dict):
                    raise ValueError("record must be a JSON object")
                records.append(DecisionRecord.from_mapping(raw))
            except Exception as exc:
                raise ValueError(f"{p}:{line_no}: {exc}") from exc
    return tuple(records)
