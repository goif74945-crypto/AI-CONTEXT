from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FailureEpisode:
    episode_id: str
    subsystem: str
    error_type: str
    symptoms: tuple[str, ...]
    root_cause: str
    repair_steps: tuple[str, ...]
    verification_tests: tuple[str, ...]
    outcome: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class RecoveryRecipe:
    key: str
    subsystem: str
    error_type: str
    root_cause: str
    repair_steps: tuple[str, ...]
    verification_tests: tuple[str, ...]
    success_count: int
    failure_count: int
    confidence: float
    evidence_ids: tuple[str, ...]


def _key(e: FailureEpisode) -> str:
    return f'{e.subsystem.strip().lower()}::{e.error_type.strip().lower()}::{e.root_cause.strip().lower()}'


def distill_recipes(episodes: Iterable[FailureEpisode], min_successes: int = 2) -> tuple[RecoveryRecipe, ...]:
    if min_successes < 1:
        raise ValueError('min_successes must be >= 1')
    groups: dict[str, list[FailureEpisode]] = defaultdict(list)
    for episode in episodes:
        if not episode.episode_id:
            raise ValueError('episode_id is required')
        groups[_key(episode)].append(episode)

    recipes: list[RecoveryRecipe] = []
    for key in sorted(groups):
        group = groups[key]
        passes = [e for e in group if e.outcome == 'PASS' and e.evidence_ids]
        failures = [e for e in group if e.outcome != 'PASS']
        if len(passes) < min_successes:
            continue
        step_counts = Counter(e.repair_steps for e in passes if e.repair_steps)
        if not step_counts:
            continue
        stable_steps, stable_count = sorted(step_counts.items(), key=lambda x: (-x[1], x[0]))[0]
        if stable_count < min_successes:
            continue
        tests = tuple(sorted({t for e in passes for t in e.verification_tests}))
        evidence = tuple(sorted({ev for e in passes for ev in e.evidence_ids}))
        confidence = len(passes) / (len(passes) + len(failures) + 1.0)
        first = passes[0]
        recipes.append(RecoveryRecipe(
            key=key,
            subsystem=first.subsystem,
            error_type=first.error_type,
            root_cause=first.root_cause,
            repair_steps=stable_steps,
            verification_tests=tests,
            success_count=len(passes),
            failure_count=len(failures),
            confidence=round(confidence, 6),
            evidence_ids=evidence,
        ))
    return tuple(recipes)


def match_recipe(recipes: Iterable[RecoveryRecipe], subsystem: str, error_type: str, symptoms: Iterable[str] = ()) -> RecoveryRecipe | None:
    del symptoms  # reserved for future semantic match without pretending lexical overlap is stronger evidence.
    candidates = [r for r in recipes if r.subsystem.lower() == subsystem.lower() and r.error_type.lower() == error_type.lower()]
    if not candidates:
        return None
    return sorted(candidates, key=lambda r: (-r.confidence, -r.success_count, r.key))[0]
