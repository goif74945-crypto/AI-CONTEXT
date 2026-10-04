from __future__ import annotations

from dataclasses import dataclass

FRACTION_BITS = 64
SCALE = 1 << FRACTION_BITS
MIN_RAW = -(1 << 127)
MAX_RAW = (1 << 127) - 1


def _check_raw(raw: int) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise TypeError("Q64.64 raw value must be an int")
    if raw < MIN_RAW or raw > MAX_RAW:
        raise OverflowError("Q64.64 overflow")
    return raw


def _trunc_div(numerator: int, denominator: int) -> int:
    if denominator == 0:
        raise ZeroDivisionError("division by zero")
    sign = -1 if (numerator < 0) ^ (denominator < 0) else 1
    quotient = abs(numerator) // abs(denominator)
    return quotient if sign > 0 else -quotient


@dataclass(frozen=True, order=True)
class Q64:
    """Signed Q64.64 value stored as a checked signed 128-bit raw integer.

    Division and decimal parsing round toward zero. Python integers are used only
    as an implementation vehicle; every persisted Q64 raw value is range-checked
    to the signed 128-bit envelope.
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
            raise TypeError("integer required")
        return cls(_check_raw(value * SCALE))

    @classmethod
    def from_ratio(cls, numerator: int, denominator: int) -> "Q64":
        if isinstance(numerator, bool) or isinstance(denominator, bool):
            raise TypeError("ratio operands must be ints")
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("ratio operands must be ints")
        return cls(_check_raw(_trunc_div(numerator * SCALE, denominator)))

    @classmethod
    def parse(cls, text: str) -> "Q64":
        if not isinstance(text, str):
            raise TypeError("decimal text required")
        token = text.strip()
        if not token:
            raise ValueError("empty decimal")
        sign = 1
        if token[0] in "+-":
            if token[0] == "-":
                sign = -1
            token = token[1:]
        if not token or token == "." or token.count(".") > 1:
            raise ValueError("invalid decimal")
        whole_text, dot, frac_text = token.partition(".")
        if whole_text == "":
            whole_text = "0"
        if not whole_text.isdigit() or (dot and frac_text and not frac_text.isdigit()):
            raise ValueError("invalid decimal")
        if dot and frac_text == "":
            frac_text = "0"
        denominator = 10 ** len(frac_text) if frac_text else 1
        numerator = int(whole_text) * denominator + (int(frac_text) if frac_text else 0)
        return cls.from_ratio(sign * numerator, denominator)

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

    def min(self, other: "Q64") -> "Q64":
        return self if self <= other else other

    def max(self, other: "Q64") -> "Q64":
        return self if self >= other else other

    def clamp(self, lower: "Q64", upper: "Q64") -> "Q64":
        if lower > upper:
            raise ValueError("lower bound exceeds upper bound")
        return self.max(lower).min(upper)

    def ceil_ratio_positive(self, positive_denominator: "Q64") -> int:
        if self.raw < 0 or positive_denominator.raw <= 0:
            raise ValueError("ceil_ratio_positive requires nonnegative numerator and positive denominator")
        return (self.raw + positive_denominator.raw - 1) // positive_denominator.raw

    def to_decimal(self, fractional_digits: int = 18) -> str:
        if isinstance(fractional_digits, bool) or not isinstance(fractional_digits, int):
            raise TypeError("fractional_digits must be int")
        if fractional_digits < 0 or fractional_digits > 40:
            raise ValueError("fractional_digits out of range")
        sign = "-" if self.raw < 0 else ""
        raw = abs(self.raw)
        whole = raw // SCALE
        rem = raw % SCALE
        if fractional_digits == 0:
            return f"{sign}{whole}"
        scale10 = 10 ** fractional_digits
        frac = (rem * scale10) // SCALE
        return f"{sign}{whole}.{frac:0{fractional_digits}d}"

    def as_raw_decimal(self) -> dict[str, int | str]:
        return {"raw": self.raw, "decimal": self.to_decimal()}
