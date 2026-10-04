from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Union

SCALE = 1 << 64
MIN_RAW = -(1 << 127)
MAX_RAW = (1 << 127) - 1

def _round_div_ties_even(numerator: int, denominator: int) -> int:
    if denominator == 0:
        raise ZeroDivisionError("division by zero")
    sign = -1 if (numerator < 0) ^ (denominator < 0) else 1
    n, d = abs(numerator), abs(denominator)
    qv, r = divmod(n, d)
    twice = r << 1
    if twice > d or (twice == d and (qv & 1)):
        qv += 1
    return sign * qv

@dataclass(frozen=True, order=True)
class Q64:
    raw: int
    def __post_init__(self) -> None:
        if not isinstance(self.raw, int):
            raise TypeError("raw must be int")
        if self.raw < MIN_RAW or self.raw > MAX_RAW:
            raise OverflowError("Q64.64 raw value exceeds signed 128-bit range")
    @classmethod
    def from_raw(cls, raw: int) -> "Q64": return cls(raw)
    @classmethod
    def zero(cls) -> "Q64": return cls(0)
    @classmethod
    def one(cls) -> "Q64": return cls(SCALE)
    @classmethod
    def from_int(cls, value: int) -> "Q64":
        if not isinstance(value, int): raise TypeError("value must be int")
        return cls(value * SCALE)
    @classmethod
    def from_ratio(cls, numerator: int, denominator: int) -> "Q64":
        return cls(_round_div_ties_even(numerator * SCALE, denominator))
    @classmethod
    def from_decimal(cls, text: str) -> "Q64":
        frac = Fraction(text); return cls.from_ratio(frac.numerator, frac.denominator)
    def __add__(self, other: "Q64") -> "Q64": return Q64(self.raw + other.raw)
    def __sub__(self, other: "Q64") -> "Q64": return Q64(self.raw - other.raw)
    def __neg__(self) -> "Q64": return Q64(-self.raw)
    def __mul__(self, other: "Q64") -> "Q64": return Q64(_round_div_ties_even(self.raw * other.raw, SCALE))
    def __truediv__(self, other: "Q64") -> "Q64":
        if other.raw == 0: raise ZeroDivisionError("Q64.64 division by zero")
        return Q64(_round_div_ties_even(self.raw * SCALE, other.raw))
    def __abs__(self) -> "Q64": return self if self.raw >= 0 else -self
    def min(self, other: "Q64") -> "Q64": return self if self <= other else other
    def max(self, other: "Q64") -> "Q64": return self if self >= other else other
    def clamp(self, lower: "Q64", upper: "Q64") -> "Q64":
        if lower > upper: raise ValueError("lower > upper")
        return self.max(lower).min(upper)
    def to_fraction(self) -> Fraction: return Fraction(self.raw, SCALE)

Q64Like = Union[Q64, int, str]
def q(value: Q64Like) -> Q64:
    if isinstance(value, Q64): return value
    if isinstance(value, int): return Q64.from_int(value)
    if isinstance(value, str): return Q64.from_decimal(value)
    raise TypeError(f"unsupported Q64 input: {type(value)!r}")
def require_non_negative(value: Q64, name: str) -> None:
    if value.raw < 0: raise ValueError(f"{name} must be non-negative")
def require_unit_interval(value: Q64, name: str) -> None:
    if value < Q64.zero() or value > Q64.one(): raise ValueError(f"{name} must be in [0,1]")
