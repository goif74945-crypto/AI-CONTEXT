# NEXY Directive Integrity / Semantic Continuity Lab

Status: **AI-PROPOSED / EXPERIMENTAL / ADVISORY ONLY**  
Session code: `NEXY-DIRECTIVE-INTEGRITY-20261005-0121-SOL`  
Storage target: `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม`  
Protected implementation repository: any repository whose name contains `NEXY.AI` is **READ-ONLY** for this work.

## Purpose

This lab studies a narrow failure mode that can survive otherwise strong deterministic architecture: a directive may be accepted correctly at one boundary, then have its meaning silently broadened, narrowed, redirected, de-authorized, or risk-downgraded while it is transformed into downstream contracts.

The proposal does **not** replace NEXY CIRL, CLE, JUDGE, LAW, or the existing execution transaction model. It adds a possible future semantic-continuity invariant between boundaries:

`accepted directive semantics -> normalized snapshot -> downstream snapshot -> compare -> PASS or FREEZE`

The central principle is:

> A transformation may reformat meaning, but it may not materially change meaning without explicit evidence-backed re-authorization.

## Why this is different from existing work

Observed project context already has explicit intent resolution (CIRL), constraint compilation (CLE), canonical request fingerprints, idempotency, execution transactions, evidence, and freeze semantics. Those solve adjacent problems. This lab focuses on **cross-boundary semantic drift**: whether an action, target, constraint, scope exclusion, side effect, authority reference, ambiguity state, mutation class, or impact class changed between two representations.

A byte-level or JSON request hash proves identity of one representation. It does not by itself prove that a later, intentionally different representation preserved the same authorized semantics. This lab proposes a small explicit semantic snapshot and transition verifier for that gap.

## Deliverables

- Task contract and provenance/gap analysis.
- AI-proposed semantic-continuity specification.
- JSON Schema for directive snapshots and authorization grants.
- Executable Python reference engine with deterministic SHA-256 canonicalization.
- Negative-path fixtures and unit tests.
- Operator-facing explanation contract that exposes blockers without hidden reasoning.
- Future adoption map that keeps current NEXY implementation untouched.
- Validation report, test matrix, manifest, and final audit.

## Authority boundary

Nothing in this folder is a NEXY requirement merely because it is detailed or tested. Promotion would require the project's normal authority/spec process and integration evidence. Current NEXY source/spec remains authoritative over this proposal.

## Safety boundary

The reference implementation has no network access, no repository mutation, no secrets, and no external side effects. It only compares JSON-like snapshots and emits PASS/FREEZE plus machine-readable violations.
