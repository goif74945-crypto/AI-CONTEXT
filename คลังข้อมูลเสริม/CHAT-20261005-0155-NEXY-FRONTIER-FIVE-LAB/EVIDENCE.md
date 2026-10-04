# Evidence Record

Project: `CHAT-20261005-0155-NEXY-FRONTIER-FIVE-LAB`
Status of actual NEXY integration/runtime/deployment: `NOT_VERIFIED`

## Environment

- Node.js `v22.16.0`
- npm `10.9.2`
- TypeScript `5.8.3`

## Failure → fix history

1. **Initial compile failure:** `TS2688 Cannot find type definition file for 'node'`. Fix: remove external `@types/node` dependency requirement and add minimal local declarations for used Node built-ins.
2. **Cache diagnostic defect found by design re-audit:** full provenance key lookup hid authority/policy/dependency drift behind `ABSENT`. Fix: separate request identity from full provenance validation and add explicit drift tests.
3. **Failure minimizer duplicate-value defect:** set-based subtraction could remove equal values at multiple positions. Fix: range/position-based chunk removal and regression test.
4. **Determinism risk:** `localeCompare` was unsuitable as a deterministic cross-environment ordering primitive. Fix: explicit code-unit lexical comparator.
5. **Regression harness inefficiency:** recompiling for every repeated run hit execution timeout. Fix: perform one clean final build, then rerun the exact compiled test artifact repeatedly.
6. **Connector publication optimization:** split source/tests were bundled into one source and one test file to reduce remote write surface. The bundle was rebuilt and all tests rerun; no evidence from the split layout was reused as final bundle proof.

7. **Final pre-publication audit defect:** Trace Invariant Miner path traversal still used `localeCompare` even though canonicalization had been fixed. This invalidated the prior final evidence. Fix: replace the remaining call with `compareCodeUnits`, add a regression test that temporarily makes `localeCompare` throw, then rebuild and rerun all evidence.

## Final evidence classes

### E1 — Static build

`npm run check` performs clean → `tsc -p tsconfig.json` → Node test suite.

Final bundled result: `PASS`.

### E2 — Unit behavior

22 tests cover positive and negative behavior across canonicalization, PACF, DFE, FCM, TIM and MES.

Final bundled result: `PASS`.

### E3 — Standalone integration

The integration test composes all five modules into one `advisoryOnly: true` report and checks digest, evidence-plan, invariant-mining and failure-minimization outputs.

Final bundled result: `PASS`.

This is E3 only for the standalone lab modules. It is **not** NEXY.AI integration evidence.

### Repeated regression

The exact compiled artifact from the final bundle build is executed repeatedly. Raw output: `evidence/repeat-regression-output.txt`.

Final result: `PASS` only if every recorded run reports `tests=22 fail=0`.

## Limitations

- No NEXY.AI source was modified or executed.
- No UI/browser E2E.
- No database/queue/external model/tool provider.
- No production load/fault benchmark.
- No deployment proof.
- TIM proposals are observations, not authority.
- PACF is a reuse gate, not an evidence generator.
