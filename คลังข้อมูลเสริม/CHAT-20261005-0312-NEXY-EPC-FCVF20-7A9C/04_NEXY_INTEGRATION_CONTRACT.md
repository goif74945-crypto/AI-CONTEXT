# NEXY Integration Contract — Advisory Shadow Boundary

## Purpose

This contract defines how FCVF-20 could later be connected to NEXY without granting it authority. It is an integration proposal only and is not evidence that NEXY currently imports or runs this package.

## Required upstream inputs

An adapter supplies a candidate identity, durable CHAT_ID, exact authoritative spec identity/hash, exact NEXY repo/branch/commit pin, exact AI-CONTEXT commit pin, current candidate status, evidence references, and requested EPC event. Time, network state and model-generated confidence are not implicit inputs.

## Output contract

FCVF may return a deterministic transition result, constitutional findings, canonical state/receipt hash, bounded exploration report, or minimized counterexample. These outputs are **advisory verification evidence**. They are not NEXY commands, JUDGE decisions, LAW updates, Canon state, or release authorization.

## Hard authority boundary

FCVF must never receive credentials or APIs capable of directly writing NEXY Core state, Canon, LAW, JUDGE state, production state, Git branches, PRs, workflows, or deployment configuration. An integration adapter should expose a one-way data path into FCVF and a read-only evidence path out.

The current NEXY exact-head evidence motivating this boundary includes `packages/core/vnext-state-matrix.ts`, where CORE owns boot/execute, SWARM owns agents_done and JUDGE owns verified/accepted/rejected; and `packages/intelligence/trinity.ts`, where the publisher is `EXTERNAL_JUDGE`, implicit override is false and Lo2 may not override the current decision.

## Proposed future pipeline

A safe future flow is: candidate/evidence snapshot -> FCVF canonicalization -> strict transition/model checks -> evidence artifact -> existing external verification/JUDGE-compatible review boundary. A failure must stop at the evidence boundary. A PASS can only mean "FCVF constitutional checks passed for this pinned snapshot and modeled scope". It must not mean "promoted" or "approved by NEXY".

## Drift handling

If the NEXY commit, authoritative source hash, AI-CONTEXT evidence commit, FCVF code or constitutional rule set changes, previous proof artifacts become stale for changed claims. The adapter must pin exact identities and rerun required verification. Never transplant a PASS across changed bytes merely because filenames remained the same.

## Failure behavior

Malformed pins, missing critical evidence, invalid Q64 values, exhausted vote rights, WIP CUT, destructive CUT, duplicate-without-witness, retrospective verdict mutation, promotion attempt, Core mutation attempt, and Canon override attempt all fail closed. No hidden fallback converts them to permissive behavior.
