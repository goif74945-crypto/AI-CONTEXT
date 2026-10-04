# TEST_PLAN

Gates:
1. TDD RED before implementation.
2. Unit behavior for S01-S20.
3. Q64 exact ratio, overflow, divide-by-zero and multiplication overflow.
4. Malformed payloads must FREEZE, not throw.
5. Any nested binary float must FREEZE `BINARY_FLOAT_FORBIDDEN`.
6. Property: S02 fairness threshold monotonic around exact 1/2 for high=2..29.
7. Adversarial: retry budget, rate-limit inconsistency, duplicate audit sequence, post-cancel effect, replay disclosure, unknown reason, invented evidence ref.
8. Mapping-key reorder and replay determinism.
9. Cross-process PYTHONHASHSEED 0/1/2/42/999/random.
10. compileall.
11. Coverage measured diagnostically, never used as authority.
12. Design-code-test conformance.
13. Repository read-back after preservation.

On failure: record -> root cause -> smallest safe repair -> full regression -> reverify.
