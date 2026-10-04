from nexy_product_evidence.model import (
    Direction,
    ExperimentProposal,
    GuardrailSpec,
    MetricKind,
    MetricSpec,
)


def valid_proposal() -> ExperimentProposal:
    return ExperimentProposal(
        experiment_id="test-exp-001",
        title="Proof visibility",
        hypothesis="Concise proof visibility improves follow-up completion.",
        population="Eligible signed-in users completing a verified task.",
        primary_metric=MetricSpec(
            name="completion_rate",
            kind=MetricKind.PROPORTION,
            direction=Direction.HIGHER_IS_BETTER,
            baseline=0.40,
            mde_abs=0.05,
            alpha=0.05,
            power=0.80,
        ),
        guardrails=(
            GuardrailSpec(
                name="abandonment_rate",
                direction=Direction.LOWER_IS_BETTER,
                baseline=0.10,
                max_degradation_abs=0.02,
            ),
        ),
        allocation_fraction=0.5,
        duration_days=14,
    )
