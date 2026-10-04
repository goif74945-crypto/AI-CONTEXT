# AI-Proposed Future Ideas

Everything in this file is **PROPOSAL**, not an NEXY.AI requirement.

## Proposal A — Intent Retention Gate
Before a long-running agent announces completion, compile the active user directives into an Interaction Contract and require all mandatory directives to carry proof references.

Potential benefit: prevents “technically did something” from being confused with “completed what the user asked.”

Failure mode: bad upstream extraction can omit a directive. Mitigation: expose the contract to a verifier and preserve provenance to the exact source message.

## Proposal B — Clarification Debt Budget
Track clarifications against directives already marked resolved. Repeated unnecessary questions increase interaction debt and can trigger a routing change to a more capable planning agent.

Potential benefit: reduces confirmation fatigue without weakening safety gates.

Failure mode: stale `resolved=true` could suppress a needed re-check. Mitigation: tie resolution to freshness/version identifiers.

## Proposal C — Scope Lease
Represent delegated mutation rights as explicit scoped leases with a target, allowed operations, and expiration/invalidating conditions.

Potential benefit: makes “tool access ≠ authorization” machine-checkable.

Failure mode: coarse scope strings could over-authorize. Mitigation: canonical scope grammar and deny-by-default matching.

## Proposal D — Completion Proof Bundle
A completion event should carry a compact map from mandatory directive IDs to evidence references, plus exact code/data identity where relevant.

Potential benefit: makes completion resumable and auditable across models.

Failure mode: evidence can go stale after mutation. Mitigation: evidence invalidation rules keyed to content identity.

## Proposal E — Interaction Regression Corpus
Store synthetic contracts for known failure classes: repeated clarification, scope drift, hidden assumption, omitted acceptance criterion, false PASS, conflicting instructions, and stale proof.

Potential benefit: allows deterministic agent-control regression testing independent of model brand.

Failure mode: corpus overfitting. Mitigation: generate variants and maintain adversarial cases separately.
