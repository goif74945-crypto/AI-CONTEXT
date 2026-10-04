# Concept Proposal — Semantic Localization Integrity Gate

**Classification:** `AI_PROPOSED_CONCEPT`  
**Adoption status:** `NOT_ADOPTED`

## Problem
Localization can change operational meaning even when a sentence still looks fluent. For a control-oriented AI system, specific drift classes are disproportionately dangerous:

- "must not" becoming "should not";
- "may" becoming "must";
- a missing negation;
- `500 ms` becoming `500 s`;
- `FREEZE` being paraphrased away;
- `{artifact_id}` being renamed or dropped;
- a UUID/hash/URL/email mutating;
- an unsupported language being accepted without any deterministic semantic check.

The proposal is not a translator. It is a **translation-boundary invariant gate**.

## Hypothesis
A deterministic invariant gate placed after translation and before release can cheaply catch a useful subset of high-impact semantic drift while preserving NEXY's preference for explicit failure over guessed correctness.

## In scope
- EN and TH reference support;
- source/target pair analysis;
- protected semantic classes and literals;
- deterministic issue ordering and fingerprint;
- binary PASS/FREEZE decision;
- adversarial corpus and unit tests;
- additive research artifact only.

## Out of scope
- proving natural-language equivalence;
- ranking translation quality/style;
- machine translation;
- production UI wiring;
- runtime service integration;
- adding localization as a current NEXY requirement;
- claiming EN/TH are the only desired product languages;
- changing NEXY authority or User Law.

## Why this is intentionally narrow
Full semantic equivalence is not deterministically provable with these rules. Pretending otherwise would violate the exact integrity principle the lab is supposed to support. The gate therefore protects explicit invariants and freezes unsupported language semantics instead of generating a confidence score dressed as truth.
