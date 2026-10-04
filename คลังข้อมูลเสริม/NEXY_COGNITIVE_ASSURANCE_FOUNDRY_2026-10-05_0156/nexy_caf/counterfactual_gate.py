from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .contracts import Decision, Finding, Verdict


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    probability_bp: int
    impact: int
    detectable: bool
    reversible: bool
    mitigation_strength: int

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("scenario name must not be empty")
        if not 0 <= self.probability_bp <= 10_000:
            raise ValueError("probability_bp must be in [0, 10000]")
        if not 0 <= self.impact <= 100:
            raise ValueError("impact must be in [0, 100]")
        if not 0 <= self.mitigation_strength <= 100:
            raise ValueError("mitigation_strength must be in [0, 100]")


class CounterfactualAdoptionGate:
    """Evaluate a proposal against explicit counterfactual failure scenarios."""

    ENGINE = "counterfactual-adoption-gate"

    def evaluate(
        self,
        *,
        proposal_id: str,
        benefit_score: int,
        scenarios: Iterable[Scenario],
        mandatory_invariants_preserved: bool,
        rollback_defined: bool,
        evidence_plan_defined: bool,
        max_residual_risk: int = 35,
    ) -> Decision:
        if not proposal_id.strip():
            raise ValueError("proposal_id must not be empty")
        if not 0 <= benefit_score <= 100:
            raise ValueError("benefit_score must be in [0, 100]")
        if not 0 <= max_residual_risk <= 100:
            raise ValueError("max_residual_risk must be in [0, 100]")

        ordered = sorted(tuple(scenarios), key=lambda s: s.name)
        findings: list[Finding] = []
        residuals: list[tuple[str, int]] = []

        if not mandatory_invariants_preserved:
            findings.append(Finding("ADOPT_INVARIANT_BREAK", 100, "Mandatory invariant is not preserved."))
        if not rollback_defined:
            findings.append(Finding("ADOPT_NO_ROLLBACK", 85, "Rollback is undefined."))
        if not evidence_plan_defined:
            findings.append(Finding("ADOPT_NO_EVIDENCE_PLAN", 85, "Evidence plan is undefined."))
        if not ordered:
            findings.append(Finding("ADOPT_NO_SCENARIOS", 90, "No counterfactual scenarios were supplied."))

        for s in ordered:
            detectability_penalty = 20 if not s.detectable else 0
            reversibility_penalty = 20 if not s.reversible else 0
            base = (s.probability_bp * s.impact) // 10_000
            mitigated = (base * (100 - s.mitigation_strength)) // 100
            residual = min(100, mitigated + detectability_penalty + reversibility_penalty)
            residuals.append((s.name, residual))
            if residual > max_residual_risk:
                findings.append(
                    Finding(
                        "ADOPT_RISK_EXCEEDS_BUDGET",
                        min(100, 60 + residual // 2),
                        f"Residual risk exceeds budget for {s.name}.",
                        (f"residual={residual}", f"budget={max_residual_risk}"),
                    )
                )

        worst = max((r for _, r in residuals), default=100)
        net_score = max(0, min(100, benefit_score - worst // 2))
        hard = any(f.severity >= 85 for f in findings)
        verdict = Verdict.FREEZE if hard else (Verdict.REVIEW if findings else Verdict.PASS)

        return Decision(
            engine=self.ENGINE,
            verdict=verdict,
            score=net_score,
            findings=tuple(findings),
            payload={
                "proposal_id": proposal_id,
                "benefit_score": benefit_score,
                "worst_residual_risk": worst,
                "residual_risk": tuple(residuals),
                "max_residual_risk": max_residual_risk,
            },
        )
