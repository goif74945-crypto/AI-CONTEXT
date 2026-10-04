from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .contracts import Decision, Finding, Verdict


class DebtKind(str, Enum):
    ASSUMPTION = "ASSUMPTION"
    STALE_EVIDENCE = "STALE_EVIDENCE"
    CONTRADICTION = "CONTRADICTION"
    ORPHAN_REQUIREMENT = "ORPHAN_REQUIREMENT"
    UNVERIFIED_COMPLETION = "UNVERIFIED_COMPLETION"


_KIND_WEIGHT: dict[DebtKind, int] = {
    DebtKind.ASSUMPTION: 2,
    DebtKind.STALE_EVIDENCE: 3,
    DebtKind.CONTRADICTION: 5,
    DebtKind.ORPHAN_REQUIREMENT: 4,
    DebtKind.UNVERIFIED_COMPLETION: 5,
}


@dataclass(frozen=True, slots=True)
class DebtItem:
    item_id: str
    kind: DebtKind
    exposure: int
    age_units: int
    blocks_release: bool = False

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise ValueError("item_id must not be empty")
        if not 0 <= self.exposure <= 100:
            raise ValueError("exposure must be in [0, 100]")
        if self.age_units < 0:
            raise ValueError("age_units must be >= 0")


class CognitiveDebtLedger:
    """Turn epistemic shortcuts into measurable release debt."""

    ENGINE = "cognitive-debt-ledger"

    def assess(
        self,
        items: Iterable[DebtItem],
        *,
        review_threshold: int = 120,
        freeze_threshold: int = 240,
    ) -> Decision:
        if not 0 <= review_threshold <= freeze_threshold:
            raise ValueError("thresholds must satisfy 0 <= review <= freeze")

        ordered = sorted(tuple(items), key=lambda x: x.item_id)
        findings: list[Finding] = []
        line_items: list[tuple[str, str, int]] = []
        total = 0

        for item in ordered:
            age_factor = min(5, 1 + item.age_units // 10)
            debt = (_KIND_WEIGHT[item.kind] * item.exposure * age_factor) // 10
            if item.blocks_release:
                debt += 100
                findings.append(
                    Finding(
                        "DEBT_RELEASE_BLOCKER",
                        100,
                        f"Debt item {item.item_id} explicitly blocks release.",
                        (item.kind.value,),
                    )
                )
            total += debt
            line_items.append((item.item_id, item.kind.value, debt))

        if total >= freeze_threshold:
            findings.append(
                Finding(
                    "DEBT_BUDGET_EXHAUSTED",
                    95,
                    "Cognitive debt exceeds freeze threshold.",
                    (f"total={total}", f"freeze={freeze_threshold}"),
                )
            )
            verdict = Verdict.FREEZE
        elif total >= review_threshold:
            findings.append(
                Finding(
                    "DEBT_REVIEW_REQUIRED",
                    70,
                    "Cognitive debt exceeds review threshold.",
                    (f"total={total}", f"review={review_threshold}"),
                )
            )
            verdict = Verdict.REVIEW
        else:
            verdict = Verdict.PASS

        if any(i.blocks_release for i in ordered):
            verdict = Verdict.FREEZE

        health = max(0, 100 - min(100, total * 100 // max(freeze_threshold, 1)))
        return Decision(
            engine=self.ENGINE,
            verdict=verdict,
            score=health,
            findings=tuple(findings),
            payload={
                "total_debt": total,
                "review_threshold": review_threshold,
                "freeze_threshold": freeze_threshold,
                "line_items": tuple(line_items),
            },
        )
