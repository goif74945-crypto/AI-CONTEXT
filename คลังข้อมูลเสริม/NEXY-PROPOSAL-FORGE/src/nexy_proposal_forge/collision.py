from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Literal

from .canon import normalize_text
from .models import ProposalValidationError

WORK_STATUSES = {"PLANNED", "IN_PROGRESS", "VERIFYING", "COMPLETE", "BLOCKED"}
ACTIVE_STATUSES = {"PLANNED", "IN_PROGRESS", "VERIFYING"}


@dataclass(frozen=True, slots=True)
class Scope:
    path: str
    recursive: bool

    @classmethod
    def parse(cls, raw: str) -> "Scope":
        if not isinstance(raw, str) or not normalize_text(raw):
            raise ValueError("scope must be a non-empty string")
        text = normalize_text(raw).replace("\\", "/")
        recursive = text.endswith("/**")
        if recursive:
            text = text[:-3]
        text = text.strip("/")
        if not text:
            raise ValueError("scope root cannot be empty")
        parts = PurePosixPath(text).parts
        if any(part in {".", ".."} for part in parts):
            raise ValueError("scope cannot contain . or .. path segments")
        if any("*" in part or "?" in part or "[" in part or "]" in part for part in parts):
            raise ValueError("only a terminal /** recursive marker is supported")
        return cls(path="/".join(parts), recursive=recursive)

    def contains(self, other: "Scope") -> bool:
        if self.path == other.path:
            return self.recursive or not other.recursive
        if not self.recursive:
            return False
        return other.path.startswith(self.path + "/")

    def overlaps(self, other: "Scope") -> bool:
        return self.contains(other) or other.contains(self)

    def render(self) -> str:
        return self.path + ("/**" if self.recursive else "")


@dataclass(frozen=True, slots=True)
class WorkManifest:
    execution_id: str
    status: str
    target_repository: str
    objective: str
    write_scopes: tuple[Scope, ...]
    proposal_ids: tuple[str, ...]

    @classmethod
    def from_dict(cls, data: Any) -> "WorkManifest":
        keys = {"execution_id", "status", "target_repository", "objective", "write_scopes", "proposal_ids"}
        if not isinstance(data, dict):
            raise ProposalValidationError(["work manifest: required object"])
        errors: list[str] = []
        unknown = sorted(set(data) - keys)
        if unknown:
            errors.append(f"work manifest: unknown field(s): {', '.join(unknown)}")

        def text_field(key: str) -> str:
            value = data.get(key)
            if not isinstance(value, str) or not normalize_text(value):
                errors.append(f"{key}: required non-empty string")
                return ""
            return normalize_text(value)

        execution_id = text_field("execution_id")
        status = text_field("status")
        target_repository = text_field("target_repository")
        objective = text_field("objective")
        if status and status not in WORK_STATUSES:
            errors.append(f"status: must be one of {', '.join(sorted(WORK_STATUSES))}")

        write_scopes: list[Scope] = []
        raw_scopes = data.get("write_scopes")
        if not isinstance(raw_scopes, list) or not raw_scopes:
            errors.append("write_scopes: required non-empty list")
        else:
            for index, raw in enumerate(raw_scopes):
                try:
                    parsed = Scope.parse(raw)
                except (TypeError, ValueError) as exc:
                    errors.append(f"write_scopes[{index}]: {exc}")
                    continue
                if parsed not in write_scopes:
                    write_scopes.append(parsed)

        proposal_ids: list[str] = []
        raw_ids = data.get("proposal_ids")
        if not isinstance(raw_ids, list):
            errors.append("proposal_ids: required list")
        else:
            for index, raw in enumerate(raw_ids):
                if not isinstance(raw, str) or not normalize_text(raw):
                    errors.append(f"proposal_ids[{index}]: required non-empty string")
                    continue
                value = normalize_text(raw)
                if any(ch.isspace() for ch in value):
                    errors.append(f"proposal_ids[{index}]: whitespace is forbidden")
                    continue
                if value not in proposal_ids:
                    proposal_ids.append(value)

        if errors:
            raise ProposalValidationError(errors)
        return cls(
            execution_id=execution_id,
            status=status,
            target_repository=target_repository,
            objective=objective,
            write_scopes=tuple(write_scopes),
            proposal_ids=tuple(proposal_ids),
        )


@dataclass(frozen=True, slots=True)
class ScopeCollision:
    other_execution_id: str
    kind: Literal["WRITE_SCOPE", "PROPOSAL_ID"]
    left: str
    right: str

    def to_dict(self) -> dict[str, str]:
        return {
            "other_execution_id": self.other_execution_id,
            "kind": self.kind,
            "left": self.left,
            "right": self.right,
        }


@dataclass(frozen=True, slots=True)
class CollisionReport:
    execution_id: str
    recommendation: Literal["CLEAR", "COLLISION"]
    advisory_only: bool
    collisions: tuple[ScopeCollision, ...]
    ignored_inactive_manifests: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "execution_id": self.execution_id,
            "recommendation": self.recommendation,
            "advisory_only": self.advisory_only,
            "collisions": [item.to_dict() for item in self.collisions],
            "ignored_inactive_manifests": list(self.ignored_inactive_manifests),
        }


def compare_work_manifests(current: WorkManifest, others: tuple[WorkManifest, ...]) -> CollisionReport:
    collisions: list[ScopeCollision] = []
    ignored: list[str] = []
    current_repo = current.target_repository.casefold()

    for other in sorted(others, key=lambda item: item.execution_id):
        if other.execution_id == current.execution_id:
            continue
        if other.status not in ACTIVE_STATUSES:
            ignored.append(other.execution_id)
            continue
        if other.target_repository.casefold() != current_repo:
            continue

        for left in current.write_scopes:
            for right in other.write_scopes:
                if left.overlaps(right):
                    collisions.append(
                        ScopeCollision(
                            other_execution_id=other.execution_id,
                            kind="WRITE_SCOPE",
                            left=left.render(),
                            right=right.render(),
                        )
                    )

        for proposal_id in sorted(set(current.proposal_ids) & set(other.proposal_ids)):
            collisions.append(
                ScopeCollision(
                    other_execution_id=other.execution_id,
                    kind="PROPOSAL_ID",
                    left=proposal_id,
                    right=proposal_id,
                )
            )

    unique = {
        (item.other_execution_id, item.kind, item.left, item.right): item
        for item in collisions
    }
    ordered = tuple(unique[key] for key in sorted(unique))
    return CollisionReport(
        execution_id=current.execution_id,
        recommendation="COLLISION" if ordered else "CLEAR",
        advisory_only=True,
        collisions=ordered,
        ignored_inactive_manifests=tuple(sorted(ignored)),
    )
