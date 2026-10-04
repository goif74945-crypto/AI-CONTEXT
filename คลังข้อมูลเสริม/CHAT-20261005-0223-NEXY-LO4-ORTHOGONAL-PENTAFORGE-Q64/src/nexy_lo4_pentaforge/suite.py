from __future__ import annotations

from dataclasses import dataclass

from .causal_explanation import ExplanationFaithfulnessReport
from .equivalence import EquivalenceWitness
from .robotics_envelope import MotionEnvelopeReport
from .schedulability import SchedulabilityReport
from .symmetry import SymmetryQuotientReport


@dataclass(frozen=True)
class PentaforgeSnapshot:
    symmetry: SymmetryQuotientReport
    explanation: ExplanationFaithfulnessReport
    robotics: MotionEnvelopeReport
    schedulability: SchedulabilityReport
    equivalence: EquivalenceWitness

    @property
    def advisory_pass(self) -> bool:
        return (
            self.explanation.passed
            and self.robotics.safe
            and self.schedulability.schedulable
            and self.equivalence.equivalent
        )
