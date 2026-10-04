from __future__ import annotations

from fractions import Fraction
import itertools
import unittest

from nnik.evaluator import evaluate
from nnik.rational import parse_rational
from nnik.units import BUILTIN_REGISTRY


def make_contract(lower_value, lower_inclusive, upper_value, upper_inclusive):
    return {
        "schema_version": "1",
        "name": "property-contract",
        "dimension": "length",
        "canonical_unit": "m",
        "lower": None if lower_value is None else {"value": str(lower_value), "inclusive": lower_inclusive},
        "upper": None if upper_value is None else {"value": str(upper_value), "inclusive": upper_inclusive},
        "normalization": {"quantum": None, "rounding_mode": None},
        "uncertainty_policy": "FREEZE_ON_BOUNDARY_OVERLAP",
    }


def independent_classify(center: Fraction, delta: Fraction, lower, upper):
    lo, hi = center - delta, center + delta
    inside = True
    if lower is not None:
        lv, li = lower
        inside &= lo > lv or (lo == lv and li)
    if upper is not None:
        uv, ui = upper
        inside &= hi < uv or (hi == uv and ui)
    if inside:
        return "ACCEPT"

    below = False
    if lower is not None:
        lv, li = lower
        below = hi < lv or (hi == lv and not li)
    above = False
    if upper is not None:
        uv, ui = upper
        above = lo > uv or (lo == uv and not ui)
    if below or above:
        return "REJECT"
    return "FREEZE"


class ExhaustiveDecisionProperties(unittest.TestCase):
    def test_small_grid_matches_independent_interval_oracle(self):
        values = [Fraction(n, 2) for n in range(-2, 7)]
        uncertainties = [Fraction(0), Fraction(1, 4), Fraction(1, 2)]
        bound_pairs = [
            (Fraction(0), True, Fraction(2), True),
            (Fraction(0), False, Fraction(2), True),
            (Fraction(0), True, Fraction(2), False),
            (None, True, Fraction(2), True),
            (Fraction(0), True, None, True),
        ]
        for center, delta, (lv, li, uv, ui) in itertools.product(values, uncertainties, bound_pairs):
            with self.subTest(center=center, delta=delta, lower=lv, upper=uv, li=li, ui=ui):
                contract = make_contract(lv, li, uv, ui)
                result = evaluate(
                    contract,
                    {"value": str(center), "unit": "m", "uncertainty_abs": str(delta)},
                )
                expected = independent_classify(
                    center,
                    delta,
                    None if lv is None else (lv, li),
                    None if uv is None else (uv, ui),
                )
                self.assertEqual(result["verdict"], expected)

    def test_semantically_equivalent_numeric_text_has_same_result_digest(self):
        contract_a = make_contract(Fraction(1), True, Fraction(2), True)
        contract_b = make_contract(Fraction(1), True, Fraction(2), True)
        contract_b["lower"]["value"] = "1.0"
        contract_b["upper"]["value"] = "4/2"
        result_a = evaluate(contract_a, {"value": "1.50", "unit": "m", "uncertainty_abs": "0.10"})
        result_b = evaluate(contract_b, {"value": "3/2", "unit": "m", "uncertainty_abs": "1/10"})
        self.assertNotEqual(result_a["input_digest"], result_b["input_digest"])
        self.assertEqual(result_a["result_digest"], result_b["result_digest"])

    def test_extreme_exponent_is_rejected_before_big_integer_expansion(self):
        result = evaluate(make_contract(Fraction(0), True, Fraction(2), True), {"value": "1e1000000", "unit": "m"})
        self.assertEqual(result["verdict"], "FREEZE")
        self.assertEqual(result["reason_code"], "NUMERIC_LIMIT_EXCEEDED")

    def test_non_string_field_name_freezes_in_api(self):
        c = make_contract(Fraction(0), True, Fraction(2), True)
        c[1] = "invalid-key"
        result = evaluate(c, {"value": "1", "unit": "m"})
        self.assertEqual(result["verdict"], "FREEZE")
        self.assertEqual(result["reason_code"], "NON_STRING_FIELD_NAME")

    def test_all_unit_definitions_are_roundtrip_exact_for_zero_and_one(self):
        record = BUILTIN_REGISTRY.to_record()
        by_dimension = {}
        for unit in record["units"]:
            by_dimension.setdefault(unit["dimension"], []).append(unit["symbol"])
        for symbols in by_dimension.values():
            for source in symbols:
                for target in symbols:
                    for value in (Fraction(0), Fraction(1)):
                        self.assertEqual(
                            BUILTIN_REGISTRY.convert(BUILTIN_REGISTRY.convert(value, source, target), target, source),
                            value,
                        )


class NumericSafetyLimits(unittest.TestCase):
    def test_oversized_integer_api_rejected(self):
        with self.assertRaisesRegex(Exception, "NUMERIC_LIMIT_EXCEEDED"):
            parse_rational(1 << 20000)

    def test_oversized_rational_text_rejected(self):
        with self.assertRaisesRegex(Exception, "NUMERIC_LIMIT_EXCEEDED"):
            parse_rational("9" * 600 + "/1")


if __name__ == "__main__":
    unittest.main()
