# CASE-NEXY-MATRIX-R1-20260930

CASE_ID: CASE-NEXY-MATRIX-R1-20260930
cause: Matrix/design convergence required real validation; prior Railway environment invalidated otherwise-correct tests.
violation: Validation environment lacked required test semantics/toolchain; therefore prior evidence could not authorize completion.
impact: No system may be counted as 70% solely from prior source presence or stale test evidence.
fix: test-only NODE_ENV normalization + Railpack Rust installation + exact-head SHA/tree binding.
prevention: require source→claim→test→exact-head deployment evidence chain.
regression:
- observed full suite 856/856 PASS
- observed coverage gate PASS
- observed DOC-C static PASS
- observed web build exit=0
status: OPEN_UNTIL_TERMINAL_DEPLOYMENT_AND_E3
