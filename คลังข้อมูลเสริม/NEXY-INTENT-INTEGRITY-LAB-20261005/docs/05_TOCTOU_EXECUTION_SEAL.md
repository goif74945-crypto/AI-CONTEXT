# 05 — TOCTOU Execution Seal

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Motivation from this session

During additive writes to `AI-CONTEXT/main`, several GitHub Contents API operations returned HTTP `409` because another concurrent writer advanced the branch between state observation and mutation. No destructive action occurred, but the event demonstrates a real control-plane property: a proposal that is valid at time T1 can become stale before mutation at time T2.

Treating a previous PASS as perpetual authorization would therefore be incorrect.

## Proposed mechanism

An **Execution Seal** binds five values:

1. target repository identity;
2. target ref;
3. exact target revision;
4. canonical intent-contract digest;
5. canonical execution-proposal digest.

A deterministic `seal_digest` covers those values. Immediately before mutation, the executor re-reads current state and verifies all bound values.

If any value differs, the result is `FREEZE` and the workflow must re-read, re-plan if necessary, and re-validate.

## Important boundary

The prototype's deterministic digest is **not a signature**. It detects accidental/tampered data changes only when the verifier already trusts the inputs. It does not authenticate a human, repository host, or adversarial actor.

Production adoption would require authenticated repository identity, signed authority, replay protection, and transaction/precondition support from the mutation backend.

## Why this matters for NEXY-like control systems

The core lesson is broader than GitHub: evidence has a validity window. Any control decision tied to mutable state should identify the exact state it proves.

Examples:

- repository commit SHA;
- database version/transaction snapshot;
- deployment artifact digest;
- policy bundle version;
- model configuration digest;
- hardware/firmware revision.

A verified action should not execute against a materially different world than the one that was verified.
