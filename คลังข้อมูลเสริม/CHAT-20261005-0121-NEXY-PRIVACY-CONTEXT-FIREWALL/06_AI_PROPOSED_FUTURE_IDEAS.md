# AI-Proposed Future Ideas

> Every item in this file is `AI_PROPOSED_FUTURE_CONCEPT`. None is canonical NEXY scope unless separately promoted by human/project authority.

## F1. Privacy Type System

Attach privacy types to Vault objects and derived artifacts so transformations can only preserve or increase restrictiveness unless an authorized declassification rule exists.

Potential invariant:
`derived_classification >= max(source_classifications)` unless an explicit declassification proof is attached.

## F2. Purpose Capability Tokens

Replace free-form purpose strings with signed, short-lived capability tokens stating:
- task identity;
- allowed purposes;
- allowed field namespaces;
- destination set;
- expiry;
- authority issuer.

This would make "purpose" harder to alter accidentally between planner and provider adapter.

## F3. Disclosure Budget

Give a task a finite privacy budget measured by fields/classes/semantic categories. Each external egress consumes budget, and retries cannot silently resend additional context without a new decision.

This is not differential privacy. It is an operational disclosure-accounting primitive.

## F4. Derived-Data Taint Graph

Track which outputs were derived from protected inputs. A sanitized summary may still carry sensitive facts even after original raw values disappear. Taint propagation could stop a later agent from treating derived text as public merely because the source field is gone.

## F5. Provider Privacy Attestation Registry

Maintain time-bounded, evidence-backed provider profiles. A profile could become stale when:
- terms/configuration change;
- retention setting changes;
- region changes;
- enterprise/privacy mode expires;
- API version changes.

Stale provider evidence would force re-admission instead of inheriting trust forever.

## F6. Semantic Minimum-Necessary Solver

A future verifier could prove that a declared field set is sufficient but not obviously excessive for a task contract. This should be advisory until deterministic evidence is strong enough, because letting an LLM be the final judge of what private data it deserves is a wonderfully circular failure mode.

## F7. Privacy Chaos Tests

Inject synthetic canary secrets and personal records into controlled contexts, then test that routing, retries, logs, traces, caches, and fallback providers never surface them outside authorized boundaries.

## F8. Revocation and Tombstone Propagation

When a field loses authorization or is deleted, emit revocation events to derived caches, embeddings, audit indexes, and task snapshots. Record proof of propagation rather than assuming deletion from one primary store means deletion everywhere.

## F9. Dual-Control Declassification

High-risk declassification (`SECRET -> INTERNAL`, etc.) could require two independent authorities or a human approval plus machine evidence, with a signed decision record.

## F10. Privacy-Safe Observability Projection

Generate telemetry from policy metadata and receipt IDs, not raw context. Observability would answer "why did this freeze?" without turning traces into a second ungoverned Vault.
