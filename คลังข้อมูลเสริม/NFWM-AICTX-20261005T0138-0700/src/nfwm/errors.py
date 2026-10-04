class NFWMError(Exception):
    """Base exception for deterministic user-facing NFWM failures."""


class ValidationError(NFWMError):
    """Input does not satisfy the declared NFWM schema contract."""
