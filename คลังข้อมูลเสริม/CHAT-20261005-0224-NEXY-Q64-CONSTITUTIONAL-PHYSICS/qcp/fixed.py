from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, ClassVar


class Q64Error(ArithmeticError):
    pass


class Q64Overflow(Q64Error):
    pass


class Q64DomainError(Q64Error):
    pass


def _round_div_even(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    if numerator == 0:
        return 0
    sign = -1 if numerator < 0 else 1
    n = abs(numerator)
    q, r = divmod(n, denominator)
    twice = r * 2
    if twice > denominator or (twice == denominator and (q & 1)):
        q += 1
    return sign * q


@dataclass(frozen=True, order=True, slots=True)
class Q64:
    """Signed Q64.64 fixed-point value backed by a checked signed 128-bit raw integer.

    The raw value is value * 2^64. Multiplication/division use deterministic
    round-to-nearest, ties-to-even. Floats are intentionally rejected.
    """

    raw: int

    FRACTION_BITS: ClassVar[int] = 64
    SCALE: ClassVar[int] = 1 << FRACTION_BITS
    RAW_MIN: ClassVar[int] = -(1 << 127)
    RAW_MAX: ClassVar[int] = (1 << 127) - 1
    _DECIMAL_RE: ClassVar[re.Pattern[str]] = re.compile(r"^([+-]?)(\d+)(?:\.(\d*))?$")

    def __post_init__(self) -> None:
        if type(self.raw) is not int:
            raise TypeError("raw must be int")
        if self.raw < self.RAW_MIN or self.raw > self.RAW_MAX:
            raise Q64Overflow("Q64.64 raw value outside signed 128-bit range")

    @classmethod
    def from_raw(cls, raw: int) -> "Q64":
        return cls(raw)

    @classmethod
    def zero(cls) -> "Q64":
        return cls(0)

    @classmethod
    def one(cls) -> "Q64":
        return cls(cls.SCALE)

    @classmethod
    def from_int(cls, value: int) -> "Q64":
        if type(value) is not int:
            raise TypeError("Q64.from_int requires int")
        return cls._checked(value * cls.SCALE)

    @classmethod
    def from_ratio(cls, numerator: int, denominator: int) -> "Q64":
        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("ratio components must be ints")
        if denominator == 0:
            raise Q64DomainError("division by zero")
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        raw = _round_div_even(numerator * cls.SCALE, denominator)
        return cls._checked(raw)

    @classmethod
    def from_decimal(cls, text: str) -> "Q64":
        if not isinstance(text, str):
            raise TypeError("Q64.from_decimal requires a string")
        match = cls._DECIMAL_RE.fullmatch(text.strip())
        if not match:
            raise ValueError(f"invalid decimal literal: {text!r}")
        sign_token, whole_token, frac_token = match.groups()
        frac = frac_token or ""
        numerator = int(whole_token + frac) if frac else int(whole_token)
        denominator = 10 ** len(frac)
        if sign_token == "-":
            numerator = -numerator
        return cls.from_ratio(numerator, denominator)

    @classmethod
    def from_value(cls, value: Any) -> "Q64":
        if isinstance(value, Q64):
            return value
        if type(value) is int:
            return cls.from_int(value)
        if isinstance(value, str):
            return cls.from_decimal(value)
        raise TypeError("Q64 accepts only Q64, int, or decimal string; float is forbidden")

    @classmethod
    def _checked(cls, raw: int) -> "Q64":
        if raw < cls.RAW_MIN or raw > cls.RAW_MAX:
            raise Q64Overflow("Q64.64 overflow")
        return cls(raw)

    def __add__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return self._checked(self.raw + other.raw)

    def __sub__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return self._checked(self.raw - other.raw)

    def __mul__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        raw = _round_div_even(self.raw * other.raw, self.SCALE)
        return self._checked(raw)

    def __truediv__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        if other.raw == 0:
            raise Q64DomainError("division by zero")
        numerator = self.raw * self.SCALE
        denominator = other.raw
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        return self._checked(_round_div_even(numerator, denominator))

    def __neg__(self) -> "Q64":
        if self.raw == self.RAW_MIN:
            raise Q64Overflow("cannot negate minimum Q64.64 value")
        return Q64(-self.raw)

    def __abs__(self) -> "Q64":
        return -self if self.raw < 0 else self

    def min(self, other: "Q64") -> "Q64":
        return self if self <= other else other

    def max(self, other: "Q64") -> "Q64":
        return self if self >= other else other

    def to_decimal(self, digits: int = 18) -> str:
        if type(digits) is not int or digits < 0 or digits > 40:
            raise ValueError("digits must be an int in [0, 40]")
        scale10 = 10 ** digits
        scaled = _round_div_even(abs(self.raw) * scale10, self.SCALE)
        if digits == 0:
            body = str(scaled)
        else:
            whole, frac = divmod(scaled, scale10)
            body = f"{whole}.{frac:0{digits}d}"
        return f"-{body}" if self.raw < 0 and scaled != 0 else body

    def __str__(self) -> str:
        return self.to_decimal(18)
