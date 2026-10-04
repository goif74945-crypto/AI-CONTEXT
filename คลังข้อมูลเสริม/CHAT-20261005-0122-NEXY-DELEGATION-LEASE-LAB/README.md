# NEXY::LEASE — Reversible Authority Lease & Intent Drift Firewall

**Status:** AI-PROPOSED CONCEPT + VERIFIED REFERENCE PROTOTYPE  
**Authority:** Supplemental only. Not DOC-B, not DOC-C, not current NEXY implementation, not deployment evidence.  
**Workstream:** `CHAT-20261005-0122-NEXY-DELEGATION-LEASE-LAB`

## Why this exists

NEXY already has strong principles around USER LAW, explicit authority, RBAC, FREEZE, rollback, truth-preserving UI, and the invariant that visible/editable/executable are different capabilities. A future tool-using or autonomous execution layer creates a narrower problem: **an actor may be authenticated and role-authorized while still attempting an action that is outside the exact plan the operator authorized.**

This project proposes an additional restrictive control, never an authority bypass:

> Bind execution authority to a short-lived, revocable lease over a concrete plan fingerprint, exact action classes, resource scope, effect class, and finite budget. Any material drift blocks execution and requires a new authorized plan.

The goal is to improve safety **and** user experience. Instead of prompting for every trivial step, the operator can authorize one bounded plan. NEXY can then execute only within that exact envelope. If the plan changes, authority does not silently follow it.

## Core concept

An `AuthorityLease` binds:
- subject / delegated actor;
- resource patterns;
- allowed verbs;
- effect classes;
- action and cost budgets;
- logical activation/expiry ticks;
- exact `plan_hash`;
- policy version;
- a separate explicit high-impact gate;
- optional parent lease for monotonic delegation.

A candidate action is allowed only when all relevant checks pass. Otherwise the reference engine returns `FREEZE` with a deterministic reason code.

## What the prototype proves

Current local verification for the reference package:
- Python compile/static syntax: PASS (E1)
- Unit behavior suite: PASS, 21/21 (E2)
- JSON schema parse: PASS (E1 presence/syntax parse, not full JSON Schema conformance)
- Demo execution: PASS for the exact allowed path (E2/example)

The prototype does **not** prove production readiness, distributed consistency, identity authenticity, cryptographic signing, provider-specific resource canonicalization, deployment behavior, or integration with the actual NEXY implementation.

## Files

- `01_CONCEPT_AND_PRODUCT_VALUE.md` — problem, value, non-goals, user benefit
- `02_ARCHITECTURE.md` — boundaries, data contracts, state and flow
- `03_REQUIREMENT_LEDGER.md` — requirement → implementation → evidence/status
- `04_FAILURE_THREAT_MODEL.md` — abuse/failure analysis and mitigations
- `05_UX_CONTROL_PROTOCOL.md` — human-facing authorization/freeze experience
- `06_INTEGRATION_AND_PROMOTION_GATE.md` — what must be true before canonical adoption
- `07_VERIFICATION_PLAN.md` — evidence classes and test strategy
- `08_AI_PROPOSED_IDEA_BACKLOG.md` — explicitly non-canonical future ideas
- `09_FORMAL_INVARIANTS.md` — safety invariants and proof obligations
- `reference/` — standalone Python reference implementation and tests
- `schemas/` — proposal schemas
- `evidence/TEST-EVIDENCE.md` — executed evidence log

## Hard boundary

This workstream must never be read as authorization to modify a repository whose name contains `NEXY.AI`. Adoption requires an explicit future specification decision and an independently authorized implementation task.
