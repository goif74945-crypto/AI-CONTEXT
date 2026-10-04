# NEXY Outcome Assurance Fabric (OAF)

**Classification:** `AI-PROPOSED / EXPERIMENTAL / NOT NEXY CANON / NOT INTEGRATED`

OAF is a standalone deterministic research/reference package stored in `AI-CONTEXT`. It is designed to answer a gap that action-level verification alone cannot answer:

> **Did the completed work produce the user-authorized end state, without silently sacrificing a protected benefit?**

The project contains five independently callable systems:

1. **OCC — Outcome Contract Compiler**: compiles an explicit objective, hard/soft criteria, forbidden outcomes, and regression protections into a canonical SHA-256-bound contract.
2. **ODV — Outcome Delta Verifier**: compares observed end state against the contract and returns `PASS | PARTIAL | FAIL | FREEZE` with typed deltas.
3. **OSF — Outcome Satisfaction Frontier**: preserves real multi-objective tradeoffs using a Pareto frontier instead of collapsing everything into one weighted score.
4. **BRG — Benefit Regression Guard**: blocks candidates that improve aggregate score while materially degrading protected user benefits.
5. **ORP — Outcome Recovery Planner**: proposes the minimum admissible reversible repair set that can make the outcome contract pass, under cost/risk bounds.

## Authority boundary

OAF does **not** change NEXY.AI, does **not** authorize actions, and does **not** prove that NEXY.AI implements any OAF feature. A future adapter could submit OAF outputs to existing NEXY authority/JUDGE layers for separate adjudication.

## Design properties

- deterministic canonical JSON and SHA-256 identity;
- strict unknown-field rejection;
- fail-closed behavior for malformed/missing/invalid observations;
- no network, model call, subprocess, clock, randomness, filesystem, or environment access in the core library;
- explicit distinction between hard failure, soft partial outcome, and insufficient observation;
- exact Pareto dominance, not score-only selection;
- exact bounded recovery search, capped at 16 candidate repair actions to avoid unbounded exponential work;
- no automatic execution of a recovery plan.

## Local validation

```bash
PYTHONPATH=src python -m compileall -q src tests tools
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python tools/benchmark.py
python -m json.tool schemas/outcome-contract.schema.json >/dev/null
python -m json.tool schemas/outcome-report.schema.json >/dev/null
```

See `08_VALIDATION_EVIDENCE.md` and `evidence/` for the recorded run. Timings are informational sandbox evidence, not production guarantees.
