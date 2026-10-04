# Change-Impact Calculus

> PROPOSAL_AI — แนวคิดที่เสนอโดย AI ยังไม่ใช่ข้อกำหนดจริงของ NEXY.AI

## 1. Purpose
Represent a proposed mutation as a set of changed facts and derive a conservative set of potentially affected claims.

Define a change set C = {c1..cn}. Each change has:
- identity: stable path/requirement/interface/config identifier;
- change_kind: semantic | structural | dependency | policy | data | runtime | deployment;
- before_fingerprint;
- after_fingerprint;
- authority_class;
- reversibility;
- observed_at.

Define an impact graph G=(V,E), where nodes may be requirements, contracts, modules, tests, evidence, policies, schemas, runtime surfaces, deployment artifacts, or documentation claims.

An edge A -> B means: validity of B may depend on A.

## 2. Conservative blast radius
DirectImpact(C) = all nodes explicitly changed.
TransitiveImpact(C) = all reachable dependents through validity-relevant edges.
UnknownFrontier(C) = boundaries where dependency information is absent, stale, ambiguous, or conflicting.

SafeImpact(C) = DirectImpact ∪ TransitiveImpact ∪ UnknownFrontier.

UnknownFrontier must never be silently discarded. If a critical claim crosses it, status becomes UNKNOWN/NOT_VERIFIED and may require FREEZE.

## 3. Edge classes
PROPOSAL_AI edge taxonomy:
- REQUIRES: B cannot be valid unless A is valid.
- IMPLEMENTS: implementation B claims to satisfy requirement A.
- VERIFIED_BY: claim A relies on evidence/test B.
- CONFIGURES: A changes behavior of B.
- SERIALIZES: A defines persisted/wire representation of B.
- AUTHORIZES: A grants authority to B.
- CALLS: A invokes B.
- OBSERVES: A telemetry/evidence observes B.
- DEPLOYS: artifact A deploys component B.
- ROLLS_BACK_WITH: A and B must revert atomically.
- DOCUMENTS: A describes B and may become stale when B changes.

## 4. Impact severity
Severity is not guessed from file size or diff size.

Suggested dimensions:
- authority impact;
- safety/security impact;
- determinism impact;
- state/persistence impact;
- external interface impact;
- evidence invalidation breadth;
- reversibility;
- uncertainty.

A one-line policy change can outrank a thousand-line UI change.

## 5. Change contract
Before any future implementation, a proposed change should be normalized into:
- intended outcome;
- authoritative requirement IDs;
- exact mutation targets;
- explicitly protected targets;
- dependency snapshot identity;
- predicted impacted claims;
- unknown frontier;
- required proof classes;
- rollback unit;
- stop conditions.

## 6. Forbidden inference
Never infer "unaffected" merely because:
- a file did not change;
- a test did not fail;
- static imports do not show a dependency;
- the API shape is unchanged;
- output examples look the same.

Semantic, policy, data, deployment, and authority dependencies can exist without direct code edges.
