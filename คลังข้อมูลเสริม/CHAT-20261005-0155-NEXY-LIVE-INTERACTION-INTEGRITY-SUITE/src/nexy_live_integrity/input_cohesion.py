from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .common import GateStatus, canonical_digest, require_digest, require_nonempty


@dataclass(frozen=True, slots=True)
class InputRequirement:
    resource_id: str
    kind: str
    required: bool = True
    expected_sha256: str | None = None
    allowed_trust: tuple[str, ...] = ("user", "project", "verified_external")

    def __post_init__(self) -> None:
        object.__setattr__(self, "resource_id", require_nonempty("resource_id", self.resource_id))
        object.__setattr__(self, "kind", require_nonempty("kind", self.kind).lower())
        if type(self.required) is not bool:
            raise TypeError("required must be boolean")
        if self.expected_sha256 is not None:
            object.__setattr__(self, "expected_sha256", require_digest("expected_sha256", self.expected_sha256))
        trust = tuple(require_nonempty("allowed_trust", x).lower() for x in self.allowed_trust)
        if not trust or len(set(trust)) != len(trust):
            raise ValueError("allowed_trust must contain unique values")
        object.__setattr__(self, "allowed_trust", trust)


@dataclass(frozen=True, slots=True)
class InputResource:
    resource_id: str
    kind: str
    sha256: str
    trust: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "resource_id", require_nonempty("resource_id", self.resource_id))
        object.__setattr__(self, "kind", require_nonempty("kind", self.kind).lower())
        object.__setattr__(self, "sha256", require_digest("sha256", self.sha256))
        object.__setattr__(self, "trust", require_nonempty("trust", self.trust).lower())


@dataclass(frozen=True, slots=True)
class CohesionResult:
    status: GateStatus
    code: str
    bound_resources: tuple[InputResource, ...]
    quarantined_resources: tuple[InputResource, ...]
    problems: tuple[str, ...]
    binding_fingerprint: str

    @property
    def allowed(self) -> bool:
        return self.status is GateStatus.PASS


class InputCohesionGate:
    """Binds a directive to an explicit, complete set of input resources.

    Extra resources are never silently consumed. They are quarantined from the
    bound set. Missing/ambiguous/tampered required resources freeze.
    """

    @staticmethod
    def evaluate(requirements: Sequence[InputRequirement], resources: Sequence[InputResource]) -> CohesionResult:
        requirement_ids = [r.resource_id for r in requirements]
        if len(set(requirement_ids)) != len(requirement_ids):
            return CohesionResult(GateStatus.FREEZE, "INPUT_DUPLICATE_REQUIREMENT", (), tuple(resources), ("duplicate_requirement_id",), canonical_digest(requirements))

        by_id: dict[str, list[InputResource]] = {}
        for resource in resources:
            by_id.setdefault(resource.resource_id, []).append(resource)

        problems: list[str] = []
        bound: list[InputResource] = []
        required_ids = set(requirement_ids)

        for req in requirements:
            candidates = by_id.get(req.resource_id, [])
            if not candidates:
                if req.required:
                    problems.append(f"missing:{req.resource_id}")
                continue
            if len(candidates) != 1:
                problems.append(f"ambiguous:{req.resource_id}")
                continue
            resource = candidates[0]
            if resource.kind != req.kind:
                problems.append(f"kind_mismatch:{req.resource_id}")
                continue
            if resource.trust not in req.allowed_trust:
                problems.append(f"trust_mismatch:{req.resource_id}")
                continue
            if req.expected_sha256 is not None and resource.sha256 != req.expected_sha256:
                problems.append(f"digest_mismatch:{req.resource_id}")
                continue
            bound.append(resource)

        quarantined = tuple(r for r in resources if r.resource_id not in required_ids)
        binding_fingerprint = canonical_digest({
            "requirements": requirements,
            "bound": tuple(sorted(bound, key=lambda r: r.resource_id)),
        })
        if problems:
            return CohesionResult(GateStatus.FREEZE, "INPUT_COHESION_FAILED", tuple(sorted(bound, key=lambda r: r.resource_id)), quarantined, tuple(sorted(problems)), binding_fingerprint)
        return CohesionResult(GateStatus.PASS, "INPUT_COHESION_VALID", tuple(sorted(bound, key=lambda r: r.resource_id)), quarantined, (), binding_fingerprint)
