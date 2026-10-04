# NEXY Formal Novelty-5 Lab

**Execution code:** `CHAT-20261005-0222-NEXY-FORMAL-NOVELTY-5-SOL`  
**Platform chat ID:** `UNKNOWN_NOT_EXPOSED`  
**Classification:** `Lo4 / AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL / ISOLATED REFERENCE IMPLEMENTATION`  
**Target repository:** `goif74945-crypto/AI-CONTEXT` only  
**Protected scope:** every repository whose name contains `NEXY.AI` is read-only / no mutation authorized or performed.

## Why this lab exists

NEXY's source-derived direction is deterministic, evidence-first, authority-controlled and fail-closed. Existing supplemental work already covers proof capsules, model drift, capability routing, authority leases, counterfactual verification, shadow execution, policy monotonicity, evidence closure, context taint, concurrency and many other topics.

This lab targets five narrower gaps that are useful precisely because they sit *before* or *between* those systems:

1. **RUC — Requirement Unsat Core**  
   Finds an irreducible set of mutually incompatible finite-domain requirements instead of returning a vague “requirements conflict” error.
2. **AEP — Absence Evidence Planner**  
   Prevents `not found` from being promoted to `does not exist` unless every declared authoritative search surface has current, version-bound coverage.
3. **SNCG — Semantic Namespace Collision Guard**  
   Detects when the same name/alias/semantic ID resolves to incompatible meaning across layers, units, domains, authority sources or lifecycles.
4. **TICM — Trace Invariant Candidate Miner**  
   Mines deterministic *candidate* invariants from traces, validates them against holdout traces, and explicitly refuses to promote observations into canon.
5. **RDRC — Requirement Delta Revalidation Compiler**  
   Compares structured requirement revisions and deterministically emits the evidence class and revalidation gates affected by additions, removals, tightening, loosening or mixed changes.

## Combined future pipeline

```text
SOURCE / USER DIRECTIVE
        ↓
[RUC] detect exact contradictory requirement core
        ↓
[SNCG] reject semantic/name collisions in contracts
        ↓
[RDRC] compile requirement changes into revalidation obligations
        ↓
[AEP] prevent false absence claims during audit/evidence search
        ↓
[TICM] propose observed invariants as NON-CANONICAL candidates only
        ↓
NEXY canonical authority / judge / verification layers decide separately
```

The components are intentionally **advisory**. None has authority to alter NEXY canon, waive evidence requirements, or silently broaden scope.

## Verification completed in isolated sandbox

- Python static bytecode compilation: PASS (`python3 -m compileall -q .`)
- Unit/negative-path suite: PASS, **20 tests**
- Deterministic stress checks: PASS
  - RUC: 200 seeded randomized cases, irreducible-core property rechecked
  - AEP: 100 input-order permutations
  - SNCG: 2,000 clean symbols + injected collision
  - TICM: 10,000 trace records, repeat-output equality
  - RDRC: 2,000 requirement deltas, repeat-output equality

These results prove only the isolated reference implementations in this lab. They do **not** prove NEXY.AI runtime integration, production performance, deployment readiness, canonical acceptance, or compatibility with an uninspected implementation revision.

## Reproduce

```bash
python3 -m compileall -q .
python3 run_all_tests.py
python3 stress_checks.py
```

## Promotion law

Lo4 ideas remain proposals until a separate authorized promotion process maps them against current canonical NEXY requirements, exact implementation state, required evidence class, regression tests and deployment gates. A green prototype is not promotion evidence.
