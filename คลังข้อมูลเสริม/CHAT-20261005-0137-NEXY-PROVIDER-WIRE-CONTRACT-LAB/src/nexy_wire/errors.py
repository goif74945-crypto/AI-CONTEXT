from __future__ import annotations


class WireContractError(ValueError):
    """Raised when a provider-boundary event violates the canonical wire contract."""

    def __init__(self, code: str, message: str, *, sequence: int | None = None) -> None:
        self.code = code
        self.sequence = sequence
        prefix = f"[{code}]"
        if sequence is not None:
            prefix += f" seq={sequence}"
        super().__init__(f"{prefix} {message}")
