# Failure Injection Atlas
Status: AI-PROPOSED CONCEPT

Purpose: design failure experiments before failures design the product for us.

## Fault dimensions
Input: malformed, contradictory, incomplete, stale, oversized, adversarial, duplicated, reordered.
Authority: conflicting laws, stale policy, missing owner, forged provenance, privilege race.
Agent/model: timeout, fabricated tool result, schema drift, refusal, partial output, inconsistent retry, context loss.
Tool/provider: rate limit, auth expiry, partial success, delayed consistency, duplicate execution, changed API, outage.
State/storage: lost checkpoint, stale cache, split-brain, partial write, corrupt index, clock skew, orphan artifact.
Orchestration: deadlock, livelock, retry storm, circular delegation, quorum ambiguity, judge unavailable, cancellation race.
Security: prompt injection, exfiltration attempt, tool escalation, confused deputy, replay.
Human boundary: ambiguous approval, destructive ambiguity, contradictory follow-up, abandoned session.

## Experiment card
Record target invariant, injected fault, expected safe state, forbidden outcome, oracle, evidence class, recovery expectation, cleanup and residual unknowns.

## Composite scenarios
1. Provider timeout + stale policy + retry.
2. Two agents produce valid but mutually exclusive plans.
3. Tool reports success but postcondition is absent.
4. Checkpoint exists but source changed afterward.
5. Human approval arrives after task state became stale.
6. Partial mutation occurs before cancellation.
7. Judge crashes after worker side effect but before acknowledgement.
8. Same request replayed after external state changed.

These are proposed tests, not claims about current NEXY implementation.
