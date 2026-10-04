# EDEL Evidence

- E1: AST/compileall PASS.
- E2: fresh evidence PASS; stale root invalidation PASS; dependent propagation PASS; insufficient evidence-class detection PASS; unknown dependency rejection PASS; dependency-cycle rejection PASS; deterministic ordering PASS.
- Stress: EDEL fingerprint stable across seeded claim/evidence permutations in combined 40,000-check stress run.
- E3: integrated promotion gate freezes when proof debt exists.

Limits: correct subject-version binding must be supplied by an external integration. This isolated prototype does not discover code dependencies automatically.
