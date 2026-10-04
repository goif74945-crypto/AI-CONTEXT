from __future__ import annotations

from typing import Any

from .distiller import distill
from .emergence import analyze_plan


def distill_emergent_risk(plan: dict[str, Any], finding_code: str) -> dict[str, Any]:
    """Minimize the plan steps required to reproduce a specific emergent-risk finding."""
    original_steps = plan.get("steps", [])
    if not isinstance(original_steps, list):
        raise ValueError("plan.steps must be a list")

    def oracle(steps: list[dict[str, Any]]) -> str | None:
        candidate = {"artifacts": plan.get("artifacts", {}), "steps": steps}
        result = analyze_plan(candidate)
        codes = {finding["code"] for finding in result.get("findings", [])}
        return finding_code if finding_code in codes else None

    return distill(original_steps, oracle, finding_code)
