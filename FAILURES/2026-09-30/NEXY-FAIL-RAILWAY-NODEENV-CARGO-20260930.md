# FAILURE — Railway validation environment mismatch

FAILURE_ID: NEXY-FAIL-RAILWAY-NODEENV-CARGO-20260930
context: NEXY exact-head validation
initial_commit: c8a6162ecd6415c1afd990765027dc650a773067

## Symptoms
- contract gate failed
- 74 test files: 71 passed / 3 failed
- 423 tests: 387 passed / 36 failed
- representative error: TEST_ONLY_STATE_RESET_DENIED
- subsequent narrowed run: 73/74 files and 422/423 tests passed, remaining error spawnSync cargo ENOENT

## Root causes
1. Railway build environment exported a non-test NODE_ENV while Vitest test-only reset helpers require NODE_ENV=test.
2. Validation image lacked cargo/Rust toolchain although a contract test executes cargo test --locked -p core-kernel --lib.

## Recovery
- tests/setup/prisma-mock.ts normalizes NODE_ENV=test only inside Vitest setup.
- validation tooling later gained Rust support.
- no production runtime reset bypass was introduced.
- no assertion/test was removed or weakened.

## Verified recovery state
Current exact HEAD fb4f0f064ffe03d032f160f397a515538b4a86bd.
Railway deployment 8ecc0830-d1c4-442f-a282-491a79d166e2 = SUCCESS.
Full suite 859/859 PASS.

prevention:
- validation runners must declare all required toolchains explicitly.
- test-only environment normalization belongs in test harness, never production runtime.
- never infer deploy success from queued/building state; require terminal SUCCESS plus gate logs.
