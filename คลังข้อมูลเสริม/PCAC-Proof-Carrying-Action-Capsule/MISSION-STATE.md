# PCAC Mission State — Superseded Design Record

- mission_id: AICTX-PCAC-20261005T0143+07
- platform_chat_id: UNKNOWN_NOT_EXPOSED_TO_ASSISTANT
- persistence_mode: DURABLE_RESUMABLE
- repository: goif74945-crypto/AI-CONTEXT
- branch: main
- status: SUPERSEDED_DURING_DESIGN
- concept_authority: AI_PROPOSED_CONCEPT_ONLY
- superseded_by: ../RIPPLE-Revision-Impact-Proof-Lineage-Engine/MISSION-STATE.md
- protected_scope: every repository whose name contains NEXY.AI
- checkpoint: CP-0002-CONCEPT-REVISION

## Original objective
Design a proof-carrying action capsule for NEXY-compatible evidence transport.

## Work performed before revision
- Read AI-CONTEXT execution/rules/project overview/current build matrix.
- Built a local, uncommitted TypeScript PCAC reference validator.
- Iterated through typecheck, negative tests, malformed-input corpus, and performance checks.
- Local latest PCAC verification before supersession: strict typecheck PASS, 27/27 tests PASS, malformed corpus PASS.
- Local benchmark observation on this container: 100 claims ≈ 5.5 ms, 1,000 ≈ 24.7 ms, 5,000 ≈ 96.7 ms. These are environment-specific observations, not SLA.

## Why it was superseded
Deep NEXY context establishes overlapping current/future concepts:
- DOC-C already defines first-class Evidence objects with source/content/hash/verification metadata.
- SystemEnvelope may carry integrity body hash/schema version.
- Constitutional design includes signed/sealed operation bundles and strong build/spec/version binding.
- DOC-E already requires evidence to bind exact commit/environment.

Persisting PCAC as the primary new system would therefore risk duplicating existing NEXY concepts instead of adding a clearly missing capability.

## New gap selected
The inspected current deep context mentions dependency/test impact review and exact-version evidence, but no explicit central mechanism was found in the inspected scope for:
- transitive evidence invalidation after a revision;
- preserving unaffected evidence while invalidating only impacted proof;
- deterministic reason chains from changed node -> stale evidence -> reopened claim;
- minimal deduplicated revalidation plan;
- freeze escalation when a blocking claim loses required fresh evidence.

That gap is now pursued as RIPPLE.

## Mutation record
No NEXY.AI repository was modified. PCAC source code was not committed to AI-CONTEXT; only this mission/provenance record and the supplemental index were persisted.

## Stop condition
PCAC is frozen as a superseded concept unless explicitly revived by future authority.
