import itertools
import unittest

from nexy_lo4_frontier import AuthorityRule, DecisionCase, ForbiddenPrivilegeSet, Capability, analyze_capability_composition, simulate_authority_change


class DeterminismPropertyTests(unittest.TestCase):
    def test_cawt_permutations_stable(self):
        rules = [
            AuthorityRule("d", 10, "DENY", "delete", "*"),
            AuthorityRule("a", 5, "ALLOW", "read", "public/*"),
            AuthorityRule("r", 5, "DENY", "read", "private/*"),
        ]
        cases = [
            DecisionCase("1", "u", "read", "public/a"),
            DecisionCase("2", "u", "read", "private/a"),
            DecisionCase("3", "u", "delete", "public/a"),
        ]
        fingerprints = set()
        for rp in itertools.permutations(rules):
            for cp in itertools.permutations(cases):
                fingerprints.add(simulate_authority_change(rp, rules, cp).fingerprint)
        self.assertEqual(len(fingerprints), 1)

    def test_ccf_permutations_stable(self):
        caps = [
            Capability("a", frozenset({"start"}), frozenset({"x"}), "s"),
            Capability("b", frozenset({"start"}), frozenset({"y"}), "s"),
            Capability("c", frozenset({"x", "y"}), frozenset({"z"}), "s"),
        ]
        rules = [ForbiddenPrivilegeSet("bad", frozenset({"z"}))]
        outputs = set()
        for cp in itertools.permutations(caps):
            r = analyze_capability_composition(cp, ["start"], rules, allowed_scopes=frozenset({"s"}))
            outputs.add((r.fingerprint, r.witness_capabilities))
        self.assertEqual(len(outputs), 1)


if __name__ == "__main__":
    unittest.main()
