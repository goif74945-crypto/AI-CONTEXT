# NEXY Authority Collision Compiler (ACC)

**Classification:** AI-PROPOSED INTEGRATION CANDIDATE. **NOT canonical NEXY.AI law.**

## Objective
Provide a small deterministic pre-execution compiler that resolves normalized directives by explicit authority instead of letting a model guess when instructions collide.

## Scope lock
IN SCOPE: this standalone artifact under `AI-CONTEXT/คลังข้อมูลเสริม/` and local tests.
OUT OF SCOPE: any write to a repository whose name contains `NEXY.AI`; natural-language policy parsing; claiming NEXY runtime/deployment integration.

## Contract
Input: target, subject, optional exact-match context, directives, optional `requireDecision`.
Each directive supplies ID, caller-authorized `authorityRank`, source class, scope, subject, JSON value, optional conditions/priority/provenance.

Precedence: `(authorityRank ASC, scopeSpecificity DESC, localPriority DESC)`.
IDs stabilize ordering only. IDs never resolve contradictory values.

## Required behavior
- Higher authority always dominates lower authority, even when the lower authority is more scope-specific.
- Equal strongest precedence + different canonical values => `FREEZE_CONFLICT`.
- No applicable directive => `FREEZE_NO_DECISION` when required, else `NO_DECISION`.
- Lower contradictory directives remain in trace as `SHADOWED`.
- Equivalent weaker directives are `REDUNDANT`.
- Output includes normalized input fingerprint and decision fingerprint.
- Caller-owned selected values are canonicalized into a snapshot so post-compile mutation cannot silently desynchronize decision content from its fingerprint.

## Determinism design
- JSON object keys sort lexicographically.
- `-0` normalizes to `0`; NaN/Infinity reject.
- Directive/condition input order is normalized for fingerprinting.
- ASCII canonical token IDs avoid locale-dependent ordering.
- Scope syntax: exact segments, `*` for one segment, terminal `**` for tail match.

## NEXY integration boundary
A future authorized NEXY adapter could map canonical authority sources to numeric ranks, normalize scope/subject keys, then invoke ACC before the law/judge execution gate. ACC deliberately does not hard-code NEXY authority law.

## Failure model
Malformed contracts throw `TypeError`. Legitimate strongest-tier contradiction returns a freeze object. This keeps invalid input separate from a valid policy collision.

## Acceptance evidence
E1 strict TypeScript build + E2 executed behavior tests. E3+ integration/runtime/deployment evidence is intentionally unavailable because NEXY.AI mutation is forbidden in this task.
