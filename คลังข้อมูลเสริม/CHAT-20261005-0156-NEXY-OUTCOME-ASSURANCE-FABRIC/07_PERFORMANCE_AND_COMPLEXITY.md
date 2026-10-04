# Performance and Complexity

## Algorithmic choices

### OCC / ODV / BRG
Linear in the number of criteria/forbidden effects. These are intended to be cheap enough for normal gate usage.

### OSF
Exact Pareto computation is quadratic in candidate count. This preserves multi-objective correctness without inventing a scalar utility function. For very large option sets, a future verified implementation could add pruning/index structures.

### ORP
Exact search is exponential. Reference v1 intentionally rejects more than 16 repair actions. Pretending exact combinatorial optimization is constant-time would be convenient, and also fictional.

## Recorded local sandbox benchmark

See `evidence/benchmark.json` for raw output. One recorded run showed approximately:
- 20,000 verifier calls in ~1.25 s (~15.9k/s);
- 120-candidate Pareto frontier median ~0.0147 s;
- exact 10-action recovery search median ~0.040 s.

These values are **informational only**. They are not production SLAs and do not establish behavior under NEXY deployment, different hardware, different Python builds, or larger contracts.

## Optimization invariants

Performance optimization must not:
- replace exact Pareto dominance with an unexplained aggregate score;
- silently truncate recovery candidates;
- skip hard/forbidden criteria;
- cache across different contract hashes without an explicit validity key;
- turn invalid observation into PASS/FAIL instead of FREEZE.
