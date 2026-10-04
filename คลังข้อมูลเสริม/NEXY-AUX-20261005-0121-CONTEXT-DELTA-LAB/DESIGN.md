# Design Contract — AI-Proposed Context Delta Lab

## Purpose
Detect source/context drift before an AI or operator reuses stale implementation or verification conclusions.

## Non-goals
- No NEXY runtime execution.
- No automatic edits to canonical project context.
- No automatic acceptance/promotion of changed requirements.
- No claim that a changed requirement is implemented.
- No network, database, clock, randomness, or hidden I/O in the core engine.

## Actors and authority
- Snapshot producer owns source normalization.
- Delta engine owns deterministic comparison only.
- Revalidation queue is advisory.
- Human/project authority owns promotion, implementation, and final status.

## Data model
A snapshot contains immutable identifying metadata plus normalized requirement records. Each record has:
- stable `id`;
- `authority`;
- `scope`;
- normative `statement`;
- required `evidence_class`;
- closed-world `depends_on` edges;
- optional `source_hash`;
- optional metadata.

## State machine
`LOAD -> VALIDATE -> CANONICALIZE -> DIFF -> PROPAGATE -> PLAN -> REPORT`

Failure transition from any pre-report stage:
`* -> FREEZE`

## Invariants
I-01 IDs are unique.
I-02 Every dependency resolves inside its snapshot.
I-03 Dependency graph is acyclic.
I-04 Authority/scope/evidence values belong to explicit enums.
I-05 Core output ordering is stable.
I-06 No output field claims runtime PASS.
I-07 Changed canonical authority cannot be downgraded below HIGH impact.
I-08 Removed current-law/current-build records are CRITICAL.
I-09 Transitive dependents are included once even through multiple paths.
I-10 Snapshot and report fingerprints use SHA-256 over canonical JSON.

## Failure model
- invalid JSON -> exit 3 / no report;
- invalid schema semantics -> exit 2 / no report;
- missing dependency -> exit 2;
- cycle -> exit 2;
- output write failure -> exit 3;
- change with `--fail-on-change` -> report is written, then exit 4.

## Security boundary
The engine parses data only. It does not execute content from statements or metadata. No shell interpolation, imports, eval, or network actions are derived from snapshot values.

## Evidence plan
E1: Python compilation.
E2: deterministic unit tests for validation, classification, impact propagation, ordering, fingerprinting, and CLI exit behavior.
E3+: intentionally NOT_VERIFIED; integration into any NEXY workflow is future work.
