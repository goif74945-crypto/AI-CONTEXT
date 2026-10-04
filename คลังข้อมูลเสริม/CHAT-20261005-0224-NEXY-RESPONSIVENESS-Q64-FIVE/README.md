# NEXY Responsiveness Without Guessing Fabric — Lo4 Q64 Five

**Status:** `Lo4_AI_PROPOSAL_ONLY`  
**Canon authority:** NONE  
**Promotion:** REQUIRED  
**Work code:** `CHAT-20261005-0224-NEXY-RESPONSIVENESS-Q64-FIVE`

This package explores making NEXY faster and calmer without buying latency improvements by deleting proof, hiding conflict, guessing, or executing speculative writes.

| # | System | User-facing target | Hard guard |
|---|---|---|---|
| 1 | AP3: Authority-Preserving Predictive Prefetch | hide retrieval latency | read-only speculation only |
| 2 | LEC: Latency Envelope Compiler | predictable latency budgets | verification minima immutable |
| 3 | PCPS: Proof Critical-Path Scheduler | decisive proof sooner | dependencies + authority preserved |
| 4 | WCRC: Warm Context Residency Controller | less repeated context reload | authority/counterevidence pinned |
| 5 | ABG: Attention Budget Governor | fewer low-value interruptions | blocker/security/conflict always surfaces |

## Numeric contract
Decision scores/probabilities/durations/budgets use signed Q64.64 with checked signed-128 raw range. No binary float literal exists in durable `src/` or `tests/`.

## Verified durable evidence
Exact code/test blobs introduced at `80cf0db8b300312b39347c5eff286a64b7365854`:
- E1 compileall PASS;
- E1 AST float scan PASS, zero float literals;
- E2 22/22 durable test methods PASS;
- E2 1,400 seeded randomized invariant iterations PASS;
- E3 isolated LEC -> WCRC -> AP3 -> PCPS -> ABG integration PASS.

A separate pre-write local suite had 34/34 tests PASS, but that number is not used as exact-commit evidence.

NEXY product integration/runtime/deployment remains **NOT_VERIFIED**. No repository whose name contains `NEXY.AI` was mutated.
