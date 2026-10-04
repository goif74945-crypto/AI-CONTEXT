# Temporal Knowledge Lifecycle
> Classification: AI-PROPOSED CONCEPT. Not an authoritative NEXY.AI requirement.

## Problem
A knowledge system can be internally consistent and still be wrong because its inputs aged. Freshness is not a cosmetic timestamp. It is a correctness property that depends on what a claim describes, what evidence supports it, and which downstream decisions consume it.

## Proposed lifecycle
DISCOVERED -> CAPTURED -> VERIFIED -> ACTIVE -> AGING -> REVIEW_DUE -> STALE -> INVALIDATED -> ARCHIVED.

Transitions must be evidence-driven. Time alone may move a claim into REVIEW_DUE, but a breaking dependency can jump directly to INVALIDATED.

## Claim record
Each reusable claim should be representable as:
- claim_id
- proposition
- claim_type
- source_refs
- observed_at
- verified_at
- valid_from / valid_until when known
- freshness_policy
- dependency_claim_ids
- contradiction_set
- confidence_basis
- owner/domain
- consumers
- state
- invalidation_reason

## Freshness classes
STATIC: mathematics, historical immutable records.
SLOW: architecture principles, long-lived standards.
MEDIUM: product capabilities, SDK behavior.
FAST: prices, availability, active incidents, current policies.
EVENT_DRIVEN: validity changes only when a named dependency changes.
UNKNOWN: no safe freshness policy exists; reuse requires revalidation.

## Core invariant
No downstream artifact may claim stronger temporal validity than its weakest critical evidence dependency.

## Failure semantics
Missing timestamp -> UNKNOWN.
Missing source -> NOT VERIFIED.
Expired evidence -> STALE unless a policy explicitly proves continued validity.
Contradictory newer evidence -> INVALIDATED pending adjudication.
