from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


_SECRET_PATTERNS = (
    re.compile(r'(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*[^\s]+'),
    re.compile(r'\bsk-[A-Za-z0-9_-]{12,}\b'),
)


@dataclass(frozen=True)
class ExecutionRecord:
    record_id: str
    objective_pattern: str
    steps: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    evidence_class: int
    passed: bool
    environment: str


@dataclass(frozen=True)
class SkillManifest:
    status: str
    name: str | None
    objective_pattern: str | None
    steps: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    environments: tuple[str, ...]
    provenance_record_ids: tuple[str, ...]
    pass_ratio: float
    reason: str | None = None


def _contains_secret(texts: Iterable[str]) -> bool:
    joined = '\n'.join(texts)
    return any(p.search(joined) for p in _SECRET_PATTERNS)


def compile_skill(records: Iterable[ExecutionRecord], *, min_passes: int = 3, min_pass_ratio: float = 0.8, min_evidence_class: int = 2) -> SkillManifest:
    data = tuple(records)
    if not data:
        return SkillManifest('FREEZE', None, None, (), (), (), (), (), 0.0, 'no execution records')
    patterns = {r.objective_pattern for r in data}
    if len(patterns) != 1:
        return SkillManifest('FREEZE', None, None, (), (), (), (), (), 0.0, 'multiple objective patterns')
    if len({r.record_id for r in data}) != len(data):
        return SkillManifest('FREEZE', None, None, (), (), (), (), (), 0.0, 'duplicate record ids')
    pass_ratio = sum(1 for r in data if r.passed) / len(data)
    passed = [r for r in data if r.passed]
    if len(passed) < min_passes or pass_ratio < min_pass_ratio:
        return SkillManifest('FREEZE', None, None, (), (), (), (), (), round(pass_ratio, 6), 'insufficient successful evidence')
    if any(r.evidence_class < min_evidence_class for r in passed):
        return SkillManifest('FREEZE', None, None, (), (), (), (), (), round(pass_ratio, 6), 'evidence class below promotion threshold')
    all_texts = []
    for r in passed:
        all_texts.extend(r.steps)
        all_texts.extend(r.inputs)
        all_texts.extend(r.outputs)
    if _contains_secret(all_texts):
        return SkillManifest('FREEZE', None, None, (), (), (), (), (), round(pass_ratio, 6), 'secret-like literal detected')
    step_variants = {r.steps for r in passed}
    if len(step_variants) != 1:
        return SkillManifest('FREEZE', None, None, (), (), (), (), (), round(pass_ratio, 6), 'step sequence drift detected')
    objective = next(iter(patterns))
    canonical_steps = passed[0].steps
    inputs = tuple(sorted(set().union(*(set(r.inputs) for r in passed))))
    outputs = tuple(sorted(set().union(*(set(r.outputs) for r in passed))))
    environments = tuple(sorted({r.environment for r in passed}))
    provenance = tuple(sorted(r.record_id for r in passed))
    safe_name = re.sub(r'[^a-z0-9]+', '-', objective.lower()).strip('-') or 'compiled-skill'
    return SkillManifest('PASS', safe_name, objective, canonical_steps, inputs, outputs, environments, provenance, round(pass_ratio, 6))
