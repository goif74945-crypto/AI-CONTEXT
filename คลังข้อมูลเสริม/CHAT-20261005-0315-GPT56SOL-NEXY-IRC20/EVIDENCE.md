# IRC-20 Evidence Ledger

## Environment
- Node: 22.16.0
- TypeScript compiler: 5.8.3
- npm: 10.9.2
- workspace: isolated `/mnt/data/irc20` during execution
- network is not required by build/tests

## Evidence classes

### E0 — Presence
Local source/design/test/evidence files exist. Durable GitHub E0 requires publication and read-back and is intentionally not inferred from local presence.

### E1 — Static
- strict TypeScript compile passed;
- static audit found exactly 20 unique mechanism IDs;
- static audit found no wall-clock/RNG/network/child-process/env/float-parser forbidden patterns in `src/`;
- Q64 implementation tokens/bounds/rounding/failure controls present.

### E2 — Unit / property
Latest local suite: 44/44 passing.
Includes:
- all twenty mechanism negatives/positives;
- Q64 exact/tie-even/overflow/divide-zero/grammar vectors;
- strict unknown-field rejection;
- truth-dimension separation;
- conservative discovery cases;
- 50 in-suite semantic permutation replays;
- 10,000-module no-recursion-overflow graph case.

Additional deterministic stress executable:
- 1,000 semantic permutations;
- 1,000 injected valid-manifest defects that must FAIL closure;
- 500 malformed unknown-field cases that must fail before analysis;
- 5,000 Q64 deterministic arithmetic vectors.

### E3 — Integration
- complete reference engine runs all 20 mechanisms over one healthy manifest and returns PASS;
- integrated broken manifest runs the same engine and returns FAIL;
- CLI healthy replay executed twice and output bytes are identical;
- broken CLI returns exit status 1, distinguishing analyzed failure from malformed-input exit 2.

## Failure/recovery evidence

The development record intentionally preserves failures:
1. RED phase: tests failed because implementation did not exist yet.
2. Q64 inverse test was over-strong by 1 ULP; corrected test to the mathematically valid fixed-point bound.
3. AUTHPATH fixture hit NOT_BUILT before UNREACHABLE; corrected fixture to isolate reachability.
4. discovery missed side-effect-only ES import; parser corrected and regression passed.
5. graph implementation hardened from shift/recursive SCC to scalable index/iterative traversal.

See `evidence/FAILURE_FIX_LOG.md` and raw logs.

## Claims not proven
- full NEXY repository execution: NOT_VERIFIED;
- NEXY runtime/production/deployment: NOT_VERIFIED;
- semantic TS/Rust equivalence: NOT_VERIFIED;
- Canon promotion: not performed and not authorized.
