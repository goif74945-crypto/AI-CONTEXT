from __future__ import annotations


class CapsuleError(ValueError):
    """Base error for invalid decision capsules."""


class CanonicalizationError(CapsuleError):
    """Raised when data cannot be represented canonically."""


class IntegrityError(CapsuleError):
    """Raised when a hash, chain, or identity check fails."""


class ReplayError(CapsuleError):
    """Raised when an event sequence violates replay semantics."""


class SchemaError(CapsuleError):
    """Raised when required structure or values are invalid."""
