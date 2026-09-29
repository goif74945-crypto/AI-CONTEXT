# CASE — Exact-head Railway validation recovery

CASE_ID: NEXY-CASE-EXACT-HEAD-RAILWAY-VALIDATION-20260930
cause: runner/test-environment mismatch plus missing Rust toolchain
impact: false-negative contract failures blocked evidence generation
fix: isolate test NODE_ENV normalization to Vitest setup; provide Rust tooling in validation path
regression_result: PASS at fb4f0f064ffe03d032f160f397a515538b4a86bd
railway_deployment: 8ecc0830-d1c4-442f-a282-491a79d166e2

Reusable rule:
A passing source inspection is insufficient. Exact-head validation must prove:
- terminal Railway SUCCESS
- full test gate exit=0
- coverage gate exit=0
- DOC-C static gate exit=0
- web build exit=0
- required migration roundtrip evidence exit=0
- commit/tree identity bound to evidence

Do not weaken tests to fit the runner; repair the runner or test harness without changing production semantics.
