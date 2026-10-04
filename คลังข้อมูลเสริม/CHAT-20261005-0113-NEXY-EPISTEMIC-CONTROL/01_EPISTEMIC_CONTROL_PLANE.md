# NEXY Epistemic Control Plane
Status: AI-PROPOSED-CONCEPT
Authority: non-authoritative design proposal.

## Problem
Large agent systems fail not only because reasoning is wrong, but because they lose track of why a statement is believed. A claim can be copied until provenance disappears, stale evidence can masquerade as current truth, and repeated AI outputs can create artificial consensus.

## Proposed model
Every operational claim is represented as a Claim Envelope:
- claim_id: stable identifier
- proposition: normalized statement
- status: FACT | ASSUMPTION | UNKNOWN | NOT_VERIFIED | DISPUTED
- source_class: user_spec | project_file | official_doc | tool_result | external_verified | inference
- evidence_refs: immutable references
- observed_at / valid_from / valid_until
- confidence: calibrated probability or bounded ordinal
- scope: where the claim applies
- dependencies: claims required for this claim
- contradiction_set: known incompatible claims
- owner: component responsible for refresh
- mutation_policy: who may change status

## Core invariants
E1. FACT requires direct evidence.
E2. AI repetition never upgrades authority.
E3. Derived claims retain dependency lineage.
E4. Expired evidence cannot silently remain current.
E5. Contradictions remain visible until resolved.
E6. UNKNOWN must survive retrieval and summarization.
E7. Confidence cannot replace evidence.
E8. A summary may compress wording, never authority.

## Control-plane services
Claim Registry; Evidence Ledger; Contradiction Resolver; Freshness Engine; Confidence Calibrator; Decision Trace Store; Unknown-Preservation Gate; Provenance Query API.

## Failure behavior
If provenance is missing, downgrade to NOT_VERIFIED.
If evidence is stale, mark STALE and request refresh.
If sources conflict, preserve both and create DISPUTED state.
If a dependency becomes invalid, recursively invalidate dependent decisions.
