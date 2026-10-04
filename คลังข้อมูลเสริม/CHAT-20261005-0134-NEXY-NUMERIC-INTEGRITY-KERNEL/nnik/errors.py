from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class NumericIntegrityError(Exception):
    code: str
    message: str
    details: Mapping[str, Any] | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class ContractError(NumericIntegrityError):
    pass


class ObservationError(NumericIntegrityError):
    pass


class UnitError(NumericIntegrityError):
    pass
