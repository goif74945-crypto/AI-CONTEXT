"""Exact signed Q64.64 arithmetic with an explicit signed-i128 raw domain.

The implementation intentionally uses Python integers as an intermediate wide type,
then enforces the exact i128 carrier range at every public construction/arithmetic
boundary.  No binary floating point is accepted or produced by authoritative code.
"""
from __future__ import annotations

from dataclasses import dataclass

RAW_MIN = -(1 << 127)
RAW_MAX = (1 << 127) - 1
SCALE = 1 << 64


class Q64Error(ArithmeticError):
    """Base error for deterministic Q64 failures."""


class Q64OverflowError(Q64Error):
    """Raised when an operation cannot be represented by signed-i128 Q64.64."""


class Q64DomainError(Q64Error):
    """Raised when an operation has an invalid mathematical domain."""


def _checked_raw(raw: int) -> int:
    if type(raw) is not int:
        raise TypeError("Q64 raw carrier must be int")
    if raw < RAW_MIN or raw > RAW_MAX:
        raise Q64OverflowError("Q64 raw overflow")
    return raw


def _trunc_div(numerator: int, denominator: int) -> int:
    if denominator == 0:
        raise Q64DomainError("Q64 division by zero")
    negative = (numerator < 0) ^ (denominator < 0)
    quotient = abs(numerator) // abs(denominator)
    return -quotient if negative else quotient


@dataclass(frozen=True, slots=True, order=True)
class Q64:
    raw: int

    def __post_init__(self) -> None:
        _checked_raw(self.raw)

    @staticmethod
    def zero() -> "Q64":
        return Q64(0)

    @staticmethod
    def one() -> "Q64":
        return Q64(SCALE)

    @staticmethod
    def from_raw(raw: int) -> "Q64":
        return Q64(_checked_raw(raw))

    @staticmethod
    def from_int(value: int) -> "Q64":
        if type(value) is not int:
            raise TypeError("Q64 integer input must be int")
        return Q64.from_raw(_checked_raw(value * SCALE))

    @staticmethod
    def from_ratio(numerator: int, denominator: int) -> "Q64":
        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("Q64 ratio inputs must be int")
        raw = _trunc_div(numerator * SCALE, denominator)
        return Q64.from_raw(raw)

    @staticmethod
    def min_value() -> "Q64":
        return Q64(RAW_MIN)

    @staticmethod
    def max_value() -> "Q64":
        return Q64(RAW_MAX)

    def __add__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64.from_raw(_checked_raw(self.raw + other.raw))

    def __sub__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64.from_raw(_checked_raw(self.raw - other.raw))

    def __neg__(self) -> "Q64":
        if self.raw == RAW_MIN:
            raise Q64OverflowError("Q64 negation overflow")
        return Q64.from_raw(-self.raw)

    def __mul__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        raw = _trunc_div(self.raw * other.raw, SCALE)
        return Q64.from_raw(_checked_raw(raw))

    def __truediv__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        raw = _trunc_div(self.raw * SCALE, other.raw)
        return Q64.from_raw(_checked_raw(raw))

    def abs(self) -> "Q64":
        return -self if self.raw < 0 else self

    def clamp(self, lower: "Q64", upper: "Q64") -> "Q64":
        if lower > upper:
            raise Q64DomainError("Q64 clamp lower > upper")
        if self < lower:
            return lower
        if self > upper:
            return upper
        return self

    def in_unit_interval(self) -> bool:
        return 0 <= self.raw <= SCALE

    def canonical(self) -> str:
        """Canonical raw representation suitable for hashing and adapters."""
        return str(self.raw)

    def decimal(self, digits: int = 8) -> str:
        if type(digits) is not int or digits < 0 or digits > 18:
            raise ValueError("digits must be integer in [0, 18]")
        negative = self.raw < 0
        magnitude = abs(self.raw)
        integer = magnitude // SCALE
        remainder = magnitude % SCALE
        if digits == 0:
            text = str(integer)
        else:
            factor = 10 ** digits
            frac = (remainder * factor) // SCALE
            text = f"{integer}.{frac:0{digits}d}"
        return f"-{text}" if negative and magnitude != 0 else text


def qmin(*values: Q64) -> Q64:
    if not values:
        raise Q64DomainError("qmin requires values")
    return min(values)


def qmax(*values: Q64) -> Q64:
    if not values:
        raise Q64DomainError("qmax requires values")
    return max(values)


def unit(value: Q64, label: str) -> Q64:
    if not value.in_unit_interval():
        raise Q64DomainError(f"{label} must be in [0,1]")
    return value


def weighted_mean(values: tuple[Q64, ...], weights: tuple[Q64, ...]) -> Q64:
    if not values or len(values) != len(weights):
        raise Q64DomainError("weighted_mean shape mismatch")
    total_weight = Q64.zero()
    numerator = Q64.zero()
    for value, weight in zip(values, weights, strict=True):
        if weight.raw < 0:
            raise Q64DomainError("negative weight")
        total_weight = total_weight + weight
        numerator = numerator + (value * weight)
    if total_weight.raw == 0:
        raise Q64DomainError("zero total weight")
    return numerator / total_weight
