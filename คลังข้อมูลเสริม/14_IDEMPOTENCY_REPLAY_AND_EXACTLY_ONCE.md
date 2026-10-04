# Idempotency, Replay, and Exactly-Once Illusions
Status: PROPOSAL / AI-PROPOSED CONCEPT
Authority: ADVISORY ONLY

## Problem
Distributed and agentic workflows retry. A retry can duplicate a payment, write, deployment, message, permission change, or canonical decision unless identity and replay semantics are explicit.

“Exactly once” is often an end-to-end property that cannot be obtained merely by a queue setting.

## Action envelope
For side effects, consider:
action_id
intent_hash
authority_id
actor/capability
target
precondition_hash
idempotency_key
created_under_source_identity
expiry/invalidation rule
attempt
parent_action
expected_effect_hash
result_receipt

## Semantics
AT_MOST_ONCE: duplicate suppression prioritized; loss may occur.
AT_LEAST_ONCE: retry prioritized; duplicates possible.
EFFECTIVELY_ONCE: retries allowed but effect is deduplicated by stable action identity and state preconditions.
EXACTLY_ONCE: claim only when the full boundary can prove it.

## Replay rule
A replay must not rely only on matching request bytes. It must verify that authority, preconditions and target state remain compatible with the original intent.

## ABA problem
State can change A -> B -> A. Comparing only current value A can falsely imply nothing changed. Use version/epoch/content identity where required.

## Duplicate conflict
Same idempotency key + different intent hash => SECURITY/INTEGRITY CONFLICT, never “last write wins.”

## Retry matrix
- read: normally retryable under freshness contract
- reversible write: retry with idempotency + precondition
- irreversible external action: require durable receipt/reconciliation
- canonical emit: stable identity and single-commit semantics
- permission change: revalidate authority on retry
- delayed queued action: revalidate expiry and governing policy

## Recovery
After ambiguous timeout:
do not assume failure.
Query authoritative side-effect state or receipt first.
If effect cannot be determined and duplication is dangerous -> FREEZE/manual reconciliation.

## Tests
- timeout after server commit before client receipt
- duplicate delivery
- reordered retries
- same key different payload
- expired authority
- target changed between attempts
- partial multi-resource commit
- replay after rollback

## Future value
This model is especially useful anywhere NEXY agents or workflows cross from deterministic reasoning into external side effects.
