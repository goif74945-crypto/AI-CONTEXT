from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    field: str
    message: str


class ExperimentValidationError(ValueError):
    """Raised when a proposal cannot safely be compiled."""

    def __init__(self, issues: list[ValidationIssue]):
        if not issues:
            raise ValueError("ExperimentValidationError requires at least one issue")
        self.issues = tuple(issues)
        super().__init__("; ".join(f"{i.code}:{i.field}:{i.message}" for i in issues))
