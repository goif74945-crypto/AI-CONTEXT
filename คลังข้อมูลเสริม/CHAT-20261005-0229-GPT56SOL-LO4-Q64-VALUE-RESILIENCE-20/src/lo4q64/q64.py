from __future__ import annotations

from dataclasses import dataclass

FRACTION_BITS = 64
SCALE = 1 << FRACTION_BITS
MIN_RAW = -(1 << 127)
MAX_RAW = (1 << 127) - 1


class Q64Error(ValueError):
    """Base error for deterministic Q64.64 arithmetic."""


class Q64OverflowError(Q64Error, OverflowError):
    pass


class Q64DomainError(Q64Error):
    pass


def _check_raw(raw: int) -> int:
    if not isinstance(raw, int) or isinstance(raw, bool):
        raise TypeError("Q64 raw value must be an int")
    if raw < MIN_RAW or raw > MAX_RAW:
        raise Q64OverflowError(f"Q64.64 raw overflow: {raw}")
    return raw


def _trunc_div(num: int, den: int) -> int:
    if den == 0:
        raise ZeroDivisionError("Q64.64 division by zero")
    sign = -1 if (num < 0) ^ (den < 0) else 1
    return sign * (abs(num) // abs(den))


@dataclass(frozen=True, order=True, slots=True)
class Q64:
    """Signed, checked, deterministic Q64.64 fixed-point value.

    Representation is a signed 128-bit raw integer with 64 fractional bits.
    Operations truncate toward zero and reject overflow.
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
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("value must be int")
        return cls(_check_raw(value * SCALE))

    @classmethod
    def from_ratio(cls, numerator: int, denominator: int) -> "Q64":
        if not isinstance(numerator, int) or isinstance(numerator, bool):
            raise TypeError("numerator must be int")
        if not isinstance(denominator, int) or isinstance(denominator, bool):
            raise TypeError("denominator must be int")
        return cls(_check_raw(_trunc_div(numerator * SCALE, denominator)))

    @classmethod
    def from_basis_points(cls, bps: int) -> "Q64":
        return cls.from_ratio(bps, 10_000)

    def __add__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64(_check_raw(self.raw + other.raw))

    def __sub__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64(_check_raw(self.raw - other.raw))

    def __neg__(self) -> "Q64":
        return Q64(_check_raw(-self.raw))

    def __mul__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64(_check_raw(_trunc_div(self.raw * other.raw, SCALE)))

    def __truediv__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64(_check_raw(_trunc_div(self.raw * SCALE, other.raw)))

    def abs(self) -> "Q64":
        return -self if self.raw < 0 else self

    def clamp(self, lower: "Q64", upper: "Q64") -> "Q64":
        if lower.raw > upper.raw:
            raise Q64DomainError("lower bound exceeds upper bound")
        return lower if self.raw < lower.raw else upper if self.raw > upper.raw else self

    def complement01(self) -> "Q64":
        ensure_unit(self)
        return Q64.one() - self

    def to_decimal_string(self, digits: int = 12) -> str:
        if digits < 0 or digits > 30:
            raise ValueError("digits must be in [0, 30]")
        sign = "-" if self.raw < 0 else ""
        raw = abs(self.raw)
        whole, frac = divmod(raw, SCALE)
        if digits == 0:
            return f"{sign}{whole}"
        decimal = (frac * (10 ** digits)) // SCALE
        return f"{sign}{whole}.{decimal:0{digits}d}"


ZERO = Q64.zero()
ONE = Q64.one()
HALF = Q64.from_ratio(1, 2)


def ensure_unit(value: Q64) -> Q64:
    if value.raw < 0 or value.raw > SCALE:
        raise Q64DomainError(f"expected [0,1], got raw={value.raw}")
    return value


def ratio01(numerator: Q64, competitor: Q64) -> Q64:
    """Return numerator / (numerator + competitor), with 0/0 defined as 0."""
    ensure_unit(numerator)
    ensure_unit(competitor)
    total = numerator + competitor
    if total.raw == 0:
        return ZERO
    return numerator / total


def weighted_mean(pairs: tuple[tuple[Q64, int], ...]) -> Q64:
    if not pairs:
        raise Q64DomainError("weighted_mean requires values")
    total_weight = 0
    accum = ZERO
    for value, weight in pairs:
        ensure_unit(value)
        if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
            raise Q64DomainError("weights must be positive integers")
        accum = accum + (value * Q64.from_int(weight))
        total_weight += weight
    return ensure_unit(accum / Q64.from_int(total_weight))


def min_q(*values: Q64) -> Q64:
    if not values:
        raise Q64DomainError("min_q requires values")
    return min(values, key=lambda x: x.raw)


def max_q(*values: Q64) -> Q64:
    if not values:
        raise Q64DomainError("max_q requires values")
    return max(values, key=lambda x: x.raw)
