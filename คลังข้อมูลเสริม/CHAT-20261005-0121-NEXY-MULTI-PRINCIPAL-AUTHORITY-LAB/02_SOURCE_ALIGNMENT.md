# Source Alignment and Authority Boundary

Status: `SOURCE_GROUNDED_PROPOSAL / NOT_CANON`

## FACT — NEXY context that motivates this lab

From the current AI-CONTEXT NEXY material:
- NEXY is a deterministic AI control hub; workers/models are not final authority.
- User/human authority is preserved through explicit governed paths.
- `visible ≠ editable ≠ executable`; backend authorization remains authoritative.
- dangerous state-changing actions require explicit control/authority paths.
- current DOC-C context includes RBAC roles and server-side enforcement.
- mutable policy/config values require versioning/audit/rollback discipline.
- constitutional/future material contains some fixed quorum patterns, demonstrating quorum as an architectural concept, but those source-design statements are not current-runtime proof.
- design, implementation, runtime, and deployment evidence are separate truth classes.

## FACT — Current project status boundary

The current AI-CONTEXT status overlay marks NEXY release/deploy authorization blocked and records an exact-head coverage-gate failure for the observed implementation revision. This lab does not alter or repair that implementation state.

## PROPOSAL — What MPAL adds

MPAL explores a generalized **multi-human authority compiler/evaluator** for future team or enterprise workflows. Instead of asking a model to infer which human is “more important,” an explicit versioned policy says:
- which roles may request an action;
- which approval groups exist;
- how many distinct principals each group requires;
- which roles can veto;
- whether the requester may count as an approver;
- how many distinct approvers are required overall;
- how denial semantics work.

## Non-replacement rule

MPAL does not replace:
- NEXY::LAW;
- current RBAC;
- Core/Judge release logic;
- constitutional quorum rules;
- identity/session authentication;
- audit logging;
- cryptographic signing;
- DOC-E deployment evidence.

If adopted in the future, MPAL would have to compile into or be governed by the authoritative LAW/Core path rather than becoming a parallel authority engine.

## Why this is distinct from the existing Delegation Lease lab

Delegation Lease work concerns **temporary scoped authority delegated to an agent/work plan** and intent drift.

MPAL concerns **joint authority resolution among multiple human principals** where independent roles, quorum, veto, and maker-checker constraints must be satisfied simultaneously.

A lease can say “agent X may perform action Y for a bounded period.” MPAL answers a different prior question: “which humans had to authorize Y, did they legally do so, and is the authority evidence internally consistent?”
