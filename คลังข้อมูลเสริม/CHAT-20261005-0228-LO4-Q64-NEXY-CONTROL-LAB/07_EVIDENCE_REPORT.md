# Evidence Report

Work ref: `CHAT-20261005-0228-LO4-Q64-NEXY-CONTROL-LAB`

## Executed evidence

- **E0 Presence — PASS**: `verify.mjs` found exactly 20 concept directories and all required `DESIGN.md + CODE.ts + TEST.test.ts + EVIDENCE.md` files.
- **E1 Static — PASS**: `tsc --noEmit` completed successfully under TypeScript 5.8.3 strict mode.
- **E1 policy scan — PASS**: decision-module scan found Q64 usage in all 20 modules and no `Math.*`, `parseFloat`, `Number(...)`, filesystem, child-process, env, or global fetch primitives.
- **E2 Unit/adversarial/property — PASS**: Node 22.16 executed **42/42 tests PASS**, including **50,000 deterministic arithmetic invariant iterations**, overflow, divide-by-zero, malformed decimal, unit-domain rejection, duplicate-ID rejection, no-safe-model, zero-weight allocation, privacy budget, and safety gates.
- **E3 local package integration — PASS**: `integration-all.test.ts` composed all 20 systems in one deterministic control flow; `integration.test.ts` also passed a focused multi-module decision chain.
- **Build evidence — PASS**: TypeScript emitted runnable JavaScript to `dist/`; compiled smoke execution passed.
- **Source/build determinism — PASS**: source and compiled probe SHA-256 were identical: `cab78256b941a69dec77dd021512616798a7fd899a4e98abcf736d0ac47c1dfb`.

## Failure/fix history

1. Initial runtime suite: 25/27 PASS; PrivacyBudgetGovernor used a TypeScript parameter property unsupported by Node strip-only runtime.
2. Fixed to explicit class property; rerun: 27/27 PASS.
3. Design re-audit found hidden unit clamping contradicted the declared no-hidden-saturation invariant.
4. Replaced clamping with fail-closed unit validation, enforced BigInt integer constructors, exact residual accounting, duplicate-ID rejection, and stronger adversarial tests.
5. Final suite: 42/42 PASS + 50,000 arithmetic invariants + source/build digest match.

## Evidence boundary

- **E4 NEXY end-to-end: NOT_VERIFIED**
- **E5 NEXY runtime/operational: NOT_VERIFIED**
- **E6 NEXY deployment: NOT_VERIFIED**
- **Canon promotion: NOT PERFORMED / NOT AUTHORIZED**

Local E1-E3 PASS proves this standalone lab at this captured content, not integration into the separate NEXY.AI repository.
