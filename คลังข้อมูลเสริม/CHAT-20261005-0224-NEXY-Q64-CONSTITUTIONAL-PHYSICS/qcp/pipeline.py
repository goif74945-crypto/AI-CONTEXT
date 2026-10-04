from __future__ import annotations

from dataclasses import dataclass

from .fixed import Q64
from .uncertainty import UncertaintyStage, UncertaintyMassCompiler
from .robustness import LinearFeature, DecisionRobustnessEngine
from .budget import BudgetState, Reservation, VectorBudgetReactor
from .reversibility import ReversibilityPolicy, ReversibilityHalfLifeScheduler
from .expectation import Consequence, ExpectationDivergenceBarrier


@dataclass(frozen=True, slots=True)
class PipelineDecision:
    status: str
    engine_statuses: tuple[tuple[str, str], ...]


class ConstitutionalPhysicsPipeline:
    """Conservative composition demo. It grants no authority beyond its input contracts."""

    def evaluate_demo_case(self, *, force_preview_divergence: bool = False) -> PipelineDecision:
        q = Q64.from_decimal

        umc = UncertaintyMassCompiler().compile([
            UncertaintyStage("normalize", q("0.30"), q("0.05"), q("0.10"), q("0.25"), ("E:normalize",)),
            UncertaintyStage("verify", q("0.25"), q("0.00"), q("0.15"), q("0.10"), ("E:verify",)),
        ])

        drc = DecisionRobustnessEngine().certify([
            LinearFeature("evidence", q("0.8"), q("1.0"), q("0.05")),
            LinearFeature("residual_uncertainty", q("-0.5"), q("0.10"), q("0.02")),
        ], bias=q("0.15"), threshold=q("0.70"))

        budget_engine = VectorBudgetReactor()
        state = BudgetState.create({"privacy": q("1"), "compute": q("10"), "irreversibility": q("1")})
        state, vbr = budget_engine.reserve(
            state,
            Reservation.create("demo", {"privacy": q("0.10"), "compute": q("2"), "irreversibility": q("0.10")}),
        )

        rhl = ReversibilityHalfLifeScheduler().assess(
            ReversibilityPolicy(q("1"), q("0.95"), q("0.70"), 12),
            current_tick=1,
            checkpoint_guard_ticks=1,
        )

        preview = [
            Consequence("data_mutation", q("0.10"), q("1")),
            Consequence("external_message", q("0.20"), q("0.8")),
        ]
        actual = [
            Consequence("data_mutation", q("0.10" if not force_preview_divergence else "0.90"), q("1")),
            Consequence("external_message", q("0.20"), q("0.8")),
        ]
        edb = ExpectationDivergenceBarrier().compare(preview, actual, tolerance=q("0.05"))

        statuses = (
            ("UMC", umc.status),
            ("DRC", drc.status),
            ("VBR", vbr.status),
            ("RHL", rhl.status),
            ("EDB", edb.status),
        )
        acceptable = {
            "UMC": {"PASS"},
            "DRC": {"CERTIFY_ALLOW"},
            "VBR": {"PASS"},
            "RHL": {"PASS"},
            "EDB": {"PASS"},
        }
        overall = "PASS" if all(status in acceptable[name] for name, status in statuses) else "FREEZE"
        return PipelineDecision(overall, statuses)
