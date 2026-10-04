from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class SurfaceSpec:
    surface_id: str
    required: bool = True
    authoritative: bool = True
    max_age_seconds: int | None = None
    expected_version: str | None = None
    scan_cost: int = 1


@dataclass(frozen=True)
class Observation:
    surface_id: str
    target: str
    searched_at: int
    version: str | None
    hits: tuple[str, ...] = ()


@dataclass(frozen=True)
class AbsenceAssessment:
    status: str
    claim: str
    hit_surfaces: tuple[str, ...]
    missing_surfaces: tuple[str, ...]
    stale_surfaces: tuple[str, ...]
    version_mismatch_surfaces: tuple[str, ...]
    next_scan_plan: tuple[str, ...]


class AbsenceEvidencePlanner:
    """Prevents 'not found' from being upgraded to 'does not exist' without coverage proof."""

    @staticmethod
    def evaluate(
        target: str,
        surfaces: Iterable[SurfaceSpec],
        observations: Iterable[Observation],
        now: int,
    ) -> AbsenceAssessment:
        specs = tuple(surfaces)
        if not target:
            raise ValueError("target must be non-empty")
        if len({s.surface_id for s in specs}) != len(specs):
            raise ValueError("surface_id values must be unique")
        obs_map: Mapping[tuple[str, str], Observation] = {
            (o.surface_id, o.target): o for o in observations
        }

        required = [s for s in specs if s.required and s.authoritative]
        missing: list[str] = []
        stale: list[str] = []
        mismatch: list[str] = []
        hit_surfaces: list[str] = []
        unresolved_specs: list[SurfaceSpec] = []

        for spec in required:
            obs = obs_map.get((spec.surface_id, target))
            if obs is None:
                missing.append(spec.surface_id)
                unresolved_specs.append(spec)
                continue
            if spec.expected_version is not None and obs.version != spec.expected_version:
                mismatch.append(spec.surface_id)
                unresolved_specs.append(spec)
                continue
            if spec.max_age_seconds is not None and now - obs.searched_at > spec.max_age_seconds:
                stale.append(spec.surface_id)
                unresolved_specs.append(spec)
                continue
            if obs.hits:
                hit_surfaces.append(spec.surface_id)

        plan = tuple(s.surface_id for s in sorted(unresolved_specs, key=lambda s: (s.scan_cost, s.surface_id)))
        if hit_surfaces:
            status = "FAIL"
            claim = f"presence observed for {target!r}; absence claim refuted"
        elif missing or stale or mismatch:
            status = "NOT_VERIFIED"
            claim = f"absence of {target!r} is not proven"
        else:
            status = "PASS"
            claim = f"no hits for {target!r} across all required authoritative surfaces"

        return AbsenceAssessment(
            status=status,
            claim=claim,
            hit_surfaces=tuple(sorted(hit_surfaces)),
            missing_surfaces=tuple(sorted(missing)),
            stale_surfaces=tuple(sorted(stale)),
            version_mismatch_surfaces=tuple(sorted(mismatch)),
            next_scan_plan=plan,
        )
