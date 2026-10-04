# Invariant Ledger

INV-001 Authority precedence is preserved.
INV-002 Scope cannot silently expand or shrink.
INV-003 Missing facts remain UNKNOWN.
INV-004 Completion claims require evidence.
INV-005 Mutation target identity is exact.
INV-006 Critical replacement/destructive writes require pre-state inspection.
INV-007 Critical writes require read-after-write.
INV-008 Retries account for idempotency and partial commit.
INV-009 Failures remain visible in execution state.
INV-010 Required compatibility cannot be traded for local success.
INV-011 Every mandatory requirement receives a terminal state.
INV-012 TODO/mock/fake success cannot satisfy production acceptance.
INV-013 Mutable evidence carries observation time.
INV-014 Transformed facts retain provenance.
INV-015 Forbidden-action checks precede optimization.
INV-016 Material target ambiguity triggers FREEZE.
INV-017 Verification should independently observe state where practical.
INV-018 Recovery uses the smallest safe correction.
INV-019 Fixes trigger affected regression checks.
INV-020 Tool/time limits produce INCOMPLETE or NOT VERIFIED, never invented completion.

## Task-specific locks
INV-NX-001 No repository whose name contains NEXY.AI may be mutated by this work.
INV-NX-002 Authored artifacts remain inside AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0112-NEXY-SEMANTIC-CONTRACT-LAB.

## Phase-boundary check
Ask whether authority, scope, target identity, unknowns, write verification, failure visibility, or objective relevance changed. Any unexplained critical change freezes mutation until resolved.
