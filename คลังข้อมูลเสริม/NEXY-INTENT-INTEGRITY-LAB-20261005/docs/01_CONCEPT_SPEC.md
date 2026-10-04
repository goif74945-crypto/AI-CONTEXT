# 01 — Intent Integrity Concept Specification

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY / NOT CURRENT NEXY.AI LAW

## Objective

Explore a deterministic mechanism that preserves human-authorized intent across long, multi-stage, multi-agent execution without requiring every worker model to retain the original conversation perfectly.

## Problem model

Semantic drift can enter at several points:

1. **Decomposition drift** — a planner drops or weakens a requirement while splitting work.
2. **Delegation drift** — downstream agents receive only a partial scope or stale objective.
3. **Evidence drift** — acceptance criteria remain but the evidence standard is silently reduced.
4. **Authority drift** — an AI-generated suggestion is promoted into a requirement without user authority.
5. **Completion drift** — an implementation artifact exists, so a worker claims the objective is complete despite missing runtime proof.
6. **Scope drift** — adjacent files/systems are modified because the model believes doing so is useful.
7. **Revision drift** — a later contract version changes meaning but is treated as equivalent to the original.

These failures are dangerous because they can produce coherent, high-quality output while violating the user's actual authority.

## Proposed contract model

The prototype uses a deliberately small contract:

- `objective`
- `scope.in_scope`
- `scope.out_of_scope`
- `scope.protected`
- `scope.allowed_repositories`
- `scope.protected_repositories`
- `requirements[]` with stable IDs
- `acceptance_criteria[]` with minimum evidence classes
- `stop_conditions[]`
- `unknowns[]`
- `assumptions[]`

The contract is canonicalized and hashed. This produces a stable identity for the semantic envelope being enforced.

## Invariants

### I-01 — Mandatory coverage
Every `must` and `must_not` requirement must appear in the proposal's covered requirement set.

### I-02 — Protected scope dominates convenience
Any proposal targeting a protected repository identity or touching a protected path causes `FREEZE`.

### I-03 — Explicit out-of-scope means forbidden
A path matching `out_of_scope` cannot be touched by the proposal.

### I-04 — In-scope is an allow boundary
When `in_scope` is non-empty, touches outside the allow patterns cause `FREEZE`.

### I-05 — Evidence cannot be weakened silently
Observed evidence must meet or exceed each criterion's minimum class.

### I-06 — Unverified is not complete
A claim marked `NOT_VERIFIED` cannot simultaneously be a completion claim.

### I-07 — Assumption is not fact
A fact-class claim cannot use an explicitly assumption/guess basis.

### I-08 — Contract change requires exact authorization
Changing objective, scope, requirements, criteria, assumptions, unknowns, or stop conditions creates deterministic change IDs. A change is authorized only if the approval envelope names that exact ID.

### I-09 — Approval is not blanket permission
An approval for one change does not authorize another concurrent change.

### I-10 — Order must not create fake drift
Set-like arrays and keyed objects are canonicalized so harmless ordering changes do not alter the semantic digest.

## Evidence hierarchy used by the prototype

`none < inspection < static < unit < integration < e2e < runtime < deployment < physical`

This is a research simplification. It must not be imported into authoritative NEXY law without explicit review because evidence classes are domain-dependent and not always totally ordered in real systems.

## Decision states

- `PASS` — no blocking or review findings.
- `REVIEW` — no blocking violation, but a non-fatal anomaly requires human/system review.
- `FREEZE` — the proposal violates an invariant or lacks required proof.

## Why deterministic digests are useful

A digest does not prove correctness. It proves identity of the canonical representation used by the guard. That is still valuable because it allows logs, approvals, execution proposals, and evidence records to bind to the exact contract revision they were evaluated against.

Potential benefits include:

- replayable audits;
- stale-contract detection;
- cross-agent handoff integrity;
- explicit approval lineage;
- fast detection of unauthorized semantic mutation.

## Important limitation

Natural-language semantic equivalence is undecidable in the general case for a simple deterministic guard. This prototype therefore avoids pretending otherwise. It detects structural contract drift, not arbitrary prose equivalence.
