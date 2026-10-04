# Promotion Gates

This lab is advisory. None of it should enter current NEXY build scope without explicit promotion.

## Gate P0 — Authority
PASS requires an explicit authorized decision to adopt the checker or a derivative.

## Gate P1 — Contract mapping
Map proposal fields to current canonical backend/UI contracts at the exact target revision.
Unknown mappings remain UNKNOWN; do not shim by guessing.

## Gate P2 — Renderer adapter
Build a read-only adapter that converts actual renderer output into a truth-surface manifest without changing renderer behavior.

## Gate P3 — Accessibility capture
Prove that accessibility semantics are captured from the actual accessibility tree, not copied from visual props.

## Gate P4 — Role/authorization mapping
Compare visible actions with real backend authorization policy. UI visibility remains non-authoritative.

## Gate P5 — Release-proof mapping
Replace the proposal's three-field release heuristic with the exact current release contract or a signed/verified release token.

## Gate P6 — Localization semantic review
State truth must survive every supported locale. Token matching alone is insufficient for production.

## Gate P7 — Browser/E2E evidence
Run real browser flows for READY/RUNNING/VERIFYING/CONSENSUS/STABLE/FREEZE/STOP and role permutations.

## Gate P8 — Regression integration
Add conformance cases to the real CI gate with exact-version evidence and deterministic fixtures.

## Gate P9 — False-positive budget
Measure legitimate UI variants rejected by the checker. A gate that always screams is merely an automated colleague from a bad meeting.

## Gate P10 — Versioning
Version:
- input manifest schema;
- invariant catalog;
- semantic-copy rules;
- adapters;
- certificates.

Any breaking semantic change requires migration and revalidation.
