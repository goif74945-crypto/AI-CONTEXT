# CFPC-20 Verification Receipt

## Environment
- GCC: g++ 14.2.0
- Clang: 17.0.0
- CMake: 3.31.6
- Ninja: 1.12.1
- Language: C++20

## E1 build/static
PASS — GCC Release build under `-Wall -Wextra -Wconversion -Wsign-conversion -Werror`.
PASS — Clang Release build under the same warning-as-error policy.
PASS — authoritative numeric/core static scan: 4 files scanned, 0 binary-float type/parser/literal hits.
PASS — SHA-256 known vectors for empty string and "abc" are executed in the unit suite.

## E2 unit/property/negative
Final suite result under GCC: `PASS=60 FAIL=0`.
Final suite result under Clang: `PASS=60 FAIL=0`.
Final suite result under ASan+UBSan: `PASS=60 FAIL=0`.

Property campaigns inside the suite:
- 25,000 deterministic linear-bound evaluations against an integer oracle.
- 5,000 monotonicity comparisons for supported nonnegative quadratic bounds.
- 1,000 certificate replays checked for identical digest.

Negative coverage includes:
- Q64 divide-by-zero;
- Q64 add/sub/multiply overflow;
- decimal precision rejection;
- empty/oversized workload;
- unbound input dimension;
- negative coefficient;
- unsupported exponent;
- dimension-power overflow;
- missing verification obligation;
- unsafe degradation;
- Canon mutation request;
- Core-state mutation request;
- automatic promotion request;
- over-budget resource;
- missing resource claim;
- duplicate resource claim;
- malformed identity hash.

## E3 standalone integration/replay
PASS — integration example emits PASS certificate under declared feasible policy.
PASS — two fresh executions were byte-identical.
Replay SHA-256 both runs:
`22bd37474d7c3822f0a572cf1c9dddfaa5bdcbfa8af4bad3c88b933d9b8c28e7`.

PASS — canonicalization remains identical when resource and monomial insertion order changes.
PASS — certificate changes when budget policy, assumptions, or verification-set content changes.

## Sanitizers
PASS — ASan+UBSan build after correcting executable linker instrumentation.
PASS — test suite under ASan+UBSan.
PASS — integration example under ASan+UBSan with halt-on-error.

## Publication identity
PASS — all 9 source/test/build files fetched from GitHub matched the locally computed Git blob identity of the exact tested bytes. See SOURCE_MANIFEST.md.

## Evidence boundary
Standalone CFPC source/runtime: VERIFIED at E1/E2/E3 for the exact published bytes.
NEXY adapter integration: NOT_VERIFIED.
NEXY production runtime: NOT_VERIFIED.
Deployment: NOT_VERIFIED.
Truth of any future proposal's declared complexity bound: NOT_VERIFIED until independently linked to that implementation.
