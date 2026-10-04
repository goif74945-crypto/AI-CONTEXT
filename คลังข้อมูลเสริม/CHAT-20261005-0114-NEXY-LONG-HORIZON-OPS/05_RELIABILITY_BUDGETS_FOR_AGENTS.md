# Reliability Budgets for Agentic Work
Status: PROPOSAL_AI

## SLI families
Scope fidelity; evidence fidelity; resume fidelity; tool correctness; recovery success; staleness escape rate; side-effect duplication rate; authority-conflict escape rate.

## Zero-tolerance invariants
Some failures should have no budget: secret exposure, unauthorized protected-scope mutation, fabricated execution evidence, silent authority override.

## Budget response
When a soft SLI burns rapidly: reduce concurrency, increase verification, disable risky automation class, route to narrower workflow, investigate dominant failure.

## Anti-gaming
Do not inflate success by refusing hard tasks, shrinking denominators, blaming users without evidence, or counting generated artifacts as verified outcomes.

## Evaluation
Use adversarial suites containing ambiguous scope, stale context, tool failure, conflicting authority and retries. Score outcome and process integrity.
