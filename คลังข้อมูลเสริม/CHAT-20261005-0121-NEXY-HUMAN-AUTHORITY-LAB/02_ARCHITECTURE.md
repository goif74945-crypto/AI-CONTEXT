# Architecture — Human Authority & Interaction Integrity Lab

**Classification: AI_PROPOSED_CONCEPT.** This document is not current NEXY law or build authority.

## 1. Design objective

Reduce interaction friction while making authority mistakes harder. The design must never trade truth for convenience.

The proposed architecture treats a user interaction as an explicit contract evaluation rather than a free-form conversational impression:

`IntentContract + ActionRequest + SystemState + ConsentBinding -> ALLOW | ASK | FREEZE`

A separate presentation checker then verifies that the UI representation does not contradict the decision.

## 2. Modules

### 2.1 Intent Contract

Purpose: encode the objective and legal boundary before mutation.

Fields include:
- actor/role;
- mode;
- allowed scope;
- protected scope;
- external-I/O authorization;
- interruption budget;
- required outcome IDs;
- material fields that are either present or explicitly missing.

Important constraint: the engine does **not** infer authorization from natural-language similarity. Mutation alignment is established by explicit outcome IDs.

### 2.2 Action Evaluator

Deterministic gate order:

1. contract validity;
2. system state legality;
3. role permission;
4. protected-scope rejection;
5. allowed-scope membership;
6. external-I/O authority;
7. objective alignment;
8. material-information gate;
9. irreversible-consent gate;
10. allow.

The order intentionally fails early on stronger boundaries before lower-level usability concerns.

### 2.3 Material Question Aggregator

Missing material fields are aggregated into one question event. This is designed to reduce repeated operator interruption while keeping the zero-guess rule.

If the declared interruption budget is exhausted, unresolved material information produces `FREEZE`, not silent guessing.

### 2.4 Irreversible Consent Binding

An irreversible action requires explicit consent bound to:

- canonical hash of the exact `IntentContract`;
- canonical hash of the exact `ActionRequest`;
- OWNER or SYSTEM grantor in this reference model;
- explicit consent flag.

Any mismatch freezes. A consent record from an older objective or different action cannot authorize the new action.

This is a conceptual binding mechanism, not a production authentication protocol.

### 2.5 Progressive Disclosure Planner

Input:
- declared mode;
- role;
- authoritative system state.

Output:
- visible panels;
- visible controls;
- mandatory notices.

Critical rule: progressive disclosure may hide complexity, but may not hide authoritative FREEZE/STOP or expose a control the role cannot legally execute.

### 2.6 Presentation Integrity Evaluator

Checks:
- FREEZE is visible whenever state is FREEZE;
- success is not shown when the action decision is ASK/FREEZE;
- visible controls are a subset of the role/state disclosure plan.

This separates UI truth from action authorization. Passing the presentation check does not authorize anything.

### 2.7 Acceptance Evaluator

Required outcome criteria can be:
- PASS;
- FAIL;
- NOT_VERIFIED.

A required PASS without an evidence reference remains `NOT_VERIFIED`. This avoids the common human-interface failure where “looks done” silently becomes “proven done.”

### 2.8 Trace Integrity Evaluator

Evaluates interaction events for:
- questions with no material blocker;
- repeated questions for the same blocker;
- interruption budget overflow;
- success display after a freeze display.

This is an offline conformance mechanism, not a runtime monitoring claim.

## 3. Determinism model

The reference engine uses:
- explicit enums;
- deterministic rule order;
- sorted reason codes;
- canonical object-key ordering before SHA-256 hashing;
- no randomness;
- no system time;
- no model call;
- no network call.

Arrays preserve declared order because sequence can be semantically meaningful.

## 4. Scope matching

The prototype supports:
- exact scope match: `artifact:alpha`;
- namespace wildcard ending in `:*`: `artifact:*`.

Protected scope wins over allowed scope.

This intentionally small grammar is easier to reason about and test than arbitrary glob/regex authorization.

## 5. Permission model

Reference defaults are intentionally conservative:
- `CONFIG`, `RECOVER`, and irreversible mutation: OWNER/SYSTEM;
- directive submission, reversible mutation, external I/O: OWNER/OPERATOR/SYSTEM;
- export: OWNER/OPERATOR/AUDITOR/SYSTEM;
- read: all roles.

An action may also declare an exact `required_role`.

This is an experimental mirror of the source direction, not a replacement for canonical backend RBAC.

## 6. Failure semantics

`ASK` is allowed only when a user answer can resolve a material blocker within the declared interruption budget.

`FREEZE` is used for:
- invalid contract;
- STOP/FREEZE state violations;
- permission denial;
- protected/out-of-scope action;
- unauthorized external I/O;
- objective drift;
- exhausted interruption budget;
- stale/mismatched/invalid irreversible consent.

No automatic retry exists in this lab.

## 7. Trust boundaries

Untrusted:
- free-form objective text;
- display text;
- external provider content;
- UI visibility.

Authority-bearing only after explicit contract validation:
- role field supplied by an upstream authenticated authority;
- declared scope/policy;
- system state;
- explicit consent binding.

The lab itself does not authenticate those upstream values. Production adoption would require secure provenance for all authority-bearing inputs.

## 8. Observability proposal

A future integration could emit structured records containing:
- contract hash;
- action hash;
- decision;
- reason codes;
- question count;
- presentation violations;
- acceptance result;
- trace-integrity result.

No raw secret or credential should be included.

## 9. Proposed metrics

These are research metrics, not current KPIs:

- **Objective Drift Escape Rate**: unauthorized outcome drift not blocked by the evaluator.
- **Authority Leakage Rate**: forbidden control/action exposed or allowed.
- **Freeze Visibility Violation Rate**: frozen state not visibly represented.
- **False Success Surface Rate**: success UI shown when decision is not ALLOW.
- **Material Interruption Efficiency**: material blockers resolved per interruption.
- **Repeated Interruption Rate**: repeated question for unchanged blocker.
- **Acceptance Evidence Gap Rate**: required PASS without evidence.
- **Consent Binding Rejection Accuracy**: stale/wrong consent correctly rejected.

Any adoption gate should prioritize zero critical authority/freeze escapes over lower friction scores.

## 10. Non-goals

This lab does not:
- parse natural language into a trusted contract;
- authenticate users;
- replace DOC-B/DOC-C/DOC-D;
- change NEXY FSM;
- authorize real destructive operations;
- define production cryptographic consent;
- measure actual user satisfaction;
- prove accessibility or usability;
- prove compatibility with all 837 normalized requirements.

## 11. Integration position if ever adopted

A safe future integration would place this logic as an advisory/preflight contract gate around human-facing request preparation, while canonical LAW/CORE/RBAC remain authoritative.

It must never become a second hidden authority path.
