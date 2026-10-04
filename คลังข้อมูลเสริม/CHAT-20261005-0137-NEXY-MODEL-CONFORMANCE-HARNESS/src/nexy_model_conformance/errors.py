class ConformanceError(Exception):
    """Base error for malformed harness inputs."""


class CanonicalizationError(ConformanceError):
    """Raised when a value cannot be represented canonically."""


class ContractError(ConformanceError):
    """Raised when a manifest/case/observation violates its local contract."""
