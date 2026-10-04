"""Deterministic property/stress checks without third-party dependencies."""

import random

from nexy_vam.assumption_planner import Assumption, Experiment, plan_experiments
from nexy_vam.behavioral_canary import CanaryCase, record_baseline, verify_canaries
from nexy_vam.correlated_evidence import EvidenceItem, EvidenceRequirement, assess_evidence
from nexy_vam.counterexample import minimize_sequence


def main() -> None:
    random.seed(20261005)
    checks = 0

    for _ in range(250):
        n = random.randint(2, 20)
        universe = list(range(n))
        required = set(random.sample(universe, random.randint(1, min(4, n))))
        noisy = universe[:]
        random.shuffle(noisy)
        predicate = lambda seq, req=required: req.issubset(set(seq))
        result = minimize_sequence(noisy, predicate, max_evaluations=5000)
        assert predicate(result.minimized)
        for i in range(len(result.minimized)):
            candidate = result.minimized[:i] + result.minimized[i + 1 :]
            assert not predicate(candidate)
        checks += 1

    base = [
        EvidenceItem("a", "c", frozenset({"r1"}), 0.9),
        EvidenceItem("b", "c", frozenset({"r1", "r2"}), 0.8),
        EvidenceItem("c", "c", frozenset({"r3"}), 0.7),
        EvidenceItem("d", "c", frozenset({"r4"}), 0.6),
    ]
    expected = assess_evidence("c", base, EvidenceRequirement(3, 2.0))
    for _ in range(250):
        shuffled = base[:]
        random.shuffle(shuffled)
        assert assess_evidence("c", shuffled, EvidenceRequirement(3, 2.0)) == expected
        checks += 1

    assumptions = [
        Assumption("a", 1, 1),
        Assumption("b", 0.8, 0.6),
        Assumption("c", 0.5, 0.5),
    ]
    experiments = [
        Experiment("x", frozenset({"a"}), 1),
        Experiment("y", frozenset({"b", "c"}), 1.2),
        Experiment("z", frozenset({"c"}), 0.3),
    ]
    expected_plan = plan_experiments(assumptions, experiments, budget=2.0)
    for _ in range(500):
        aa = assumptions[:]
        ee = experiments[:]
        random.shuffle(aa)
        random.shuffle(ee)
        assert plan_experiments(aa, ee, budget=2.0) == expected_plan
        checks += 1

    cases = [CanaryCase("k", {})]
    baseline = record_baseline(cases, lambda _: {"a": 1, "b": 2})
    assert verify_canaries(cases, lambda _: {"b": 2, "a": 1}, baseline).status == "PASS"
    assert verify_canaries(cases, lambda _: {"b": 3, "a": 1}, baseline).status == "DRIFT"
    checks += 2

    print(f"STRESS_PASS: {checks} deterministic/property checks")


if __name__ == "__main__":
    main()
