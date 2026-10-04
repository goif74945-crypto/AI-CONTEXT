# Adversarial Scenario Catalog
Architecture probes, not claims about current NEXY.AI.
1. Semantic alias collision: same status word means different lifecycle states. Reject incompatible contracts.
2. Time-travel cache: source revision changes before TTL. Dependency revision invalidates cache.
3. Authority laundering: retrieved text claims project-law status. Content cannot elevate authority.
4. Partial tool success: 7/10 durable targets mutate. Return PARTIAL_RESULT plus per-target receipts.
5. Retry duplication: timeout after write. Idempotency prevents duplicate side effect.
6. Capability disappearance: required provider behavior vanishes. Negotiation blocks/reroutes; no silent downgrade.
7. Conflicting fresh sources: equal authority disagrees. Emit CONFLICT and freeze dependent mutation.
8. Evidence drift: mutable citation path changes. Revision/hash mismatch invalidates evidence.
9. Replay contamination: replay calls live service. Policy blocks live side effects; recorded fixtures used.
10. Unknown coercion: UNKNOWN mapped to false/zero/empty. Exhaustive handling rejects coercion.
11. Cross-tenant provenance leak: raw sensitive lineage exposed. Protected references and data-class policy block it.
12. Concurrent writers: agents write from different heads. Optimistic concurrency detects conflict; refresh before retry.
13. Model migration: schema valid but undocumented semantics differ. Conformance fixtures catch it.
14. Poisoned summary: summary omits protected scope. Authoritative task contract wins.
15. Clock ambiguity: timestamp lacks zone. Contract rejects it.
16. Future enum: old consumer sees unknown state. Fail closed instead of defaulting.
## Evidence
Each scenario records fixture, expected/observed transition, side effects, receipts, trace IDs, PASS/FAIL, and exact revisions.
