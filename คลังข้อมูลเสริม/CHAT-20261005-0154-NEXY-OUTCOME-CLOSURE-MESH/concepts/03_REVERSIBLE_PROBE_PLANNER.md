# Concept 3 — Reversible Probe Planner
AI-PROPOSED / NON-GOVERNING

**Problem:** an agent often knows what fact is missing but can choose an evidence-gathering action whose side effect is riskier than the uncertainty.

**Contract:** candidate probes declare what they resolve, cost, effect class, authority requirement, and rollback for reversible writes.

**Core invariant:** irreversible probes are never selected. Exact optimization occurs only inside a bounded candidate domain; outside that domain the planner blocks rather than lying about minimality.

**Why it can help NEXY:** it creates a deterministic bridge from UNKNOWN to a *safe proposed way to obtain evidence* while keeping execution authority outside the planner.

**Implementation:** `src/reversible_probe.ts`.
**Tests:** `tests/reversible_probe.test.mjs`, authority/budget/tie-break adversarial tests, integration test.
**Evidence:** final direct test record and demo.
