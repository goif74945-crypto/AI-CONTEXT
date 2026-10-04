# SCARM-20 Local Verification Evidence

## Claim classes
- E1 static/type correctness: PASS for the standalone SCARM package at the exact hashed source bytes.
- E2 unit/negative/property behavior: PASS locally.
- E3 standalone integration/replay behavior: PASS locally.
- NEXY runtime integration/deployment: NOT_VERIFIED and not claimed.

## Environment
- Node.js: v22.16.0
- npm: 10.9.2
- TypeScript compiler: 5.8.3
- Host: isolated task container; no NEXY repository mutation was performed.

## E1
Command: `npm run build`
Result: PASS, exit 0.
Evidence: `evidence/final-build.log`.

Static verification additionally checked:
- no `Math.random`, wall-clock Date/performance APIs, locale collation, timers, or float formatting/parsing in authoritative source;
- no direct fs/network/child-process imports in `src`;
- no decimal numeric literals in `src`;
- all 20 mechanism identifiers are present.
Result: PASS.
Evidence: `evidence/static-verification.txt`.

## E2
Command: `npm test`
Result: 28 passed, 0 failed, 0 skipped.
Coverage by intent includes:
- Q64.64 exact arithmetic and overflow/divide-by-zero failure;
- positive and negative cases for C01-C20;
- UNKNOWN behavior for missing explicit evidence/provenance;
- hard-block behavior for revision laundering, spent-right appeal, incomplete vote reasoning, and dropped dissent;
- exhaustive 5! ballot-order permutations;
- exhaustive 6! evidence-order and tie-order permutations;
- deterministic Q64 Jaccard symmetry/range corpus;
- regression for DEFECT-001.
Evidence: `evidence/final-test.log`.

## E3 standalone integration
Test: `E3 multi-mechanism dossier detects manipulation deterministically and blocks only at advisory review boundary`.
Result: PASS.
It composes 19 findings into MANIPGATE64, verifies hard blockers, changes input order, and proves normalized result equality.

## Cross-process determinism
Command: run `scripts/determinism-replay.mjs` twice and byte-compare outputs.
Result: PASS. Final replay outputs are byte-identical.
Evidence: `evidence/replay-final-a.json`, `evidence/replay-final-b.json`.

## Defect/fix loop
DEFECT-001 was found after an initially passing test set, repaired, and regression-tested. See `evidence/DEFECT-001-MANIPGATE-CLEAR-SEVERITY.md`.

## Limits
- Semantic atoms are explicit normalized inputs; this package does not claim embedding/NLP semantic proof.
- Provenance-sensitive mechanisms never infer hidden identities.
- This evidence proves only the standalone package, not integration into NEXY runtime.
