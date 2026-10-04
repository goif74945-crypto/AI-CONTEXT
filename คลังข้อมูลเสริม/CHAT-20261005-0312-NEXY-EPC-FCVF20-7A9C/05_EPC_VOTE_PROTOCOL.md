# EPC Vote Protocol Contract

## Vote rights

For one durable `CHAT_ID`, the lifetime budget is exactly one KEEP round and one CUT round. DEFER, WIP and INSUFFICIENT_EVIDENCE do not consume either right. A revision never restores a spent right.

## Preconditions

A KEEP or CUT receipt requires exact authoritative spec evidence, exact NEXY code evidence, current AI-CONTEXT evidence and executed test evidence. CUT additionally requires `READY`; WIP or INSUFFICIENT_EVIDENCE cannot be transformed into CUT merely because the candidate looks weak.

## Immutable history

A base vote receipt is immutable. Later information is represented as an append-only revision referencing the base `VOTE_ID`. A revision whose purpose is to change the prior verdict is rejected. A different later governance decision must be represented by whatever formally authorized process exists outside this experimental package; FCVF does not invent extra vote rights.

## CUT semantics

CUT is a logical disposition only: `ARCHIVED`, `REJECTED`, or `SUPERSEDED`. It never means file deletion, Git deletion, history rewrite or evidence destruction. This preserves auditability and permits later reassessment without falsifying history.

## Duplicate law

A duplicate claim requires a concrete semantic target and witness. Filename, acronym, title or vague similarity is insufficient. FCVF stores duplicate evidence as evidence; it does not convert a similarity claim directly into CUT.

## Authority law

KEEP/CUT is advisory proposal-court state. It cannot override NEXY Canon/LAW/JUDGE, cannot mutate Core state, and cannot automatically promote a candidate. Numeric metrics are protocol-integrity metadata and cannot compensate for a hard constitutional failure.

## Required receipt fields

The executable `VoteRecord` materializes the user-required fields: `VOTE_ID`, `CHAT_ID`, `ROUND`, `TIMESTAMP`, `SPEC_ID`, `SPEC_HASH`, `NEXY_REPO`, `NEXY_BRANCH`, `NEXY_COMMIT_SHA`, `AI_CONTEXT_COMMIT_SHA`, `CANDIDATE_ID`, `CANDIDATE_PATH`, `STATUS_BEFORE`, `VERDICT`, `SPEC_EVIDENCE`, `CODE_EVIDENCE`, `AI_CONTEXT_EVIDENCE`, `ARCHITECTURE_FIT`, `CANON_COMPATIBILITY`, `NOVELTY`, `OVERLAP`, `IMPLEMENTATION_VALUE`, `VERIFICATION_VALUE`, `SECURITY_IMPACT`, `DETERMINISM_IMPACT`, `MAINTENANCE_COST`, `CONFLICTS`, `DUPLICATES`, `DEPENDENCIES`, `FACT`, `ASSUMPTION`, `UNKNOWN`, `REASON`, `COUNTERARGUMENT`, and `FINAL_JUSTIFICATION`. Test `test_vote_record_contract.py` verifies that mapping.

## Numeric interpretation

Q64.64 fields in FCVF are deliberately restricted to evidence/protocol-integrity quantities. FCVF does not pretend it can derive objective "novelty" or "maintenance cost" from thin air; those fields are held at neutral zero in the reference engine rather than populated with invented precision. Hard compatibility/security/determinism invariants are non-compensatory.
