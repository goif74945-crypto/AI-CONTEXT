from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str, rel: str):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ick = load("ick_deep", "01-invariant-conservation-kernel/src/ick.py")
mfwr = load("mfwr_deep", "02-minimal-failure-witness-reducer/src/mfwr.py")
esc = load("esc_deep", "03-epistemic-saturation-controller/src/esc.py")
eecp = load("eecp_deep", "04-exact-evidence-cut-planner/src/eecp.py")
uis = load("uis_deep", "05-unknown-impact-slicer/src/uis.py")


def validate_ick() -> int:
    cases = 0
    for before_auth, after_auth, before_ev, after_ev in itertools.product(range(2), repeat=4):
        for before_u, after_u, before_c, after_c, before_cap, after_cap, side_effect in itertools.product([False, True], repeat=7):
            before = ick.Snapshot.build(
                authority_level=before_auth,
                evidence_level=before_ev,
                unknowns=["u"] if before_u else [],
                constraints=["c"] if before_c else [],
                capabilities=["write"] if before_cap else [],
            )
            after = ick.Snapshot.build(
                authority_level=after_auth,
                evidence_level=after_ev,
                unknowns=["u"] if after_u else [],
                constraints=["c"] if after_c else [],
                capabilities=["write"] if after_cap else [],
                side_effects=["write"] if side_effect else [],
            )
            for grants in itertools.product([False, True], repeat=5):
                auth_grant, ev_ref, resolve_u, waive_c, grant_cap = grants
                receipt = ick.TransitionReceipt.build(
                    authority_grant_id="g" if auth_grant else None,
                    evidence_refs=["e"] if ev_ref else [],
                    resolved_unknowns=["u"] if resolve_u else [],
                    waived_constraints=["c"] if waive_c else [],
                    granted_capabilities=["write"] if grant_cap else [],
                )
                expected_ok = True
                expected_ok &= not (after_auth > before_auth and not auth_grant)
                expected_ok &= not (after_ev > before_ev and not ev_ref)
                expected_ok &= not (before_u and not after_u and not resolve_u)
                expected_ok &= not (before_c and not after_c and not waive_c)
                expected_ok &= not (after_cap and not before_cap and not grant_cap)
                expected_ok &= not (side_effect and not after_cap)
                report = ick.evaluate_transition(before, after, receipt)
                assert (report.status == "PASS") == expected_ok
                cases += 1
    return cases


def validate_mfwr() -> int:
    cases = 0
    universe = tuple(range(7))
    for size in range(1, 5):
        for required in itertools.combinations(universe, size):
            required_set = set(required)
            result = mfwr.reduce_failure(universe, lambda xs, req=required_set: req <= set(xs))
            assert set(result.witness) == required_set
            assert tuple(sorted(result.witness)) == required
            for i in range(len(result.witness)):
                candidate = result.witness[:i] + result.witness[i + 1 :]
                assert not (required_set <= set(candidate))
            cases += 1
    return cases


def validate_esc() -> int:
    cases = 0
    claim_options = [(), ("C1",), ("C2",), ("C1", "C2")]
    evidence_options = [(), ("E1",), ("E2",)]
    domains = ["P1", "P2"]
    for c2 in claim_options:
        for e2 in evidence_options:
            for d2 in domains:
                r1 = esc.Round.build(round_id="r1", contributions=[
                    esc.Contribution.build(agent_id="a1", independence_domain="P1", claim_ids=["C1"], evidence_refs=["E1"])
                ])
                r2 = esc.Round.build(round_id="r2", contributions=[
                    esc.Contribution.build(agent_id="a2", independence_domain=d2, claim_ids=c2, evidence_refs=e2)
                ])
                report = esc.analyze_rounds([r1, r2], patience=1, min_rounds=2)
                new_claim = bool(set(c2) - {"C1"})
                new_evidence = bool(set(e2) - {"E1"})
                new_support = any((claim, d2) not in {("C1", "P1")} for claim in c2)
                expected_saturated = not (new_claim or new_evidence or new_support)
                assert (report.status == "SATURATED") == expected_saturated
                cases += 1
    return cases


