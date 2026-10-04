# Future System Concepts
Every item below is **AI-PROPOSED CONCEPT — NOT AUTHORITATIVE — NOT IMPLEMENTED — NOT VERIFIED**.

## 1. Evidence Time Machine
Reconstruct exactly what the system could legitimately know at a historical instant, excluding evidence created later. Useful for incident review and avoiding hindsight bias.

## 2. Proof Obligation Compiler
Translate a semantic change proposal into a machine-readable list of evidence obligations based on change radius, affected contracts and authority.

## 3. Assumption Kill-Switch
Maintain explicit assumptions with invalidation triggers. When an assumption is disproven, automatically mark dependent decisions/evidence as needing revalidation rather than silently retaining them.

## 4. Semantic Drift Radar
Compare meaning across evolving specs, schemas, UI labels and operational behavior. Detect “same word, different meaning” and “different word, same contract” cases.

## 5. Negative Knowledge Vault
Store verified statements about what is NOT true or NOT supported, with scope and freshness bindings. This prevents future agents from repeatedly rediscovering disproven interpretations.

## 6. Decision Rehearsal Sandbox
Before a high-radius decision, simulate the decision packet against historical failure fossils and hypothetical invalidators. Output proof obligations, not predictions presented as facts.

## 7. Context Entropy Monitor
Detect when a project context accumulates duplicates, contradictory authority, stale evidence, orphan records and unbounded terminology. Entropy findings trigger curation, never automatic deletion of authoritative history.

## 8. Unknown-to-Evidence Planner
Given blockers, rank candidate evidence-gathering actions by how many critical unknowns they could retire, while respecting cost, risk and protected scope.

## 9. Evidence Supply Chain
Track evidence provenance from source observation through normalization, test execution, artifact production, signoff and release claim. A broken link invalidates only dependent claims, not unrelated facts.

## 10. Reversibility Envelope
For each proposed mutation, define the last safe rollback point, required retained state, rollback proof and conditions after which reversal becomes destructive or impossible.

## Promotion rule
None of these concepts may become NEXY law merely because they are useful. Promotion requires authoritative approval, conflict analysis, architecture integration, implementation, tests and evidence.
