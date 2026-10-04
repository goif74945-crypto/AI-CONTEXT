from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Iterable

from .canonical import CanonicalizationError, stable_hash
from .model import (
    Case,
    MetamorphicRelation,
    Observation,
    RelationResult,
    RelationStatus,
    SystemAdapter,
    VerificationReport,
)


@dataclass(slots=True)
class VerificationEngine:
    """Executes metamorphic relations with fail-closed result classification."""

    adapter: SystemAdapter

    def run_relation(self, seed: Case, relation: MetamorphicRelation) -> RelationResult:
        try:
            seed_hash = self._safe_hash(seed)
        except Exception as exc:
            return RelationResult(
                relation_id=relation.relation_id,
                status=RelationStatus.ERROR,
                reason=f"seed canonicalization failed: {type(exc).__name__}: {exc}",
                seed_case_hash="UNAVAILABLE",
                derived_case_hash=None,
                baseline_observation_hash=None,
                derived_observation_hash=None,
            )

        try:
            derived = relation.mutator(seed)
            if not isinstance(derived, Case):
                raise TypeError("relation mutator must return Case")
            derived_hash = self._safe_hash(derived)
        except Exception as exc:  # mutation errors are evidence, not process crashes
            return RelationResult(
                relation_id=relation.relation_id,
                status=RelationStatus.ERROR,
                reason=f"relation mutation failed: {type(exc).__name__}: {exc}",
                seed_case_hash=seed_hash,
                derived_case_hash=None,
                baseline_observation_hash=None,
                derived_observation_hash=None,
            )

        baseline, baseline_error = self._observe(seed)
        if baseline_error is not None:
            return RelationResult(
                relation_id=relation.relation_id,
                status=RelationStatus.ERROR,
                reason=baseline_error,
                seed_case_hash=seed_hash,
                derived_case_hash=derived_hash,
                baseline_observation_hash=None,
                derived_observation_hash=None,
            )

        derived_observation, derived_error = self._observe(derived)
        if derived_error is not None:
            return RelationResult(
                relation_id=relation.relation_id,
                status=RelationStatus.ERROR,
                reason=derived_error,
                seed_case_hash=seed_hash,
                derived_case_hash=derived_hash,
                baseline_observation_hash=self._safe_hash(baseline),
                derived_observation_hash=None,
            )

        assert baseline is not None and derived_observation is not None
        try:
            oracle = relation.oracle(baseline, derived_observation, seed, derived)
        except Exception as exc:
            return RelationResult(
                relation_id=relation.relation_id,
                status=RelationStatus.ERROR,
                reason=f"oracle execution failed: {type(exc).__name__}: {exc}",
                seed_case_hash=seed_hash,
                derived_case_hash=derived_hash,
                baseline_observation_hash=self._safe_hash(baseline),
                derived_observation_hash=self._safe_hash(derived_observation),
            )

        return RelationResult(
            relation_id=relation.relation_id,
            status=RelationStatus.PASS if oracle.passed else RelationStatus.FAIL,
            reason=oracle.reason,
            seed_case_hash=seed_hash,
            derived_case_hash=derived_hash,
            baseline_observation_hash=self._safe_hash(baseline),
            derived_observation_hash=self._safe_hash(derived_observation),
            details=oracle.details,
        )

    def run(self, seed: Case, relations: Iterable[MetamorphicRelation], *, run_id: str | None = None) -> VerificationReport:
        relation_list = tuple(relations)
        if not relation_list:
            raise ValueError("at least one metamorphic relation is required")
        seen: set[str] = set()
        duplicates: set[str] = set()
        for relation in relation_list:
            if relation.relation_id in seen:
                duplicates.add(relation.relation_id)
            seen.add(relation.relation_id)
        if duplicates:
            raise ValueError(f"duplicate relation ids: {sorted(duplicates)}")

        results = tuple(self.run_relation(seed, relation) for relation in relation_list)
        return VerificationReport(
            run_id=run_id or f"mvk-{uuid.uuid4().hex}",
            results=results,
            metadata={"relation_count": len(results)},
        )

    def _observe(self, case: Case) -> tuple[Observation | None, str | None]:
        try:
            observation = self.adapter(case)
            if not isinstance(observation, Observation):
                raise TypeError("adapter must return Observation")
            self._safe_hash(observation)
            return observation, None
        except Exception as exc:
            return None, f"adapter execution failed: {type(exc).__name__}: {exc}"

    @staticmethod
    def _safe_hash(value: object) -> str:
        try:
            return stable_hash(value)
        except CanonicalizationError:
            raise
