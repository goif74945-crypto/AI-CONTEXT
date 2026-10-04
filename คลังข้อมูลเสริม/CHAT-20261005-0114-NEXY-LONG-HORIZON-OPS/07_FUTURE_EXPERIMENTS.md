# Future Experiment Registry
All entries are AI-PROPOSED CONCEPTS, NOT REQUIREMENTS.

## EXP-01 Context Freshness Linter
Test whether source-bound invalidation reduces stale-context errors. Stop if current authoritative context is falsely invalidated.

## EXP-02 Dependency Authority Graph
Map dependency deltas → affected invariants → minimum defensible regression suite. Stop on any missed critical regression.

## EXP-03 Bounded Agent Cost Envelope
Test explicit resource budgets against runaway fan-out/retry. Stop if enforcement causes fabricated or partial success.

## EXP-04 Migration State Machine Checker
Statically detect missing rollback, dual compatibility, cutover and cleanup gates. Stop if a known unsafe plan passes.

## EXP-05 Proposal Authority Guard
Ensure retrieval cannot rank PROPOSAL_AI above conflicting authoritative project facts.

## EXP-06 Reliability Budget Simulator
Simulate failure rate/blast radius and verify hard invariant violations always FREEZE/BLOCK rather than consume ordinary error budget.
