# 03 — SNCG: Semantic Namespace Collision Guard

**Status:** AI-PROPOSED / Lo4 / NON-CANONICAL

## Objective
Detect contracts that look compatible by name but are semantically incompatible.

## Contract fingerprint
Each symbol declares:
- namespace;
- canonical name + aliases;
- stable semantic ID;
- kind;
- domain;
- unit;
- authority source;
- lifecycle.

Labels are normalized with Unicode NFKC + casefold before comparison.

## Collision classes
- `NAMESPACE_COLLISION`: same normalized name/alias maps to different semantic identities.
- `IDENTITY_DRIFT`: same semantic ID carries an incompatible signature.

## Immutable rules
- Shared names are legal only when they resolve to the same semantic identity and compatible signature.
- Same semantic ID cannot silently change kind/domain/unit/authority/lifecycle.
- Unicode width/case variants cannot bypass collision checks.

## NEXY fit
NEXY spans UI, API, policy, evidence, memory, runtime and model-provider layers. Terms such as `TTL`, `status`, `confidence`, `authority`, `verified` or `session` can silently diverge. SNCG is designed as a contract-lint gate before cross-layer integration.

## Failure behavior
Empty names/aliases or semantic IDs are invalid. Collisions are reported, never auto-renamed or auto-merged.

## Acceptance evidence
E2 tests cover valid shared identity, name collision, semantic-ID drift and Unicode-width normalization; stress covers 2,000 symbols plus injected collision.
