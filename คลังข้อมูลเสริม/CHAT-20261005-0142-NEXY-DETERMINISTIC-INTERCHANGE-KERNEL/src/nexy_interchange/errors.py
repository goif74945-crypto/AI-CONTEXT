from __future__ import annotations


class InterchangeError(ValueError):
    """Base error for deterministic interchange validation failures."""

    code = "INTERCHANGE_ERROR"

    def __init__(self, message: str, *, path: str = "$") -> None:
        super().__init__(message)
        self.path = path

    def __str__(self) -> str:
        return f"{self.code} at {self.path}: {super().__str__()}"


class UnsupportedTypeError(InterchangeError):
    code = "UNSUPPORTED_TYPE"


class NonStringKeyError(InterchangeError):
    code = "NON_STRING_KEY"


class DuplicateKeyError(InterchangeError):
    code = "DUPLICATE_KEY"


class NormalizationCollisionError(InterchangeError):
    code = "NORMALIZATION_COLLISION"


class UnsafeIntegerError(InterchangeError):
    code = "UNSAFE_INTEGER"


class InvalidUnicodeError(InterchangeError):
    code = "INVALID_UNICODE"


class ResourceLimitError(InterchangeError):
    code = "RESOURCE_LIMIT"


class CycleError(InterchangeError):
    code = "CYCLE"


class InvalidJsonError(InterchangeError):
    code = "INVALID_JSON"


class EnvelopeVerificationError(InterchangeError):
    code = "ENVELOPE_VERIFICATION_FAILED"
