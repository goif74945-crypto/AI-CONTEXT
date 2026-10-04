from __future__ import annotations


class OutcomeFabricError(ValueError):
    """Base class for deterministic, user-correctable contract/input failures."""


class ContractValidationError(OutcomeFabricError):
    """Raised when a proposed outcome contract is malformed or ambiguous."""


class ObservationValidationError(OutcomeFabricError):
    """Raised when an observation payload cannot be evaluated safely."""


class RecoveryPlanningError(OutcomeFabricError):
    """Raised when a recovery planning request is structurally invalid."""
