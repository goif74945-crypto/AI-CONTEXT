# Temporal Truth and Validity Model for NEXY.AI
Status: PROPOSAL / AI-PROPOSED CONCEPT
Grounding: FACT_PROJECT + engineering inference
Authority: ADVISORY ONLY

## Why this exists
A value can be correct and still be unusable because its validity interval, source identity, policy version, or dependency state changed. NEXY already distinguishes exact execution evidence from historical evidence. This proposal generalizes that idea into a temporal truth model.

## Core distinction
Do not store only value=true/false. Store:
- proposition
- authority
- observed_at
- valid_from
- valid_until or invalidation predicate
- source identity
- policy/spec version
- dependency set
- evidence pointer
- confidence is metadata, never authority
- supersession link
- verification state

## Validity is dependency-based
PROPOSAL: a fact remains admissible while its invalidation predicate is false. Wall-clock age alone is insufficient.

Example:
A compiler proof from yesterday may remain valid if source, toolchain, flags, inputs and governing contract are unchanged.
A proof from 30 seconds ago is invalid if the source tree changed.

## Temporal states
CURRENT_VERIFIED
CURRENT_UNVERIFIED
HISTORICAL_VERIFIED
SUPERSEDED
STALE_DEPENDENCY
FUTURE_NOT_EFFECTIVE
CONFLICTING_INTERVAL
UNKNOWN_VALIDITY

## Bitemporal model
Use two time axes where useful:
1. valid time: when the proposition applies to the modeled world.
2. transaction/knowledge time: when NEXY learned or recorded it.

This prevents retroactive edits from erasing what the system believed at an earlier decision point.

## Decision rule
An action may consume a proposition only when:
- governing authority is valid,
- source identity matches required scope,
- validity interval contains the decision point,
- dependencies remain valid,
- no higher-authority supersession exists,
- required evidence is available.

Otherwise FREEZE or request refresh according to contract.

## Test corpus
- old proof + identical dependency graph => may remain admissible
- new proof + changed source SHA => reject
- policy becomes effective tomorrow => do not apply today
- two overlapping authoritative policies disagree => CONFLICT/FREEZE
- retroactively corrected record => historical decision reconstruction still possible
- missing timezone/clock authority => do not infer temporal order when order is safety-critical

## Project grounding
FACT_PROJECT observed read-only:
- scripts/evidence-attestation.ts states runtime release evidence is bound to an exact CI execution.
- historical evidence/.seal.json is explicitly not deployment authorization.
- queue code can fail when time authority is unavailable.
These support, but do not mandate, the generalized model above.

## Acceptance criteria for future adoption
- deterministic evaluation for identical temporal inputs
- explicit invalidation reason
- reconstructable historical decision
- no wall-clock freshness heuristic can override dependency identity
- temporal ambiguity produces explicit failure, never guessed ordering
