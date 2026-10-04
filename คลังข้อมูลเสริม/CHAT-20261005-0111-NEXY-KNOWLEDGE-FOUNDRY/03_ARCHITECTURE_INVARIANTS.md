# Architecture Invariants for Future NEXY.AI Work

These are decision guards, not claims about the current implementation.

## Identity
Every durable entity needs a canonical identifier, explicit lifecycle, and collision strategy.

## Contracts
Boundaries expose versioned contracts. Consumers must not depend on undocumented internal shape.

## State
Authoritative state has one declared owner. Caches and projections are derived and disposable.

## Failure
External dependencies are fallible. Timeouts, retries, idempotency, backoff, circuit breaking, and partial-failure semantics are deliberate.

## Security
Trust boundaries are explicit. Least privilege applies to agents, services, plugins, tokens, storage, and automation.

## Observability
Critical operations emit enough evidence to reconstruct what happened without exposing secrets.

## Compatibility
Migrations define forward compatibility, backward compatibility, rollback window, and mixed-version behavior.

## AI-specific
Model output is untrusted input until validated. Tool permissions are narrower than reasoning scope. Retrieval provenance is preserved. Completion requires verification evidence.

## Change impact card
For major changes record: invariant touched, contracts affected, migration, new failure modes, security boundary changes, observability, rollback, and verification gates.
