from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from math import gcd
from typing import Any

_FRAC_BITS = 64
_SCALE = 1 << _FRAC_BITS
_MIN_RAW = -(1 << 127)
_MAX_RAW = (1 << 127) - 1

class Q64Error(ValueError):
    pass

class Q64Overflow(OverflowError):
    pass


def _checked_raw(raw: int) -> int:
    if not isinstance(raw, int) or isinstance(raw, bool):
        raise TypeError("raw must be int")
    if raw < _MIN_RAW or raw > _MAX_RAW:
        raise Q64Overflow("signed Q64.64 raw overflow")
    return raw


def _trunc_div(n: int, d: int) -> int:
    if d == 0:
        raise ZeroDivisionError("Q64.64 division by zero")
    sign = -1 if (n < 0) ^ (d < 0) else 1
    q = abs(n) // abs(d)
    return -q if sign < 0 else q


@dataclass(frozen=True, order=True, slots=True)
class Q64:
    raw: int

    def __post_init__(self) -> None:
        _checked_raw(self.raw)

    @classmethod
    def zero(cls) -> "Q64":
        return cls(0)

    @classmethod
    def one(cls) -> "Q64":
        return cls(_SCALE)

    @classmethod
    def from_int(cls, value: int) -> "Q64":
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("value must be int")
        return cls(_checked_raw(value << _FRAC_BITS))

    @classmethod
    def from_ratio(cls, numerator: int, denominator: int) -> "Q64":
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("ratio terms must be int")
        return cls(_checked_raw(_trunc_div(numerator << _FRAC_BITS, denominator)))

    @classmethod
    def from_decimal(cls, text: str) -> "Q64":
        if not isinstance(text, str):
            raise TypeError("decimal input must be str; floats are forbidden")
        try:
            d = Decimal(text)
        except InvalidOperation as exc:
            raise Q64Error("invalid decimal") from exc
        if not d.is_finite():
            raise Q64Error("non-finite decimal forbidden")
        sign, digits, exponent = d.as_tuple()
        coeff = 0
        for digit in digits:
            coeff = coeff * 10 + digit
        if sign:
            coeff = -coeff
        if exponent >= 0:
            num = coeff * (10 ** exponent)
            den = 1
        else:
            num = coeff
            den = 10 ** (-exponent)
        return cls.from_ratio(num, den)

    @classmethod
    def coerce(cls, value: Any) -> "Q64":
        if isinstance(value, Q64):
            return value
        if isinstance(value, int) and not isinstance(value, bool):
            return cls.from_int(value)
        if isinstance(value, str):
            return cls.from_decimal(value)
        if isinstance(value, float):
            raise TypeError("float input is forbidden in Q64.64 decision paths")
        raise TypeError(f"unsupported Q64 value: {type(value).__name__}")

    def __add__(self, other: Any) -> "Q64":
        o = Q64.coerce(other)
        return Q64(_checked_raw(self.raw + o.raw))

    def __sub__(self, other: Any) -> "Q64":
        o = Q64.coerce(other)
        return Q64(_checked_raw(self.raw - o.raw))

    def __neg__(self) -> "Q64":
        if self.raw == _MIN_RAW:
            raise Q64Overflow("negation overflow")
        return Q64(-self.raw)

    def __mul__(self, other: Any) -> "Q64":
        o = Q64.coerce(other)
        return Q64(_checked_raw(_trunc_div(self.raw * o.raw, _SCALE)))

    def __truediv__(self, other: Any) -> "Q64":
        o = Q64.coerce(other)
        return Q64(_checked_raw(_trunc_div(self.raw << _FRAC_BITS, o.raw)))

    def abs(self) -> "Q64":
        return -self if self.raw < 0 else self

    def clamp(self, low: "Q64", high: "Q64") -> "Q64":
        if low.raw > high.raw:
            raise Q64Error("invalid clamp interval")
        return low if self.raw < low.raw else high if self.raw > high.raw else self

    def min(self, other: "Q64") -> "Q64":
        return self if self.raw <= other.raw else other

    def max(self, other: "Q64") -> "Q64":
        return self if self.raw >= other.raw else other

    def floor_int(self) -> int:
        return self.raw >> _FRAC_BITS

    def to_ratio(self) -> tuple[int, int]:
        g = gcd(abs(self.raw), _SCALE)
        return self.raw // g, _SCALE // g

    def canonical(self) -> str:
        n, d = self.to_ratio()
        return f"{n}/{d}"
