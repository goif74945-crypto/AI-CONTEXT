from __future__ import annotations

import importlib.util
import pathlib
import random
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {rel}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ruc = load("ruc", "01_requirement_unsat_core/ruc.py")
aep = load("aep", "02_absence_evidence_planner/aep.py")
sncg = load("sncg", "03_semantic_namespace_collision_guard/sncg.py")
ticm = load("ticm", "04_trace_invariant_candidate_miner/ticm.py")
rdrc = load("rdrc", "05_requirement_delta_revalidation_compiler/rdrc.py")


def check_ruc() -> None:
    rng = random.Random(20261005)
    domains = {f"v{i}": tuple(range(4)) for i in range(5)}
    solver = ruc.RequirementUnsatCore(domains, max_assignments=2_000)
    for case in range(200):
        reqs = []
        for j in range(rng.randint(1, 8)):
            var = f"v{rng.randrange(5)}"
            value = rng.randrange(4)
            kind = "eq" if rng.random() < 0.5 else "neq"
            reqs.append(ruc.Requirement(f"C{case}-R{j}", (ruc.Rule(kind, var, value=value),)))
        a = solver.solve(reqs)
        b = solver.solve(reqs)
        assert a == b, "RUC non-determinism"
        if not a.satisfiable:
            core = [x for x in reqs if x.requirement_id in a.core_ids]
            assert not solver.solve(core).satisfiable
            for idx in range(len(core)):
                reduced = core[:idx] + core[idx + 1 :]
                assert solver.solve(reduced).satisfiable, "core is not irreducible"


def check_aep() -> None:
    surfaces = [aep.SurfaceSpec(f"s{i}", max_age_seconds=100, expected_version=f"v{i}", scan_cost=i + 1) for i in range(25)]
    obs = [aep.Observation(f"s{i}", "x", 100, f"v{i}") for i in range(25)]
    baseline = aep.AbsenceEvidencePlanner.evaluate("x", surfaces, obs, now=150)
    assert baseline.status == "PASS"
    for _ in range(100):
        shuffled_surfaces = list(surfaces)
        shuffled_obs = list(obs)
        random.Random(_).shuffle(shuffled_surfaces)
        random.Random(_ + 1).shuffle(shuffled_obs)
        got = aep.AbsenceEvidencePlanner.evaluate("x", shuffled_surfaces, shuffled_obs, now=150)
        assert got.status == baseline.status
        assert got.missing_surfaces == baseline.missing_surfaces


def check_sncg() -> None:
    contracts = [
        sncg.SymbolContract("n", f"symbol-{i}", f"id-{i}", "scalar", "domain", None, "A", "runtime")
        for i in range(2_000)
    ]
    assert sncg.SemanticNamespaceCollisionGuard.analyze(contracts) == ()
    contracts.append(sncg.SymbolContract("other", "SYMBOL-10", "other-id", "duration", "other", "seconds", "B", "runtime"))
    collisions = sncg.SemanticNamespaceCollisionGuard.analyze(contracts)
    assert any(c.label == "symbol-10" for c in collisions)


def check_ticm() -> None:
    train = [{"phase": "run", "step": i, "load": i % 7} for i in range(10_000)]
    result_a = ticm.TraceInvariantCandidateMiner.mine(train)
    result_b = ticm.TraceInvariantCandidateMiner.mine(train)
    assert result_a == result_b
    assert any(c.kind == "nondecreasing" and c.field == "step" for c in result_a)


def check_rdrc() -> None:
    old = []
    new = []
    for i in range(2_000):
        old.append(rdrc.RequirementSpec(
            f"R{i}", {"mode": rdrc.FieldConstraint("allowed_set", values=("safe", "fast"))}, 2
        ))
        values = ("safe",) if i % 2 == 0 else ("safe", "fast")
        new.append(rdrc.RequirementSpec(
            f"R{i}", {"mode": rdrc.FieldConstraint("allowed_set", values=values)}, 2
        ))
    a = rdrc.RequirementDeltaRevalidationCompiler.compare(old, new)
    b = rdrc.RequirementDeltaRevalidationCompiler.compare(old, new)
    assert a == b
    assert sum(d.change == "TIGHTENED" for d in a) == 1_000
    assert sum(d.change == "UNCHANGED" for d in a) == 1_000


def main() -> int:
    checks = [check_ruc, check_aep, check_sncg, check_ticm, check_rdrc]
    started = time.perf_counter()
    for fn in checks:
        t0 = time.perf_counter()
        fn()
        print(f"PASS {fn.__name__} elapsed={time.perf_counter()-t0:.6f}s")
    print(f"FINAL: PASS total_elapsed={time.perf_counter()-started:.6f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
