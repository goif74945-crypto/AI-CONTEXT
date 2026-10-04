# Recovery Recipe Distiller — Design

STATUS: PROPOSED_BY_AI / STANDALONE PROTOTYPE

## Objective
Promote repeated, evidence-backed repair experience into reusable recovery recipes without treating a single successful repair as universal truth.

## Inputs
Failure episodes with subsystem, error type, symptoms, root cause, repair steps, verification tests, outcome and evidence IDs.

## Publication gate
A recipe is emitted only when:
- at least `min_successes` PASS episodes exist for the same canonical key;
- successful episodes contain evidence IDs;
- there is at least one stable repair-step sequence shared across successful episodes;
- confidence reflects both success and failure counts.

## Invariants
- failed attempts are retained as confidence penalties;
- recipe provenance lists evidence IDs;
- output ordering is deterministic;
- no recipe is emitted from insufficient evidence.

## Evidence target
E2 tests cover thresholding, failure penalty, stable step extraction and matching.
