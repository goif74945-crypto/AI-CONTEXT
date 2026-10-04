from __future__ import annotations

from fractions import Fraction
from typing import Any

from .errors import NumericIntegrityError
from .rational import canonical_fraction, parse_rational

I128_MIN = -(1 << 127)
I128_MAX = (1 << 127) - 1


def project_fraction_to_i128(value: Fraction, quantum: Fraction) -> int:
    """Project an exact rational into signed-128 fixed-point integer units."""
    if quantum <= 0:
        raise NumericIntegrityError("INVALID_FIXED128_QUANTUM", "fixed128 quantum must be > 0")
    scaled = value / quantum
    if scaled.denominator != 1:
        raise NumericIntegrityError(
            "NOT_EXACTLY_REPRESENTABLE_FIXED128",
            "value is not an exact integer multiple of the fixed128 quantum",
            {"value": canonical_fraction(value), "quantum": canonical_fraction(quantum)},
        )
    integer = scaled.numerator
    if integer < I128_MIN or integer > I128_MAX:
        raise NumericIntegrityError(
            "FIXED128_OVERFLOW",
            "fixed-point integer lies outside signed 128-bit range",
            {"integer": str(integer)},
        )
    return integer


def restore_i128(integer: int, quantum: Fraction) -> Fraction:
    if isinstance(integer, bool) or not isinstance(integer, int):
        raise NumericIntegrityError("INVALID_FIXED128_INTEGER", "fixed128 payload must be an integer")
    if integer < I128_MIN or integer > I128_MAX:
        raise NumericIntegrityError("FIXED128_OVERFLOW", "integer lies outside signed 128-bit range")
    if quantum <= 0:
        raise NumericIntegrityError("INVALID_FIXED128_QUANTUM", "fixed128 quantum must be > 0")
    return Fraction(integer, 1) * quantum


def project_exact(value: Any, quantum: Any) -> dict[str, str | int]:
    parsed_value = parse_rational(value, field="value")
    parsed_quantum = parse_rational(quantum, field="quantum")
    integer = project_fraction_to_i128(parsed_value, parsed_quantum)
    restored = restore_i128(integer, parsed_quantum)
    assert restored == parsed_value
    return {
        "integer": integer,
        "quantum": canonical_fraction(parsed_quantum),
        "exact_value": canonical_fraction(restored),
        "encoding": "SIGNED_I128_FIXED_POINT",
    }
