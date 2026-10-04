from __future__ import annotations

from dataclasses import dataclass
import re

SCALE_BITS = 64
SCALE = 1 << SCALE_BITS
RAW_MIN = -(1 << 127)
RAW_MAX = (1 << 127) - 1
_DECIMAL_RE = re.compile(r"^[+-]?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$")


class Q64Error(ValueError):
    """Base deterministic fixed-point error."""


class Q64Overflow(Q64Error):
    """Raised when a signed 128-bit Q64.64 raw value would overflow."""


class Q64DivisionByZero(Q64Error):
    """Raised for deterministic division by zero."""


def _checked_raw(raw: int) -> int:
    if not isinstance(raw, int) or isinstance(raw, bool):
        raise TypeError("raw must be int")
    if raw < RAW_MIN or raw > RAW_MAX:
        raise Q64Overflow("Q64.64 signed 128-bit overflow")
    return raw


def _round_half_even_div(numerator: int, denominator: int) -> int:
    if denominator == 0:
        raise Q64DivisionByZero("division by zero")
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
    sign = -1 if numerator < 0 else 1
    n = abs(numerator)
    q, r = divmod(n, denominator)
    twice = r << 1
    if twice > denominator or (twice == denominator and (q & 1)):
        q += 1
    return sign * q


@dataclass(frozen=True, slots=True, order=True)
class Q64:
    """Signed Q64.64 fixed-point value stored as a checked signed 128-bit integer.

    All multiplication and division round to nearest, ties-to-even. Construction
    from decimal text is exact before the single Q64.64 rounding step.
    """

    raw: int

    def __post_init__(self) -> None:
        _checked_raw(self.raw)

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
        return cls(_checked_raw(value * SCALE))

    @classmethod
    def from_ratio(cls, numerator: int, denominator: int) -> "Q64":
        if not isinstance(numerator, int) or isinstance(numerator, bool):
            raise TypeError("numerator must be int")
        if not isinstance(denominator, int) or isinstance(denominator, bool):
            raise TypeError("denominator must be int")
        return cls(_checked_raw(_round_half_even_div(numerator * SCALE, denominator)))

    @classmethod
    def from_decimal(cls, text: str) -> "Q64":
        if not isinstance(text, str) or not _DECIMAL_RE.fullmatch(text):
            raise Q64Error("invalid canonical decimal text")
        sign = -1 if text.startswith("-") else 1
        body = text[1:] if text[:1] in "+-" else text
        if "." in body:
            whole, frac = body.split(".", 1)
            denominator = 10 ** len(frac)
            numerator = int(whole) * denominator + int(frac)
        else:
            numerator = int(body)
            denominator = 1
        return cls.from_ratio(sign * numerator, denominator)

    def __add__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64(_checked_raw(self.raw + other.raw))

    def __sub__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        return Q64(_checked_raw(self.raw - other.raw))

    def __neg__(self) -> "Q64":
        return Q64(_checked_raw(-self.raw))

    def __abs__(self) -> "Q64":
        if self.raw == RAW_MIN:
            raise Q64Overflow("absolute value overflow")
        return Q64(abs(self.raw))

    def __mul__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        raw = _round_half_even_div(self.raw * other.raw, SCALE)
        return Q64(_checked_raw(raw))

    def __truediv__(self, other: "Q64") -> "Q64":
        if not isinstance(other, Q64):
            return NotImplemented
        if other.raw == 0:
            raise Q64DivisionByZero("division by zero")
        raw = _round_half_even_div(self.raw * SCALE, other.raw)
        return Q64(_checked_raw(raw))

    def min(self, other: "Q64") -> "Q64":
        return self if self.raw <= other.raw else other

    def max(self, other: "Q64") -> "Q64":
        return self if self.raw >= other.raw else other

    def clamp(self, lower: "Q64", upper: "Q64") -> "Q64":
        if lower.raw > upper.raw:
            raise Q64Error("lower exceeds upper")
        return self.max(lower).min(upper)

    def is_unit_interval(self) -> bool:
        return 0 <= self.raw <= SCALE

    def to_ratio(self) -> tuple[int, int]:
        return self.raw, SCALE

    def canonical(self) -> dict[str, int | str]:
        return {"format": "Q64.64", "raw": self.raw}

    def __str__(self) -> str:
        sign = "-" if self.raw < 0 else ""
        raw = abs(self.raw)
        whole, frac_raw = divmod(raw, SCALE)
        if frac_raw == 0:
            return f"{sign}{whole}"
        # Exact finite decimal because denominator is 2^64. 5^64 / 10^64.
        frac_dec = frac_raw * (5 ** 64)
        frac_text = f"{frac_dec:064d}".rstrip("0")
        return f"{sign}{whole}.{frac_text}"