def eval_formula(options, available):
    return any(set(option) <= available for option in options)


def validate_eecp() -> int:
    cases = 0
    leaves = ("A", "B", "C", "D")
    nonempty_subsets = [subset for size in range(1, len(leaves) + 1) for subset in itertools.combinations(leaves, size)]
    # Deterministic sample of formula families: every 1-option and every 2-option OR-of-AND formula.
    families = [(opt,) for opt in nonempty_subsets]
    families += list(itertools.combinations(nonempty_subsets, 2))
    for options in families:
        nodes = [eecp.Evidence(x, 1) for x in leaves]
        branches = []
        for idx, option in enumerate(options):
            branch = f"B{idx}"
            nodes.append(eecp.Claim(branch, "AND", tuple(option)))
            branches.append(branch)
        nodes.append(eecp.Claim("T", "OR", tuple(branches)))
        graph = eecp.EvidenceGraph(nodes)
        actual = set(graph.proof_frontier("T"))

        satisfying = []
        for size in range(len(leaves) + 1):
            for combo in itertools.combinations(leaves, size):
                s = frozenset(combo)
                if eval_formula(options, set(combo)):
                    satisfying.append(s)
        expected = set()
        for candidate in sorted(satisfying, key=lambda s: (len(s), tuple(sorted(s)))):
            if not any(existing <= candidate for existing in expected):
                expected.add(candidate)
        assert actual == expected, (options, actual, expected)

        # Cross-check cutsets by brute-force subset minimal hitting sets.
        brute_cuts = []
        for size in range(1, len(leaves) + 1):
            for combo in itertools.combinations(leaves, size):
                s = frozenset(combo)
                if any(existing <= s for existing in brute_cuts):
                    continue
                if all(s & proof for proof in expected):
                    brute_cuts.append(s)
        actual_cuts = {frozenset(x) for x in graph.minimal_cutsets("T")}
        assert actual_cuts == set(brute_cuts), (options, actual_cuts, brute_cuts)
        cases += 1
    return cases


def validate_uis() -> int:
    cases = 0
    names = ("a", "b", "c", "d")
    variables = [uis.Variable.build(name, [0, 1]) for name in names]
    for mask_bits in range(1 << len(names)):
        influential = {names[i] for i in range(len(names)) if mask_bits & (1 << i)}
        rules = []
        # Exact table. Output parity over only the chosen influential variables.
        for values in itertools.product([0, 1], repeat=len(names)):
            assignment = dict(zip(names, values))
            parity = sum(assignment[name] for name in influential) % 2
            conditions = {name: [assignment[name]] for name in names}
            rules.append(uis.Rule.build("r-" + "".join(map(str, values)), conditions, f"O{parity}"))
        model = uis.ImpactModel(variables, rules, default_output="UNREACHABLE", max_states=100)
        report = model.analyze()
        expected_material = tuple(sorted(influential)) if influential else ()
        assert report.material_unknowns == expected_material, (mask_bits, report.material_unknowns, expected_material)
        if influential:
            assert report.status == "MATERIAL_UNKNOWNS"
        else:
            assert report.status == "STABLE"
        cases += 1
    return cases


def main() -> None:
    counts = {
        "ICK_exhaustive_cases": validate_ick(),
        "MFWR_required_subset_cases": validate_mfwr(),
        "ESC_structural_cases": validate_esc(),
        "EECP_formula_families": validate_eecp(),
        "UIS_influence_masks": validate_uis(),
    }
    total = sum(counts.values())
    for key, value in counts.items():
        print(f"{key}={value}")
    print(f"DEEP_VALIDATION_PASS total_cases={total}")


if __name__ == "__main__":
    main()
