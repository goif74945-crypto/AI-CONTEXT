# Validation Report

**Artifact status:** `PASS` for this standalone experimental tool slice.  
**NEXY integration status:** `NOT_VERIFIED / NOT PERFORMED`.

## Tests executed locally

```text
python -m unittest discover -s tests -v
Ran 14 tests
OK
```

Covered behaviors:

1. all-PASS gate allows;
2. ALL combines blockers;
3. ANY exposes alternative minimal repairs and cost ranking;
4. threshold repair calculation;
5. stale revision downgrades PASS;
6. insufficient evidence class downgrades PASS;
7. conflict summary precedence;
8. evidence-map insertion order does not alter certificate;
9. unknown leaf rejection;
10. invalid threshold rejection;
11. inclusion-minimal set eliminates dominated supersets;
12. nested repair sets match a brute-force oracle;
13. 50 seeded deterministic structural-regression iterations;
14. repair-set limit is disclosed.

## CLI fixture

Input: `fixtures/release_gate_example.json`, locked to recorded NEXY revision `9e615b04...`.

Observed:

- root compact status: `FAIL`;
- decision: `FREEZE`;
- primary/recommended repair set:
  - `core_branch_coverage`
  - `doc_e_e11_signoff`
  - `doc_e_e12_rollback_provider`
- generated certificate SHA-256:
  `fbd001162936086eb9e53a52df7218cd99ee657d3e78d19c950bd7ddce23153c`.

The example chooses E11 rather than the blocked GitHub Actions alternative because the declared sample repair cost is lower. That is a demonstration of the ranking contract, **not** an authoritative statement that obtaining E11 is actually easier, safer, or sufficient for NEXY release.

## Evidence classification

- E0 presence: available after repository write/read-back.
- E1 static: PASS in local sandbox.
- E2 unit: PASS in local sandbox.
- E3 integration with NEXY: NOT_VERIFIED.
- E4 end-to-end: NOT_VERIFIED.
- E5 runtime/operational: NOT_VERIFIED.
- E6 deployment: NOT_VERIFIED.
- E7 physical: out of scope.

## Known limitations

- Monotone formulas only.
- Exponential repair enumeration is bounded and may truncate.
- Scalar repair cost is advisory caller data.
- Upstream evidence authenticity is not verified by this engine.
- Gate completeness depends entirely on the caller's declared evidence inventory.
- Presence of the tool in AI-CONTEXT does not make it NEXY law.
