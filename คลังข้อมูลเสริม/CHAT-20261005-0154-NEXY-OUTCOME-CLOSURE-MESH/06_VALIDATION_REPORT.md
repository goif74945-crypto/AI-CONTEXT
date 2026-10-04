# Validation Report

Status: LOCAL_REFERENCE_IMPLEMENTATION_VERIFIED
Scope: this isolated NOCM reference project only

## TDD evidence
1. `evidence/01_RED.txt`
   - Initial tests existed before product source.
   - Build failed on missing source modules and initial Node test typing harness.
2. `evidence/02_RED_HARNESS_FIXED.txt`
   - Test harness moved to `.mjs` while product source remained absent.
   - Build failed because `src/**/*.ts` did not exist, establishing a clean source-missing RED state.
3. Product source was then implemented.

## GREEN evidence
- Initial implementation run: all 21 original unit/integration tests passed.
- Adversarial suite was added to verify already-declared safety/determinism invariants.
- Final direct run: 33 tests, 33 pass, 0 fail, 0 skipped, 0 cancelled.

## Test distribution
- Adoption Readiness: base readiness, protected mutation, collision, rollback.
- Outcome Closure: closure, evidence deficit, forbidden trigger, order determinism.
- Progress Truth: complete, unknown, blocked priority, empty set.
- Reversible Probe: exact minimum-cost safe cover, irreversible rejection, rollback requirement, ready path.
- Benefit Regression: improvement, critical regression, missing metric, unchanged candidate.
- Adversarial: malformed identities/thresholds, unknown forbidden state, authority deficit, budget proof, tie-break determinism, compatibility fail/unknown, missing evidence, order-invariant readiness fingerprint.
- Integration: all five modules compose into human-review readiness with automatic promotion disabled.

## Toolchain observed
- Node: v22.16.0
- npm: 10.9.2
- TypeScript compiler available in environment: 5.8.3
- Project dependencies: none

## Evidence classes
- E0: source/docs/tests/evidence files exist locally; remote E0 requires GitHub readback.
- E1: TypeScript build executed successfully as part of tests.
- E2: unit and adversarial tests executed successfully.
- E3: integration test and executable demo executed successfully.
- E4+: NOT CLAIMED. No NEXY runtime integration, production deployment, or release evidence exists.

## Important limitation
The deterministic 64-bit fingerprints are non-cryptographic. Security/provenance integrations must continue using NEXY's authoritative evidence hash requirements rather than substituting these fingerprints.
