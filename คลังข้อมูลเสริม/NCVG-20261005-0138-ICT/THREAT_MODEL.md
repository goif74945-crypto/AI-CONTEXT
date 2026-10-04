# NCVG Threat Model

> **AI proposal. Security properties are limited to those explicitly tested.**

## Assets
- integrity of verification decision;
- integrity of requirement/evidence linkage;
- protected mutation boundary;
- reproducible bundle identity.

## Failure sources
- fabricated PASS evidence;
- stale evidence reused from another commit;
- missing evidence references;
- execution marked PASS despite failure;
- protected-scope mutation claims;
- duplicate identifiers;
- malformed input causing caller ambiguity;
- bundle changed after review.

## Implemented controls
- evidence-ID resolution;
- status/class checks;
- exact expected-commit binding;
- duplicate-ID rejection;
- protected/forbidden target checks;
- fail-closed canonicalization;
- deterministic bundle hash;
- nonzero FREEZE exit code.

## Non-guarantees
SHA-256 is content integrity, not authentication. Mutation target strings are assertions, not independent authorization receipts. NCVG validates consistency of supplied evidence but does not independently execute every evidence claim.

Future hardening ideas are documented separately and remain proposals only.
