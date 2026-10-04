# DRCDO Evidence

- E1: AST/compileall PASS.
- E2: equivalent mapping-order outputs PASS; divergent output freezes; executor exception freezes; invalid policy identity rejected; malicious nested-input mutation cannot poison the next replay.
- Stress: DRCDO fingerprint stable across seeded executor-map order permutations in combined 40,000-check stress run.
- E3: integrated promotion gate freezes when replay divergence exists.

Limits: executors are local callables in this prototype; provider/network/runtime replay is NOT_VERIFIED.
