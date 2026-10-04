# Adoption Gates for NEXY

**Status:** `AI-PROPOSED / NOT CURRENT NEXY REQUIREMENTS`

This standalone tool should not be wired into a real NEXY release path merely because its unit tests pass. Promotion should require all gates below.

## A. Authority gate

- Explicit owner approves the capability and its semantic role.
- Confirm whether freeze explanation is advisory, user-facing, JUDGE-facing, or release-authoritative.
- Resolve whether project status `PARTIAL` is modeled as decomposed leaves or supported directly in a later schema.

## B. Contract gate

- Versioned input/output schema.
- Canonical evidence IDs mapped to authoritative requirement/evidence registry.
- Explicit definition of hard FAIL vs unresolved evidence.
- Explicit repair-cost authority and units, or removal of cost ranking from authoritative surfaces.

## C. Correctness gate

- Property-based tests over generated monotone formulas.
- Independent oracle/model checker for bounded formulas.
- Regression corpus for stale evidence, conflicting authority, thresholds, duplicate leaf references, and deeply nested gates.
- Deterministic output across supported runtimes/platforms.

## D. Security gate

- Fuzz malformed JSON and pathological gate shapes.
- Verify depth/node/search caps cannot be bypassed.
- Verify inert metadata/remediation cannot trigger execution or injection into downstream renderers.
- Enforce data classification if certificates contain sensitive evidence metadata.

## E. Integration gate

- Adapter tests from canonical NEXY evidence registry.
- Exact-revision linkage tests.
- JUDGE/release-path integration tests if used there.
- UI/E2E test that freeze reasons cannot be mistaken for authorization.

## F. Operational gate

- Metrics for evaluation size, truncation rate, invalid-input rate, certificate drift, and repeated blocker cores.
- Alert on truncation when downstream policy expects complete repair alternatives.
- Retention/version policy for certificates.
- Replay test against historical certificates.

## G. Release gate

Only after the appropriate evidence class for the actual integration target is met. Local unit tests in this folder are not E3/E4/E5/E6 proof for NEXY itself.
