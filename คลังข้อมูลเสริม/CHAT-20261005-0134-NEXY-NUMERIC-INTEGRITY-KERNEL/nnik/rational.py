from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import re
from typing import Any

from .errors import NumericIntegrityError

_DECIMAL_RE = re.compile(r"^[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?$")
_RATIONAL_RE = re.compile(r"^([+-]?\d+)/([+-]?\d+)$")
MAX_NUMERIC_TEXT_LENGTH = 1024
MAX_DECIMAL_DIGITS = 512
MAX_ABS_DECIMAL_EXPONENT = 2048
MAX_INTEGER_BITS = 16384


def _check_int_size(value: int, field: str) -> None:
    if value.bit_length() > MAX_INTEGER_BITS:
        raise NumericIntegrityError("NUMERIC_LIMIT_EXCEEDED", f"{field} integer magnitude exceeds safety limit")


def _fraction_checked(numerator: int, denominator: int, field: str) -> Fraction:
    _check_int_size(numerator, field)
    _check_int_size(denominator, field)
    if denominator == 0:
        raise NumericIntegrityError("ZERO_DENOMINATOR", f"{field} denominator must not be zero")
    return Fraction(numerator, denominator)


def _decimal_checked(value: Decimal, field: str) -> Fraction:
    if not value.is_finite():
        raise NumericIntegrityError("NON_FINITE_NUMERIC", f"{field} must be finite")
    tup = value.as_tuple()
    if len(tup.digits) > MAX_DECIMAL_DIGITS or abs(tup.exponent) > MAX_ABS_DECIMAL_EXPONENT:
        raise NumericIntegrityError("NUMERIC_LIMIT_EXCEEDED", f"{field} decimal exceeds safety limits")
    result = Fraction(value)
    _check_int_size(result.numerator, field)
    _check_int_size(result.denominator, field)
    return result


def parse_rational(value: Any, *, field: str = "value") -> Fraction:
    """Parse a finite exact number. Python float is intentionally forbidden."""
    if isinstance(value, bool):
        raise NumericIntegrityError("INVALID_NUMERIC", f"{field} must not be boolean")
    if isinstance(value, Fraction):
        _check_int_size(value.numerator, field)
        _check_int_size(value.denominator, field)
        return value
    if isinstance(value, int):
        _check_int_size(value, field)
        return Fraction(value, 1)
    if isinstance(value, Decimal):
        return _decimal_checked(value, field)
    if isinstance(value, float):
        raise NumericIntegrityError(
            "BINARY_FLOAT_FORBIDDEN",
            f"{field} must be supplied as int, Decimal, Fraction, or numeric string",
        )
    if not isinstance(value, str):
        raise NumericIntegrityError("INVALID_NUMERIC_TYPE", f"{field} has unsupported type {type(value).__name__}")
    if len(value) > MAX_NUMERIC_TEXT_LENGTH:
        raise NumericIntegrityError("NUMERIC_LIMIT_EXCEEDED", f"{field} numeric text exceeds safety limit")
    if value != value.strip() or not value:
        raise NumericIntegrityError("INVALID_NUMERIC_TEXT", f"{field} must not contain surrounding whitespace")
    match = _RATIONAL_RE.fullmatch(value)
    if match:
        numerator_text, denominator_text = match.groups()
        if len(numerator_text.lstrip("+-")) > MAX_DECIMAL_DIGITS or len(denominator_text.lstrip("+-")) > MAX_DECIMAL_DIGITS:
            raise NumericIntegrityError("NUMERIC_LIMIT_EXCEEDED", f"{field} rational exceeds safety limits")
        return _fraction_checked(int(numerator_text), int(denominator_text), field)
    if not _DECIMAL_RE.fullmatch(value):
        raise NumericIntegrityError("INVALID_NUMERIC_TEXT", f"{field} is not an exact decimal/rational literal")
    return _decimal_checked(Decimal(value), field)


def canonical_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _ceil(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def round_fraction_to_int(value: Fraction, mode: str) -> int:
    allowed = {"FLOOR", "CEILING", "TOWARD_ZERO", "AWAY_ZERO", "HALF_UP", "HALF_EVEN"}
    if mode not in allowed:
        raise NumericIntegrityError("INVALID_ROUNDING_MODE", f"unsupported rounding mode: {mode}")

    if mode == "FLOOR":
        return _floor(value)
    if mode == "CEILING":
        return _ceil(value)
    if mode == "TOWARD_ZERO":
        return _floor(value) if value >= 0 else _ceil(value)
    if mode == "AWAY_ZERO":
        return _ceil(value) if value >= 0 else _floor(value)

    sign = 1 if value >= 0 else -1
    absolute = abs(value)
    lower = _floor(absolute)
    remainder = absolute - lower
    half = Fraction(1, 2)
    if remainder < half:
        rounded = lower
    elif remainder > half:
        rounded = lower + 1
    elif mode == "HALF_UP":
        rounded = lower + 1
    else:  # HALF_EVEN
        rounded = lower if lower % 2 == 0 else lower + 1
    return sign * rounded


def quantize(value: Fraction, step: Fraction, mode: str) -> Fraction:
    if step <= 0:
        raise NumericIntegrityError("INVALID_QUANTUM", "quantization step must be > 0")
    units = value / step
    return Fraction(round_fraction_to_int(units, mode), 1) * step
