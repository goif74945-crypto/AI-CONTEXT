from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .contracts import Decision, Finding, Verdict


class ActionMode(str, Enum):
    EXECUTE = "EXECUTE"
    EXECUTE_WITH_EXPLANATION = "EXECUTE_WITH_EXPLANATION"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    FREEZE = "FREEZE"


@dataclass(frozen=True, slots=True)
class TrustContext:
    uncertainty: int
    irreversibility: int
    impact: int
    evidence_strength: int
    user_effort: int
    scope_clarity: int

    def __post_init__(self) -> None:
        for name in (
            "uncertainty",
            "irreversibility",
            "impact",
            "evidence_strength",
            "user_effort",
            "scope_clarity",
        ):
            value = getattr(self, name)
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be in [0, 100]")


class HumanTrustBudgetGovernor:
    """Choose the smallest safe interaction burden for an action."""

    ENGINE = "human-trust-budget-governor"

    def govern(self, context: TrustContext) -> Decision:
        risk = (
            context.uncertainty * 3
            + context.irreversibility * 3
            + context.impact * 2
            + (100 - context.evidence_strength) * 3
            + (100 - context.scope_clarity) * 2
        ) // 13

        findings: list[Finding] = []
        if context.scope_clarity < 40:
            findings.append(Finding("TRUST_SCOPE_UNCLEAR", 90, "Scope clarity is below safe threshold."))
        if context.evidence_strength < 30 and context.impact >= 70:
            findings.append(Finding("TRUST_WEAK_EVIDENCE_HIGH_IMPACT", 95, "High-impact action lacks evidence."))
        if context.irreversibility >= 80:
            findings.append(Finding("TRUST_IRREVERSIBLE", 85, "Action is highly irreversible."))

        if any(f.severity >= 90 for f in findings) or risk >= 80:
            mode = ActionMode.FREEZE
            verdict = Verdict.FREEZE
        elif risk >= 60 or context.irreversibility >= 60:
            mode = ActionMode.REQUIRE_CONFIRMATION
            verdict = Verdict.REVIEW
        elif risk >= 30:
            mode = ActionMode.EXECUTE_WITH_EXPLANATION
            verdict = Verdict.PASS
        else:
            mode = ActionMode.EXECUTE
            verdict = Verdict.PASS

        explanation_budget = max(1, min(100, risk + (100 - context.user_effort) // 4))
        autonomy_budget = max(0, 100 - risk)

        return Decision(
            engine=self.ENGINE,
            verdict=verdict,
            score=autonomy_budget,
            findings=tuple(findings),
            payload={
                "risk": risk,
                "action_mode": mode.value,
                "autonomy_budget": autonomy_budget,
                "explanation_budget": explanation_budget,
            },
        )
