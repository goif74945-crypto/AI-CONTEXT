# Adoption Gates

**Status: AI_PROPOSED_CONCEPT. Not an adoption decision.**

This lab must remain supplemental until an authorized project authority deliberately promotes some or all of it.

## Gate A — Authority compatibility

Required before promotion:
- map every promoted rule to DOC-B/DOC-C/DOC-D authority;
- prove no alternate authority path is created;
- verify upstream role and system-state provenance;
- confirm canonical backend RBAC still decides execution authority;
- reject any proposal rule that conflicts with newer project law.

Failure: `BLOCKED`.

## Gate B — Requirement coverage

Required:
- map proposed integration to the current 837-row normalized source matrix;
- enumerate impacted current-build rows;
- identify excluded/deferred/future domains separately;
- prove that no deprecated 215-entry denominator is used.

The current lab has **not** performed this exhaustive mapping.

## Gate C — Security

Required:
- abuse tests for forged role/state/consent input;
- replay tests for consent binding;
- canonicalization ambiguity review;
- denial-of-service bounds for malformed contracts;
- provenance/identity for authority-bearing inputs;
- audit privacy review.

A local unit test is not enough for production security claims.

## Gate D — Determinism

Required:
- cross-platform canonicalization vectors;
- same-input/same-output property tests;
- stable schema/version behavior;
- explicit evolution policy for hashes and consent bindings;
- rejection of ambiguous serialization.

## Gate E — UX integrity

Required:
- critical FREEZE always visible;
- no false success;
- no hidden dangerous-control path;
- no added question when an action can legally continue;
- one aggregated material question performs at least as well as repeated questioning;
- newcomer and advanced-operator flows both remain understandable.

Authority regression is a hard failure even if user preference metrics improve.

## Gate F — Evidence integrity

Required:
- acceptance evidence references must resolve to real evidence records;
- stale evidence invalidation must be defined;
- presentation PASS may never substitute for action/release proof;
- UX tests may never substitute for backend authorization tests.

## Gate G — Integration

Required:
- exact integration boundary defined;
- canonical CORE/LAW ownership unchanged unless separately authorized;
- no direct UI-to-authority bypass;
- rollback path proven;
- API/schema contracts versioned;
- integration tests run at exact revision.

## Gate H — User study

Research hypothesis:
A structured intent contract + aggregated material questioning can reduce operator friction without increasing unsafe assumptions.

To test it:
- compare interruption count and task completion;
- measure comprehension of next legal action after FREEZE;
- measure false-success perception;
- stratify by declared experience, not inferred personality;
- never manipulate attachment/emotion as a product metric.

No benefit claim is made until evidence exists.

## Gate I — Production

Production readiness would require applicable E3/E4/E5/E6 evidence. This lab currently has only E0/E1/E2 evidence for its standalone reference code.
