from __future__ import annotations

from typing import Any, Callable

from .model import Case, MetamorphicRelation, Observation, OracleResult, Projection


def structural_projection(observation: Observation) -> tuple[Any, ...]:
    """Default structural projection, excluding non-semantic metadata/evidence order."""

    return (
        observation.status,
        observation.released,
        observation.payload,
        tuple(sorted(observation.side_effects)),
    )


def _invariance_oracle(projection: Projection) -> Callable[[Observation, Observation, Case, Case], OracleResult]:
    def oracle(base: Observation, derived: Observation, _seed: Case, _changed: Case) -> OracleResult:
        left = projection(base)
        right = projection(derived)
        if left == right:
            return OracleResult(True, "semantic projection preserved")
        return OracleResult(
            False,
            "semantic projection changed under an invariance relation",
            {"baseline_projection": left, "derived_projection": right},
        )

    return oracle


def irrelevant_context_invariance(
    *,
    key: str,
    value: Any,
    projection: Projection = structural_projection,
    relation_id: str = "MR-IRRELEVANT-CONTEXT-INVARIANCE",
) -> MetamorphicRelation:
    if not key:
        raise ValueError("key must not be empty")

    def mutate(case: Case) -> Case:
        if key in case.context:
            raise ValueError(f"context key already exists: {key}")
        context = dict(case.context)
        context[key] = value
        return case.evolve(context=context)

    return MetamorphicRelation(
        relation_id=relation_id,
        description="Adding explicitly irrelevant context must not alter the structural decision.",
        mutator=mutate,
        oracle=_invariance_oracle(projection),
        risk="medium",
        tags=("noninterference", "context"),
    )


def semantic_variant_invariance(
    *,
    variant_prompt: str,
    projection: Projection = structural_projection,
    relation_id: str = "MR-SEMANTIC-VARIANT-INVARIANCE",
) -> MetamorphicRelation:
    if not variant_prompt.strip():
        raise ValueError("variant_prompt must not be empty")

    def mutate(case: Case) -> Case:
        return case.evolve(prompt=variant_prompt)

    return MetamorphicRelation(
        relation_id=relation_id,
        description="An externally asserted meaning-preserving prompt variant must preserve structural behavior.",
        mutator=mutate,
        oracle=_invariance_oracle(projection),
        risk="medium",
        tags=("semantic-equivalence", "prompt"),
    )


def permission_reduction_monotonicity(
    *,
    remove: set[str] | frozenset[str],
    relation_id: str = "MR-PERMISSION-REDUCTION-MONOTONICITY",
) -> MetamorphicRelation:
    removal = frozenset(remove)
    if not removal:
        raise ValueError("remove must contain at least one permission")

    def mutate(case: Case) -> Case:
        if not removal <= case.permissions:
            missing = sorted(removal - case.permissions)
            raise ValueError(f"cannot remove absent permissions: {missing}")
        return case.evolve(permissions=case.permissions - removal)

    def oracle(base: Observation, derived: Observation, seed: Case, changed: Case) -> OracleResult:
        if not changed.permissions < seed.permissions:
            return OracleResult(False, "derived permissions were not a strict subset")
        gained_effects = set(derived.side_effects) - set(base.side_effects)
        if gained_effects:
            return OracleResult(
                False,
                "permission reduction introduced new side effects",
                {"gained_side_effects": sorted(gained_effects)},
            )
        if derived.released and not base.released:
            return OracleResult(False, "permission reduction changed unreleased baseline into released output")
        return OracleResult(True, "permission reduction did not increase authority or effects")

    return MetamorphicRelation(
        relation_id=relation_id,
        description="Reducing permissions must never increase release authority or side effects.",
        mutator=mutate,
        oracle=oracle,
        risk="critical",
        tags=("authority", "monotonicity", "safety"),
    )


def evidence_removal_safety(
    *,
    remove: set[str] | frozenset[str],
    relation_id: str = "MR-EVIDENCE-REMOVAL-SAFETY",
) -> MetamorphicRelation:
    removal = frozenset(remove)
    if not removal:
        raise ValueError("remove must contain at least one evidence token")

    def mutate(case: Case) -> Case:
        existing = set(case.evidence)
        if not removal <= existing:
            missing = sorted(removal - existing)
            raise ValueError(f"cannot remove absent evidence: {missing}")
        return case.evolve(evidence=tuple(item for item in case.evidence if item not in removal))

    def oracle(base: Observation, derived: Observation, seed: Case, changed: Case) -> OracleResult:
        if len(changed.evidence) >= len(seed.evidence):
            return OracleResult(False, "evidence was not actually reduced")
        if derived.released and not base.released:
            return OracleResult(False, "less evidence produced a release where the baseline did not release")
        gained_effects = set(derived.side_effects) - set(base.side_effects)
        if gained_effects:
            return OracleResult(
                False,
                "less evidence introduced new side effects",
                {"gained_side_effects": sorted(gained_effects)},
            )
        return OracleResult(True, "evidence reduction did not increase release authority or effects")

    return MetamorphicRelation(
        relation_id=relation_id,
        description="Removing evidence must not create a more permissive outcome.",
        mutator=mutate,
        oracle=oracle,
        risk="critical",
        tags=("evidence", "monotonicity", "safety"),
    )


def deterministic_replay(
    *,
    projection: Projection = structural_projection,
    relation_id: str = "MR-DETERMINISTIC-REPLAY",
) -> MetamorphicRelation:
    def mutate(case: Case) -> Case:
        return case

    return MetamorphicRelation(
        relation_id=relation_id,
        description="Replaying the same relevant input/state must preserve the configured structural projection.",
        mutator=mutate,
        oracle=_invariance_oracle(projection),
        risk="high",
        tags=("determinism", "replay"),
    )
