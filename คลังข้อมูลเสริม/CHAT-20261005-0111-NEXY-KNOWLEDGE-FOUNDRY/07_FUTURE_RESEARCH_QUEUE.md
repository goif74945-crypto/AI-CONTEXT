# Future Research Queue

This queue avoids assuming current NEXY.AI implementation.

1. Context compiler: compile authoritative context into minimal task packets with provenance and conflict detection.
2. Evidence graph: claims as nodes, sources/tests as edges, freshness and contradiction propagation.
3. Capability firewall: separate what an agent may reason about from what it may mutate.
4. Reversible execution ledger: pair mutations with pre-state, post-state, verification, and rollback.
5. Failure-memory engine: cluster root causes and inject prevention rules into future work packets.
6. Contract intelligence: detect API/schema drift before runtime integration failure.
7. Eval synthesis: derive adversarial tests from requirements, invariants, and historical failures.
8. Uncertainty budget: prevent chains of weak assumptions from enabling high-impact actions.
9. Context entropy metrics: measure duplicated, stale, contradictory, and low-value knowledge.
10. Evidence-weighted multi-agent resolution: avoid majority-vote fallacy.

## Graduation rule
A track leaves IDEA only when the problem is evidenced, current gap verified, mechanism falsifiable, risks documented, evaluation designed, and integration/rollback understood.

## Priority heuristic
Priority = expected reuse × failure-cost reduction × evidence quality ÷ integration complexity.
Do not invent numeric precision when inputs are not measurable.
