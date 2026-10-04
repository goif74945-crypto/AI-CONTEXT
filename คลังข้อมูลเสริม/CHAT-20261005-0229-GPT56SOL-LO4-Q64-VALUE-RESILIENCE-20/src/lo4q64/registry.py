from __future__ import annotations

from .engines import SPECS


def list_concepts() -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "concept_id": spec.concept_id,
            "title": spec.title,
            "required_inputs": spec.required_inputs,
            "summary": spec.summary,
        }
        for _, spec in sorted(SPECS.items())
    )
