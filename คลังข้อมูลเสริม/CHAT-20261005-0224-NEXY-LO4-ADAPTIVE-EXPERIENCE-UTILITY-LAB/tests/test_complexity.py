import unittest

from aeul.complexity import ChangeSurface, ComplexityWeights, assess_complexity
from aeul.q64 import Q64

q = Q64.from_decimal
W = ComplexityWeights(q("0.25"), q("0.25"), q("0.25"), q("0.25"))


def surface(i, touch="1", persistence="0.2", migration="0.2", contract="0.2", rollback="0.2"):
    return ChangeSurface(i, q(touch), q(persistence), q(migration), q(contract), q(rollback))


class ComplexityTests(unittest.TestCase):
    def test_low_complexity_passes(self):
        r = assess_complexity([surface("core", touch="0.5")], weights=W, max_total_tax=q("0.5"), max_surface_tax=q("0.5"))
        self.assertEqual(r.status, "PASS")
        intrinsic = (q("0.25") * q("0.2")) + (q("0.25") * q("0.2")) + (q("0.25") * q("0.2")) + (q("0.25") * q("0.2"))
        expected = (q("0.5") * intrinsic) / q("0.5")
        self.assertEqual(r.normalized_tax, expected)

    def test_total_tax_rejects_wide_change(self):
        items = [surface("a", persistence="1", migration="1", contract="1", rollback="1"), surface("b", persistence="1", migration="1", contract="1", rollback="1")]
        r = assess_complexity(items, weights=W, max_total_tax=q("1.5"), max_surface_tax=q("1.1"))
        self.assertEqual(r.status, "REJECT")
        self.assertEqual(r.reason, "TOTAL_COMPLEXITY_TAX_EXCEEDS_LIMIT")

    def test_single_surface_limit_rejects(self):
        r = assess_complexity([surface("a", persistence="1", migration="1", contract="1", rollback="1")], weights=W, max_total_tax=q("2"), max_surface_tax=q("0.9"))
        self.assertEqual(r.reason, "SINGLE_SURFACE_TAX_EXCEEDS_LIMIT")

    def test_duplicate_surface_freezes(self):
        r = assess_complexity([surface("a"), surface("a")], weights=W, max_total_tax=q("2"), max_surface_tax=q("1"))
        self.assertEqual(r.status, "FREEZE")

    def test_no_surface_has_zero_tax(self):
        r = assess_complexity([], weights=W, max_total_tax=q("0"), max_surface_tax=q("0"))
        self.assertEqual(r.status, "PASS")
        self.assertEqual(r.total_tax, Q64.zero())

    def test_order_deterministic(self):
        items = [surface("a", touch="0.5"), surface("b", touch="0.25")]
        a = assess_complexity(items, weights=W, max_total_tax=q("1"), max_surface_tax=q("1"))
        b = assess_complexity(reversed(items), weights=W, max_total_tax=q("1"), max_surface_tax=q("1"))
        self.assertEqual(a.fingerprint, b.fingerprint)
