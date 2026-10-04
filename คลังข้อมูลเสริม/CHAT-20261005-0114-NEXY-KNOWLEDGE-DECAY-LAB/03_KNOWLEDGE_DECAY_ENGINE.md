# Knowledge Decay Engine
**AI-PROPOSED CONCEPT — NOT AUTHORITATIVE — NOT IMPLEMENTED — NOT VERIFIED**

## Problem
Large engineering contexts fail quietly when old evidence remains syntactically valid but semantically stale. A commit SHA, provider contract, dependency behavior, requirement interpretation, benchmark, threat assumption, or operational fact can decay at different rates. Treating all stored facts as equally fresh creates false confidence.

## Proposed model
Represent each durable claim as a Knowledge Atom:
- atom_id
- claim
- truth_class
- authority_source
- observed_at
- bound_revision/environment
- dependencies
- invalidators
- freshness_policy
- last_revalidated_at
- confidence is NOT proof
- state: FRESH | AGING | STALE | SUPERSEDED | CONFLICT | UNKNOWN

Freshness should be evidence-specific, not a single global TTL.

## Decay dimensions
1. Revision decay: code/repo changed after evidence.
2. Environment decay: runtime/provider/config changed.
3. Authority decay: newer law/spec supersedes source.
4. Dependency decay: upstream behavior/version changes.
5. Temporal decay: fact naturally expires.
6. Semantic decay: terminology/meaning changed while text stayed.
7. Coverage decay: system expanded beyond old evidence denominator.
8. Identity decay: evidence no longer binds to exact target identity.

## Proposed invalidation graph
Knowledge atoms form a dependency DAG. An invalidator does not necessarily delete downstream knowledge; it changes its status and creates revalidation obligations.

Example:
provider API contract changes
-> provider adapter assumptions become AGING
-> integration evidence becomes STALE
-> release evidence depending on it becomes NOT_VERIFIED
-> unrelated deterministic core law remains unaffected.

## Freshness policy classes
- IMMUTABLE_LAW: changes only by explicit authority.
- REVISION_BOUND: invalidated by target revision change.
- ENVIRONMENT_BOUND: invalidated by environment identity/config change.
- TIME_BOUND: expires after explicit interval.
- PROVIDER_BOUND: invalidated by provider/version/schema change.
- COMPOSITE: requires multiple bindings.
- MANUAL_REVIEW: no automatic PASS; human/authority promotion required.

## Retrieval behavior
Context retrieval should rank not just semantic relevance but:
authority × target binding × freshness × dependency validity × evidence class.
A highly relevant stale artifact must lose to a less verbose current artifact.

## Failure semantics
- missing freshness metadata -> UNKNOWN, never silently FRESH.
- invalidation cycle -> CONFLICT/FREEZE for affected claim set.
- source unavailable -> preserve last known claim as STALE/NOT_VERIFIED.
- conflicting revalidation -> retain both evidence records and block promotion.

## Value to NEXY
This supports NEXY's freeze-over-guess identity by making staleness first-class. It reduces the dangerous failure mode where old PASS evidence survives after the target has changed.

## Adoption gate
Before implementation, define canonical atom schema, invalidation semantics, migration strategy, storage cost, retrieval latency budget, and tests proving stale evidence cannot satisfy a fresh proof obligation.
