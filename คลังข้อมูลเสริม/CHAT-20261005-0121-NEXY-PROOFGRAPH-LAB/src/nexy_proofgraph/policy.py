from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class NEXYPolicy:
    current_requirement_rows: int
    current_build_rows: int
    deprecated_registry_count: int
    historical_partial_registry_count: int
    ontology_entity_count: int
    proposal_root: str
    protected_repo_name_fragment: str
    scan_max_bytes: int

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "NEXYPolicy":
        n = data["nexy"]
        return cls(
            current_requirement_rows=int(n["current_requirement_rows"]),
            current_build_rows=int(n["current_build_rows"]),
            deprecated_registry_count=int(n["deprecated_registry_count"]),
            historical_partial_registry_count=int(n["historical_partial_registry_count"]),
            ontology_entity_count=int(n["ontology_entity_count"]),
            proposal_root=str(data.get("proposal_root", "คลังข้อมูลเสริม")),
            protected_repo_name_fragment=str(data.get("protected_repo_name_fragment", "NEXY.AI")),
            scan_max_bytes=int(data.get("scan_max_bytes", 2_000_000)),
        )


def load_policy(path: Path) -> NEXYPolicy:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return NEXYPolicy.from_mapping(raw)
