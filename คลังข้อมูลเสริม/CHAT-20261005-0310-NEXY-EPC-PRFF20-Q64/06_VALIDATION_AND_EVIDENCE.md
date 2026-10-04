# Validation and Evidence

## Final tested source surfaces
Evidence files are stored under `evidence/` and source identities under `evidence/SOURCE_SHA256.txt`.

### GCC 14.2 Release
`evidence/01_gcc_release.txt`
- CTest 3/3 PASS.
- unit PASS.
- property PASS, 14,207 checks.
- sanitizer stress logic PASS, 200 cases.

### GCC strict warning gate
`evidence/02_gcc_strict.txt`
Adds:
`-Wconversion -Wsign-conversion -Wshadow -Wnull-dereference -Wduplicated-cond -Wduplicated-branches -Wlogical-op`
on top of target `-Wall -Wextra -Wpedantic -Werror`.
Result: 3/3 PASS.

### Clang 17 independent compiler
`evidence/03_clang_release.txt`
Result: 3/3 PASS.

### UBSan
`evidence/04_ubsan_full.txt`
- unit PASS;
- full 14,207 property checks PASS;
- 200-case stress PASS.

### ASan
`evidence/05_asan_bounded.txt`
- unit PASS;
- 200-case stress PASS;
- integration example PASS;
- full 14,207-property binary under ASan is explicitly `NOT_VERIFIED_BY_THIS_GATE` because full-instrumented attempts exceeded the command budget. It is not reported as PASS.

### Q64.64 / float exclusion
`evidence/06_float_scan.txt`: PASS for `include/**/*.hpp + src/**/*.cpp`.
No authoritative `float`, `double`, decimal floating literal or float conversion/math API is present in that scope.

### Deterministic replay
`evidence/07_replay_hashes.txt`:
10/10 example runs have one unique SHA-256:
`e52f6fa0ace6819816d2f7c5ecb7b0fb21acfa8f1aaf3fe7a02cf474fc362ff8`.

## Property/oracle coverage
`tests/property_main.cpp` contains:
- 10,000 exact Q64 complement identities;
- closed-form parallel-path oracle for 2..8 channels;
- 200 random DAGs where production evidence-vertex min-cut, edge min-cut and minimum cut-family count are compared to exhaustive brute-force subset removal;
- 2,000 node/edge/target order permutations requiring byte-identical canonical output;
- 2,000 support-edge mutations requiring strict resilience downgrade.

Total reported property cases/check groups: 14,207.

## Adversarial unit coverage
- resilient three-path PASS;
- single-path fail-closed;
- 3 roots merged through one shared channel -> C04 catches collapse;
- shared multi-claim bottleneck under isolation policy -> fail;
- independent multi-claim paths -> pass;
- exact search budget exhaustion -> block;
- duplicate nodes -> reject;
- illegal edge into ROOT -> reject;
- dependency cycle -> reject;
- exact Q64 half/complement and out-of-domain ratio behavior.

## Failure evidence preserved
Compilation regressions, iteration-label correction, ASan budget limitation and sanitizer-stress oracle correction are documented in `00_TEMP_MEMORY.md`; they were not erased from the audit narrative.
