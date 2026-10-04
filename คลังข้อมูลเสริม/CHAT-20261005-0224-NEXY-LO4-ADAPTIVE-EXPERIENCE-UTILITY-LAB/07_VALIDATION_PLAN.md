# Validation Plan

## E0 Presence
After publication, read back all final source/test/design/evidence files from the exact AI-CONTEXT revision and compare Git blob identities against the tested local bytes.

## E1 Static
- `python3 -m compileall -f -q aeul tests`.
- AST assertion: no float literals or `float()` calls in decision modules.
- standard-library-only package metadata.

## E2 Unit/adversarial
Run full unittest discovery under at least two `PYTHONHASHSEED` values.

Required proof includes:
- Q64.64 signed boundaries/overflow/divide-by-zero/half-even behavior;
- independent Fraction-oracle random multiply/divide checks;
- every engine's positive + negative path;
- missing/conflicting evidence paths;
- deterministic ordering/fingerprint tests.

## E3-lab Integration
Execute end-to-end local ICF flow from utility selection through bounded pilot planning. This is standalone component integration only, not NEXY product integration.

## Stress
Fixed-seed deterministic stress:
- 10,000 IURS cases;
- 3,000 DCPX cases.

## Replay
Normalize timing-only text and require the complete seed-1 and seed-777 unittest reports to be byte-identical.

## Publication seal
For every final source/test file:
1. compute local Git blob SHA;
2. fetch the file at the final publication commit;
3. compare connector-reported Git blob SHA;
4. mismatch => `NOT_VERIFIED` and no COMPLETE claim.

## Out of scope evidence
E4 user/product flow, E5 production runtime, E6 deployment and E7 physical evidence remain `NOT_VERIFIED` / not claimed.
