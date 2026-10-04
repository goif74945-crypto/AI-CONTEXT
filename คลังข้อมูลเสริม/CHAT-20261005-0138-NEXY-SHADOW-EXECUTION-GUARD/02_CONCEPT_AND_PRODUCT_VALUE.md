# Concept & Product Value — NEXY Shadow Execution Guard

Status: AI-PROPOSED / EXPERIMENTAL / ADVISORY ONLY

## Problem

A tool call can be syntactically valid and still be operationally wrong.

Examples:
- a generated patch writes one directory higher than intended;
- an update is based on a stale file hash;
- a move crosses from an authorized subtree into a protected subtree;
- a delete is technically allowed by a broad prefix but cannot be rolled back because no restore bytes were captured;
- an adapter emits a tool action whose side effects are not modeled.

Schema validation alone does not answer whether the *planned effects* are legal.

## Proposed capability

Insert a deterministic shadow stage before high-impact mutation:

`candidate tool plan → canonical effects → Shadow Execution Guard → PREVIEW_PASS | FREEZE → human/JUDGE/executor`

The guard works only on a caller-supplied snapshot and declared effects. It does not call the real tool.

## User value

- Fewer accidental destructive actions.
- Clearer “why frozen” diagnostics before damage occurs.
- Detect stale preconditions before a write.
- Explicit predicted blast radius.
- Explicit rollback completeness instead of vague “undo is possible” promises.
- Portable safety behavior across provider/tool adapters.
- Deterministic artifact that another model/operator can review.

## Why this is different from nearby supplemental work

- Tool Contract Drift Lab: asks whether an external tool’s contract changed.
- Minimal Blocker Core: explains why a verification gate cannot pass.
- Intent Integrity Lab: protects intent/requirements from unauthorized reinterpretation.
- Resource Governor: allocates bounded resources while preserving proof obligations.
- Shadow Execution Guard: simulates declared mutation effects against scope + snapshot *before execution*.

These systems could compose, but this lab deliberately owns only the shadow-effect boundary.

## Product principle fit

The concept aligns with NEXY’s documented direction:
- verify before action;
- freeze rather than guess;
- keep tools/models as workers, not authority;
- preserve human/user authority;
- expose useful results without requiring users to understand hidden internals;
- define recovery behavior for durable mutation.

## Important truth boundary

This document proposes a capability. It is not evidence that current NEXY.AI implements, invokes, or needs this exact subsystem.
