# WORKFLOW — VERIFICATION

## Goal
Prove or disprove a concrete claim with the correct evidence class.

## Procedure
1. State the claim precisely.
2. Identify target/version/environment.
3. Determine required evidence class from `rules/VERIFICATION.md`.
4. Define pass/fail invariant before running the test.
5. Execute the smallest decisive proof.
6. Capture raw result/reference.
7. Run negative/regression proof when the claim is critical.
8. Assign PASS/FAIL/PARTIAL/BLOCKED/NOT_VERIFIED/UNKNOWN/CONFLICT.
9. Record limitations.

## Claim template
- claim:
- target:
- commit/version:
- environment:
- evidence_class_required:
- test/command:
- expected:
- observed:
- status:
- artifact/log:
- limitations:

## Reproducibility
A second AI/operator should be able to rerun the proof without guessing hidden setup.

## Failure
A failing verification is useful evidence. Do not suppress it to preserve a desired narrative.
