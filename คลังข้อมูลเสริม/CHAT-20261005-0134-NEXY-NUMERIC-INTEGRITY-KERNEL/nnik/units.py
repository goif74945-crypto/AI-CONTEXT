from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from typing import Dict, Iterable

from .canonical import canonical_bytes
from .errors import UnitError
from .rational import canonical_fraction


@dataclass(frozen=True)
class UnitDefinition:
    symbol: str
    dimension: str
    scale_to_base: Fraction
    offset_to_base: Fraction = Fraction(0, 1)

    def to_record(self) -> dict[str, str]:
        return {
            "symbol": self.symbol,
            "dimension": self.dimension,
            "scale_to_base": canonical_fraction(self.scale_to_base),
            "offset_to_base": canonical_fraction(self.offset_to_base),
        }


class UnitRegistry:
    def __init__(self, units: Iterable[UnitDefinition]) -> None:
        table: Dict[str, UnitDefinition] = {}
        for unit in units:
            if unit.symbol in table:
                raise ValueError(f"duplicate unit symbol: {unit.symbol}")
            if unit.scale_to_base == 0:
                raise ValueError(f"unit scale must be non-zero: {unit.symbol}")
            table[unit.symbol] = unit
        self._units = table
        self._registry_digest = sha256(canonical_bytes(self.to_record())).hexdigest()

    @property
    def digest(self) -> str:
        return self._registry_digest

    def get(self, symbol: str) -> UnitDefinition:
        if not isinstance(symbol, str) or not symbol:
            raise UnitError("INVALID_UNIT", "unit symbol must be a non-empty string")
        try:
            return self._units[symbol]
        except KeyError as exc:
            raise UnitError("UNKNOWN_UNIT", f"unit is not registered: {symbol}", {"unit": symbol}) from exc

    def require_dimension(self, symbol: str, dimension: str) -> UnitDefinition:
        unit = self.get(symbol)
        if unit.dimension != dimension:
            raise UnitError(
                "DIMENSION_MISMATCH",
                f"unit {symbol} has dimension {unit.dimension}, expected {dimension}",
                {"unit": symbol, "actual_dimension": unit.dimension, "expected_dimension": dimension},
            )
        return unit

    def convert(self, value: Fraction, from_symbol: str, to_symbol: str) -> Fraction:
        source = self.get(from_symbol)
        target = self.get(to_symbol)
        if source.dimension != target.dimension:
            raise UnitError(
                "DIMENSION_MISMATCH",
                f"cannot convert {source.dimension} to {target.dimension}",
                {"from_unit": from_symbol, "to_unit": to_symbol},
            )
        base = value * source.scale_to_base + source.offset_to_base
        return (base - target.offset_to_base) / target.scale_to_base

    def convert_delta(self, delta: Fraction, from_symbol: str, to_symbol: str) -> Fraction:
        source = self.get(from_symbol)
        target = self.get(to_symbol)
        if source.dimension != target.dimension:
            raise UnitError(
                "DIMENSION_MISMATCH",
                f"cannot convert uncertainty {source.dimension} to {target.dimension}",
                {"from_unit": from_symbol, "to_unit": to_symbol},
            )
        return delta * source.scale_to_base / target.scale_to_base

    def to_record(self) -> dict[str, object]:
        return {
            "registry_version": "1",
            "units": [self._units[key].to_record() for key in sorted(self._units)],
        }


def F(numerator: int, denominator: int = 1) -> Fraction:
    return Fraction(numerator, denominator)


BUILTIN_REGISTRY = UnitRegistry(
    [
        UnitDefinition("1", "dimensionless", F(1)),
        UnitDefinition("%", "dimensionless", F(1, 100)),
        UnitDefinition("m", "length", F(1)),
        UnitDefinition("cm", "length", F(1, 100)),
        UnitDefinition("mm", "length", F(1, 1000)),
        UnitDefinition("km", "length", F(1000)),
        UnitDefinition("in", "length", F(127, 5000)),
        UnitDefinition("ft", "length", F(381, 1250)),
        UnitDefinition("s", "time", F(1)),
        UnitDefinition("ms", "time", F(1, 1000)),
        UnitDefinition("min", "time", F(60)),
        UnitDefinition("h", "time", F(3600)),
        UnitDefinition("kg", "mass", F(1)),
        UnitDefinition("g", "mass", F(1, 1000)),
        UnitDefinition("mg", "mass", F(1, 1_000_000)),
        UnitDefinition("lb", "mass", F(45_359_237, 100_000_000)),
        UnitDefinition("K", "temperature", F(1), F(0)),
        UnitDefinition("C", "temperature", F(1), F(5463, 20)),
        UnitDefinition("F", "temperature", F(5, 9), F(45_967, 180)),
        UnitDefinition("B", "data_size", F(1)),
        UnitDefinition("kB", "data_size", F(1000)),
        UnitDefinition("MB", "data_size", F(1_000_000)),
        UnitDefinition("KiB", "data_size", F(1024)),
        UnitDefinition("MiB", "data_size", F(1_048_576)),
        UnitDefinition("Hz", "frequency", F(1)),
        UnitDefinition("kHz", "frequency", F(1000)),
        UnitDefinition("MHz", "frequency", F(1_000_000)),
    ]
)
