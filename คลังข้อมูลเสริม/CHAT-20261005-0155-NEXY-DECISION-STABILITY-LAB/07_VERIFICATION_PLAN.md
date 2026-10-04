# Verification Plan

Required for lab completion:

1. **E0 Presence** — all design/code/test/evidence files exist at the committed AI-CONTEXT revision.
2. **E1 Static** — compile every Python module using py_compile/compileall.
3. **E2 Unit** — run unittest coverage for each of MONO, IRIS, EDGE, MDE, DAMP plus negative paths.
4. **E3 Integration** — run the five-system suite through one oracle and shared evidence contract.
5. **Determinism** — rerun tests under distinct PYTHONHASHSEED values and compare deterministic fingerprints.
6. **Stress** — fixed-seed 5k MONO cases, 5k fingerprint permutations, 50k temporal transitions; every worsening transition must apply immediately.
7. **Remote exactness** — download code/tests from the exact GitHub commit and rerun verification on those downloaded bytes.
8. **Scope audit** — confirm no repository containing NEXY.AI was mutated.

Higher evidence classes E4/E5/E6 are outside this lab and must remain NOT_VERIFIED.
