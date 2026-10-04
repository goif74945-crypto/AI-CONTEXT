# Verification Evidence

## Build
- GCC 14.2 Release build with `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror`: PASS.
- Clang 17 Debug build with AddressSanitizer + UndefinedBehaviorSanitizer: PASS.
- Fresh Release configure/build/test from empty build directory: PASS.

## Test suite
- Behavioral test groups: 29 / 29 PASS.
- Q64 identity iterations: 20,001 PASS.
- Portfolio deterministic property iterations: 2,000 PASS.
- Concepts C01 through C20 all exercised.
- Authority escalation rejection exercised.
- Budget mismatch regression exercised.

## Static audit
`STATIC_AUDIT=PASS`
Scanned production `include/` + `src/` for forbidden:
- binary float types
- clocks
- randomness
- locale/collation semantics
- direct authority-escalation API patterns

## Deterministic replay
- Runs: 50
- Unique output hashes: 1
- Canonical example SHA-256: `f6afd3fb3d0779a92324b93e688c9f5568f8606635afed7612e756db4fc64090`

## Compiler differential
- GCC 14.2 canonical example output SHA-256: `f6afd3fb3d0779a92324b93e688c9f5568f8606635afed7612e756db4fc64090`
- Clang 17 ASan/UBSan canonical example output SHA-256: same
- Byte comparison: PASS

## Evidence classes
- Local implementation behavior: VERIFIED.
- Standalone package composition: VERIFIED.
- Cross-compiler deterministic example: VERIFIED for inspected compilers.
- NEXY runtime integration: NOT VERIFIED.
- Production security/performance at NEXY scale: NOT VERIFIED.
- Canon promotion: NOT PERFORMED.

The full raw evidence files are preserved in the sealed bundle.
