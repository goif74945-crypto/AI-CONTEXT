# Validation Report

Classification: `EXECUTION_EVIDENCE`

## Environment
- Node.js `v22.16.0`
- npm `10.9.2`
- Python `3.13.5`
- project dependencies: none beyond Node/Python standard runtimes

## Final gates
1. `node --check` on all JS/MJS sources: PASS.
2. `npm run test:all`: PASS, 107/107.
3. `python3 scripts/q64-oracle.py`: PASS, 16 vectors.
4. `node scripts/replay-stress.mjs`: PASS, 10,000 executions, 20 distinct baseline digests, no observed drift.
5. `node bench/benchmark.mjs`: PASS, 20,000 evaluations. Observed run: ~69,606 evaluations/s. Throughput is environment-specific and not a correctness guarantee.
6. `node src/cli.js fixtures/smoke.json`: PASS with canonical deterministic output and SHA-256 digest.

## What is proven
- authored modules parse under the observed Node runtime;
- the static policy gate finds exactly 20 marked Lo4 modules and none of its forbidden patterns;
- tested Q64 arithmetic and concept contracts behave as asserted in the current suite;
- selected Q64 vectors match a separately implemented Python exact-rational oracle;
- repeated identical sample inputs produced stable result digests over the observed replay workload;
- CLI and multi-module composition work in the local environment.

## What is not proven
- production NEXY integration;
- full semantic correctness of every proposed formula for every future domain;
- real-world calibration of thresholds;
- E4 browser/user flow, E5 operational recovery, E6 deployment, or E7 physical-system behavior;
- global performance guarantee.

## Verdict
Standalone reference implementation: `PASS` for the explicitly executed local gates.
NEXY.AI adoption/integration: `NOT_VERIFIED` and not authorized by this project.
