from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import unittest

from nnik.canonical import canonical_dumps, digest
from nnik.evaluator import evaluate
from nnik.rational import parse_rational, quantize, round_fraction_to_int
from nnik.units import BUILTIN_REGISTRY

ROOT = Path(__file__).resolve().parents[1]


def contract(**overrides):
    base = {
        "schema_version": "1",
        "name": "length-window",
        "dimension": "length",
        "canonical_unit": "m",
        "lower": {"value": "1", "inclusive": True},
        "upper": {"value": "2", "inclusive": True},
        "normalization": {"quantum": None, "rounding_mode": None},
        "uncertainty_policy": "FREEZE_ON_BOUNDARY_OVERLAP",
    }
    base.update(overrides)
    return base


class RationalTests(unittest.TestCase):
    def test_exact_decimal(self):
        self.assertEqual(parse_rational("0.1"), Fraction(1, 10))
        self.assertEqual(parse_rational(Decimal("1.25")), Fraction(5, 4))

    def test_float_forbidden(self):
        with self.assertRaisesRegex(Exception, "BINARY_FLOAT_FORBIDDEN"):
            parse_rational(0.1)

    def test_rational_literal(self):
        self.assertEqual(parse_rational("-10/20"), Fraction(-1, 2))

    def test_rounding_modes(self):
        self.assertEqual(round_fraction_to_int(Fraction(5, 2), "HALF_EVEN"), 2)
        self.assertEqual(round_fraction_to_int(Fraction(7, 2), "HALF_EVEN"), 4)
        self.assertEqual(round_fraction_to_int(Fraction(-5, 2), "HALF_UP"), -3)
        self.assertEqual(round_fraction_to_int(Fraction(-11, 10), "TOWARD_ZERO"), -1)
        self.assertEqual(round_fraction_to_int(Fraction(-11, 10), "AWAY_ZERO"), -2)

    def test_quantize_exact(self):
        self.assertEqual(quantize(Fraction(1234, 1000), Fraction(1, 100), "HALF_EVEN"), Fraction(123, 100))


class UnitRegistryTests(unittest.TestCase):
    def test_cm_to_m_exact(self):
        self.assertEqual(BUILTIN_REGISTRY.convert(Fraction(100), "cm", "m"), Fraction(1))

    def test_fahrenheit_to_celsius_exact(self):
        self.assertEqual(BUILTIN_REGISTRY.convert(Fraction(32), "F", "C"), Fraction(0))
        self.assertEqual(BUILTIN_REGISTRY.convert(Fraction(212), "F", "C"), Fraction(100))

    def test_temperature_delta_ignores_offset(self):
        self.assertEqual(BUILTIN_REGISTRY.convert_delta(Fraction(9), "F", "C"), Fraction(5))

    def test_all_pair_round_trips(self):
        record = BUILTIN_REGISTRY.to_record()
        dimensions = {}
        for item in record["units"]:
            dimensions.setdefault(item["dimension"], []).append(item["symbol"])
        probes = [Fraction(-7, 3), Fraction(0), Fraction(1, 10), Fraction(12345, 67)]
        for symbols in dimensions.values():
            for source in symbols:
                for target in symbols:
                    for value in probes:
                        converted = BUILTIN_REGISTRY.convert(value, source, target)
                        restored = BUILTIN_REGISTRY.convert(converted, target, source)
                        self.assertEqual(restored, value, (source, target, value))

    def test_cross_dimension_rejected(self):
        result = evaluate(contract(), {"value": "1", "unit": "s"})
        self.assertEqual(result["verdict"], "FREEZE")
        self.assertEqual(result["reason_code"], "DIMENSION_MISMATCH")

    def test_unknown_unit_rejected(self):
        result = evaluate(contract(), {"value": "1", "unit": "meter"})
        self.assertEqual(result["verdict"], "FREEZE")
        self.assertEqual(result["reason_code"], "UNKNOWN_UNIT")


