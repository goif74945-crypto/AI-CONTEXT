from __future__ import annotations

from dataclasses import dataclass

from .canon import jaccard_basis_points, matching_text, ngram_units, word_units
from .models import Proposal


@dataclass(frozen=True, slots=True)
class OverlapResult:
    proposal_id: str
    score_bp: int
    title_bp: int
    problem_bp: int
    capability_bp: int
    surface_bp: int
    exact_title: bool

    def to_dict(self) -> dict[str, int | str | bool]:
        return {
            "proposal_id": self.proposal_id,
            "score_bp": self.score_bp,
            "title_bp": self.title_bp,
            "problem_bp": self.problem_bp,
            "capability_bp": self.capability_bp,
            "surface_bp": self.surface_bp,
            "exact_title": self.exact_title,
        }


def _field_score(left: str, right: str) -> int:
    words = jaccard_basis_points(word_units(left), word_units(right))
    grams = jaccard_basis_points(ngram_units(left), ngram_units(right))
    return (words * 40 + grams * 60) // 100


def _list_score(left: tuple[str, ...], right: tuple[str, ...]) -> int:
    left_text = "\n".join(left)
    right_text = "\n".join(right)
    return _field_score(left_text, right_text)


def compare_proposals(candidate: Proposal, existing: Proposal) -> OverlapResult:
    title_bp = _field_score(candidate.title, existing.title)
    problem_bp = _field_score(candidate.problem, existing.problem)
    capability_bp = _list_score(candidate.proposed_capabilities, existing.proposed_capabilities)
    surface_bp = _list_score(candidate.integration_surfaces, existing.integration_surfaces)
    exact_title = matching_text(candidate.title) == matching_text(existing.title)

    score_bp = (
        title_bp * 35
        + capability_bp * 35
        + problem_bp * 20
        + surface_bp * 10
    ) // 100
    if exact_title:
        score_bp = max(score_bp, 9_500)

    return OverlapResult(
        proposal_id=existing.proposal_id,
        score_bp=score_bp,
        title_bp=title_bp,
        problem_bp=problem_bp,
        capability_bp=capability_bp,
        surface_bp=surface_bp,
        exact_title=exact_title,
    )


def rank_overlaps(candidate: Proposal, catalog: tuple[Proposal, ...]) -> tuple[OverlapResult, ...]:
    results = [compare_proposals(candidate, existing) for existing in catalog]
    return tuple(sorted(results, key=lambda item: (-item.score_bp, item.proposal_id)))
