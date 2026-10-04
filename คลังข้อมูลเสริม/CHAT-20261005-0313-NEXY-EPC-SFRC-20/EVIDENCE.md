# Verification Evidence — SFRC-20

## Evidence target
Standalone workspace corresponding to the exact source files stored in the verified bundle. This evidence does **not** claim NEXY production/runtime integration.

## Environment
- Node.js: `v22.16.0`
- npm: `10.9.2`
- TypeScript compiler: `5.8.3`
- execution environment: isolated ChatGPT container workspace

## E1 static/build evidence
Executed:
```bash
npx tsc -p tsconfig.json
find dist -type f -name '*.js' -print0 | sort -z | xargs -0 -n1 node --check
```
Observed PASS, exit code 0.

Additional scans found no `Math.random`, `Date.now`, `performance.now`, `crypto.random`, `fetch(`, or `localeCompare(` in `src/`; no decimal floating numeric literals in `src/`; and all markers `SFRC-01` through `SFRC-20` present.

## E2 unit/property/negative evidence
```text
SUMMARY passed=50 failed=0 total=50
```
Coverage includes Q64 arithmetic/div0/signed-i128 overflow, finite-grid property vectors, all SFRC-01..20 behaviors, metric drift, confounders, intervention leakage, window violations, peeking, multiplicity, incomplete scenario coverage, weak perturbation, self-replication, duplicate replicator, protocol mismatch, missing environment replication, null hash chain, regression-to-mean, falsification, insufficient/negative replication, critical-gate failure, unresolved null, incomplete packet evidence and advisory-only authority.

## E3 deterministic replay evidence
The chamber flow was run through confounder/isolation/window/metric/peeking/multiplicity/effect/robustness/replication/cross-environment/regression/falsification/synthesis/packet stages twice. Both complete 50-test runs passed; the two logs are byte-identical and `replay-diff.log` is empty.

## Tested source size
```text
55   src/canonical.ts
4    src/index.ts
120  src/model.ts
143  src/q64.ts
664  src/sfrc.ts
494  test/run-tests.ts
1480 total lines
```

## Key SHA-256 pins
- `src/sfrc.ts`: `3b6d6db6f862f2a616115b75787cfcf7d7702e08856fd15cfef1b55f6236d723`
- `test/run-tests.ts`: `51fc07358f83287808ffc2ae74763cec12c0a510ebb33802f294b11361249c3d`
- `evidence/test-run-1.log`: `96754231f6ca269ebdd208bac2643a40afb8214d224a2d74de736fe61c7099ac`
- exact tested source+evidence archive: `71982d0ae740a2158115b9337eda318e1a6c48be884dadec573a088597cd6083`

## GitHub persistence verification
The archive is persisted as ten base64 chunks under `bundle/`. Read-back verification from GitHub produced 10/10 matching chunk SHA-256 values, 39,664 joined base64 characters, 29,747 decoded archive bytes, and archive SHA-256 exactly `71982d0ae740a2158115b9337eda318e1a6c48be884dadec573a088597cd6083`.

## Verification classification
- E0 presence: PASS after GitHub read-back.
- E1 static/type/syntax: PASS.
- E2 unit/property/negative: PASS, 50/50 twice.
- E3 standalone multi-system chamber integration/replay: PASS.
- E4 NEXY end-to-end integration: NOT_VERIFIED, intentionally not performed.
- E5 NEXY production/runtime: NOT_VERIFIED.
- E6 deployment: NOT_VERIFIED.

The tests prove the standalone experimental implementation at the hashed source revision. They do not prove NEXY currently calls this package; modifying NEXY.AI was explicitly forbidden.