class EvaluationTests(unittest.TestCase):
    def test_accept_exact_conversion(self):
        result = evaluate(contract(), {"value": "150", "unit": "cm"})
        self.assertEqual(result["verdict"], "ACCEPT")
        self.assertEqual(result["observation"]["canonical_value"], "3/2")

    def test_reject_below(self):
        result = evaluate(contract(), {"value": "99", "unit": "cm"})
        self.assertEqual((result["verdict"], result["reason_code"]), ("REJECT", "BELOW_LOWER_BOUND"))

    def test_reject_above(self):
        result = evaluate(contract(), {"value": "2.01", "unit": "m"})
        self.assertEqual((result["verdict"], result["reason_code"]), ("REJECT", "ABOVE_UPPER_BOUND"))

    def test_exclusive_boundary_rejected(self):
        c = contract(lower={"value": "1", "inclusive": False})
        result = evaluate(c, {"value": "1", "unit": "m"})
        self.assertEqual(result["verdict"], "REJECT")

    def test_uncertainty_fully_inside_accepts(self):
        result = evaluate(contract(), {"value": "1.5", "unit": "m", "uncertainty_abs": "0.1"})
        self.assertEqual(result["verdict"], "ACCEPT")

    def test_uncertainty_fully_outside_rejects(self):
        result = evaluate(contract(), {"value": "0.5", "unit": "m", "uncertainty_abs": "0.1"})
        self.assertEqual(result["verdict"], "REJECT")

    def test_uncertainty_boundary_overlap_freezes(self):
        result = evaluate(contract(), {"value": "1.05", "unit": "m", "uncertainty_abs": "0.1"})
        self.assertEqual((result["verdict"], result["reason_code"]), ("FREEZE", "BOUNDARY_OVERLAP"))

    def test_uncertainty_conversion(self):
        result = evaluate(contract(), {"value": "150", "unit": "cm", "uncertainty_abs": "5"})
        self.assertEqual(result["observation"]["uncertainty_abs"], "1/20")

    def test_quantization_policy(self):
        c = contract(normalization={"quantum": "0.1", "rounding_mode": "HALF_EVEN"})
        result = evaluate(c, {"value": "1.25", "unit": "m"})
        self.assertEqual(result["observation"]["canonical_value"], "6/5")

    def test_negative_uncertainty_freezes(self):
        result = evaluate(contract(), {"value": "1.5", "unit": "m", "uncertainty_abs": "-0.1"})
        self.assertEqual(result["reason_code"], "NEGATIVE_UNCERTAINTY")
        self.assertEqual(result["verdict"], "FREEZE")

    def test_unbounded_contract_freezes(self):
        c = contract(lower=None, upper=None)
        result = evaluate(c, {"value": "1", "unit": "m"})
        self.assertEqual(result["reason_code"], "UNBOUNDED_CONTRACT")

    def test_empty_acceptance_set_freezes(self):
        c = contract(lower={"value": "1", "inclusive": True}, upper={"value": "1", "inclusive": False})
        result = evaluate(c, {"value": "1", "unit": "m"})
        self.assertEqual(result["reason_code"], "EMPTY_ACCEPTANCE_SET")

    def test_float_api_freezes(self):
        result = evaluate(contract(), {"value": 1.5, "unit": "m"})
        self.assertEqual(result["reason_code"], "BINARY_FLOAT_FORBIDDEN")

    def test_extra_fields_freeze(self):
        result = evaluate(contract(debug=True), {"value": "1.5", "unit": "m"})
        self.assertEqual(result["reason_code"], "UNKNOWN_CONTRACT_FIELD")

    def test_input_key_order_determinism(self):
        c1 = contract()
        c2 = dict(reversed(list(c1.items())))
        o1 = {"value": "150", "unit": "cm", "uncertainty_abs": "5"}
        o2 = {"uncertainty_abs": "5", "unit": "cm", "value": "150"}
        r1 = evaluate(c1, o1)
        r2 = evaluate(c2, o2)
        self.assertEqual(r1, r2)
        self.assertEqual(canonical_dumps(r1), canonical_dumps(r2))

    def test_digest_sensitive_to_semantics(self):
        r1 = evaluate(contract(), {"value": "1.5", "unit": "m"})
        r2 = evaluate(contract(upper={"value": "1.4", "inclusive": True}), {"value": "1.5", "unit": "m"})
        self.assertNotEqual(r1["result_digest"], r2["result_digest"])

    def test_registry_digest_stable(self):
        self.assertEqual(BUILTIN_REGISTRY.digest, digest(BUILTIN_REGISTRY.to_record()))


class CLITests(unittest.TestCase):
    def test_cli_evaluate_fixture(self):
        proc = subprocess.run(
            [sys.executable, "-m", "nnik.cli", "evaluate", str(ROOT / "fixtures" / "length_accept.json")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["verdict"], "ACCEPT")

    def test_cli_json_number_tokens_are_exact(self):
        proc = subprocess.run(
            [sys.executable, "-m", "nnik.cli", "evaluate", str(ROOT / "fixtures" / "json_number_token.json")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["verdict"], "ACCEPT")
        self.assertEqual(data["observation"]["canonical_value"], "3/2")
        self.assertEqual(data["observation"]["uncertainty_abs"], "1/10")

    def test_cli_rejects_oversized_file_before_json_parse(self):
        oversized = ROOT / "evidence" / "oversized_input.tmp.json"
        oversized.write_text(" " * 1_048_577, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "nnik.cli", "evaluate", str(oversized)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn("exceeds", proc.stderr)
        finally:
            oversized.unlink(missing_ok=True)

    def test_cli_domain_freeze_is_successful_process(self):
        proc = subprocess.run(
            [sys.executable, "-m", "nnik.cli", "evaluate", str(ROOT / "fixtures" / "length_dimension_mismatch.json")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["verdict"], "FREEZE")
        self.assertEqual(data["reason_code"], "DIMENSION_MISMATCH")


if __name__ == "__main__":
    unittest.main()
