# Adoption Gates

Status: `AI_PROPOSED_CONCEPT_NOT_ADOPTED`

This lab must not become production law merely because code exists and tests pass.

## Gate A — Product authority
Authorized NEXY authority explicitly decides whether localization integrity is a current product requirement and names the governed surfaces.

## Gate B — Language ownership
A qualified owner defines supported language pairs, terminology, and protected control vocabulary. The reference EN/TH regexes are not enough by themselves.

## Gate C — False-positive/false-negative study
Run a representative corpus of real product/control text. Measure missed critical drift and unnecessary freezes. Zero known critical semantic escape is required for the claimed protected classes.

## Gate D — Integration contract
Define where the gate runs, which revision/policy it binds to, how source and target provenance are sealed, and whether failure blocks publish, build, or runtime display.

## Gate E — Security review
Verify inputs cannot bypass extraction with encoding tricks, hidden Unicode, markup, placeholder variants, or parser differentials.

## Gate F — Performance envelope
Benchmark realistic batch sizes and payload lengths. Define bounded runtime/memory and deterministic exhaustion behavior.

## Gate G — User experience
FREEZE copy must explain the exact protected invariant that changed and the next legal action without pretending the translation itself is globally wrong.

## Gate H — Evidence
Production adoption needs appropriate integration/E2E evidence at the exact NEXY revision. This lab's E2 tests are not evidence of NEXY runtime integration.
