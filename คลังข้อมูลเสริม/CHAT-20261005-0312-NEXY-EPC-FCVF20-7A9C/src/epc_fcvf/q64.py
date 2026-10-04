from __future__ import annotations

from dataclasses import dataclass


class Q64Error(ArithmeticError):
    """Fail-closed Q64.64 arithmetic error."""


I128_MIN = -(1 << 127)
I128_MAX = (1 << 127) - 1
SCALE = 1 << 64


def _check_raw(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise Q64Error("Q64_RAW_NOT_INT")
    if value < I128_MIN or value > I128_MAX:
        raise Q64Error("Q64_OVERFLOW")
    return value


def _signed_mag(value: int, negative: bool) -> int:
    if value < 0:
        raise Q64Error("Q64_NEGATIVE_MAGNITUDE")
    raw = -value if negative else value
    return _check_raw(raw)


@dataclass(frozen=True, order=True, slots=True)
class Q64:
    """Signed checked Q64.64 scalar backed by a conceptual i128 raw value.

    Operations truncate toward zero and never use binary floating point.
    """

    raw: int

    def __post_init__(self) -> None:
        _check_raw(self.raw)

    @classmethod
    def zero(cls) -> "Q64":
        return cls(0)

    @classmethod
    def one(cls) -> "Q64":
        return cls(SCALE)

    @classmethod
    def from_int(cls, value: int) -> "Q64":
        if isinstance(value, bool) or not isinstance(value, int):
            raise Q64Error("Q64_INT_REQUIRED")
        return cls(_check_raw(value << 64))

    @classmethod
    def from_ratio(cls, numerator: int, denominator: int) -> "Q64":
        if isinstance(numerator, bool) or isinstance(denominator, bool):
            raise Q64Error("Q64_RATIO_INT_REQUIRED")
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise Q64Error("Q64_RATIO_INT_REQUIRED")
        if denominator == 0:
            raise Q64Error("Q64_DIV_ZERO")
        negative = (numerator < 0) ^ (denominator < 0)
        magnitude = (abs(numerator) << 64) // abs(denominator)
        return cls(_signed_mag(magnitude, negative))

    def add(self, other: "Q64") -> "Q64":
        return Q64(_check_raw(self.raw + other.raw))

    def sub(self, other: "Q64") -> "Q64":
        return Q64(_check_raw(self.raw - other.raw))

    def neg(self) -> "Q64":
        if self.raw == I128_MIN:
            raise Q64Error("Q64_NEG_OVERFLOW")
        return Q64(-self.raw)

    def mul(self, other: "Q64") -> "Q64":
        negative = (self.raw < 0) ^ (other.raw < 0)
        magnitude = (abs(self.raw) * abs(other.raw)) >> 64
        return Q64(_signed_mag(magnitude, negative))

    def div(self, other: "Q64") -> "Q64":
        if other.raw == 0:
            raise Q64Error("Q64_DIV_ZERO")
        negative = (self.raw < 0) ^ (other.raw < 0)
        magnitude = (abs(self.raw) << 64) // abs(other.raw)
        return Q64(_signed_mag(magnitude, negative))

    def clamp_unit(self) -> "Q64":
        if self.raw < 0:
            return Q64.zero()
        if self.raw > SCALE:
            return Q64.one()
        return self

    def to_decimal_string(self, places: int = 8) -> str:
        if places < 0 or places > 18:
            raise Q64Error("Q64_BAD_DECIMAL_PLACES")
        negative = self.raw < 0
        mag = abs(self.raw)
        integer = mag >> 64
        frac = mag & (SCALE - 1)
        if places == 0:
            body = str(integer)
        else:
            digits = (frac * (10 ** places)) // SCALE
            body = f"{integer}.{digits:0{places}d}"
        return f"-{body}" if negative and mag else body
