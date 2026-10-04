# Design — Minimal Failure Witness Reducer (MFWR)

Classification: `AI_PROPOSED_CONCEPT / REFERENCE_IMPLEMENTATION`

## Problem
Large failing traces are expensive to understand and easy to misdiagnose. Existing verification can prove that a scenario fails, but a human or downstream repair agent still needs the smallest reproducible witness. A reducer must not hide nondeterminism by treating an unstable oracle as a valid proof.

## Contract
MFWR accepts an ordered JSON-compatible sequence and a trusted deterministic failure oracle supplied by the integrating test harness.

1. The full input must reproduce the failure.
2. Every candidate oracle result is checked twice. A disagreement is `ORACLE_UNSTABLE` and aborts reduction.
3. A deterministic ddmin-style coarse pass removes large chunks.
4. A final single-element elimination pass guarantees **1-minimality**: removing any one remaining element no longer reproduces the failure.
5. A hard evaluation budget prevents unbounded work. Budget exhaustion is explicit, never reported as success.

## Output
- minimal witness sequence;
- original/reduced lengths;
- oracle evaluation count;
- stable content fingerprints;
- `ONE_MINIMAL` status.

## Why this is distinct
This system does not generate test spaces, mutate contracts, prove interleavings, or classify provenance. It post-processes an already reproducible failure into a smaller exact witness.

## Integration proposal
Useful after NEXY-compatible verification, fuzzing, scenario generation, replay or interleaving analysis. The integration adapter owns the real failure oracle and evidence class. MFWR itself does not execute arbitrary user code from data files.
