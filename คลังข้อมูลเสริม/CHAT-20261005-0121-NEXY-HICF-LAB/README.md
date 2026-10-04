# AI-PROPOSED NEXY Human Intent Continuity Fabric (HICF)

**Classification:** AI-PROPOSED / SUPPLEMENTARY / NON-CANONICAL  
**Run ID:** `CHAT-20261005-0121-NEXY-HICF-LAB`

## Purpose

HICF is a proposed interaction-control layer for preserving the user's objective, authority, immutable constraints, and clarification state across long-running AI work while minimizing unnecessary interaction.

It is deliberately **not** a replacement for NEXY CIRL, USER LAW, CORE, JUDGE, RSEL, GUARD, DIALOG, or the canonical freeze model. It is a candidate front-door control fabric that can provide deterministic, inspectable inputs to those systems if a future authoritative specification adopts it.

## Problem

A capable AI agent can still fail users in boring but expensive ways:

- asking the same question again after it was already answered;
- asking low-value clarifications when a safe reversible default exists;
- silently changing the objective during a long task;
- treating inferred preferences as durable user law;
- continuing through an authority conflict because the UI wanted to feel smooth;
- over-freezing harmless read-only work because *any* unknown exists;
- losing the exact reason why a clarification was required.

HICF separates these concerns into deterministic records and gates.

## Components

1. **Intent Envelope** — canonical representation of objective, constraints, immutables, prohibitions, unknowns and authority state.
2. **Continuity Fingerprint** — stable SHA-256 fingerprint over canonical intent state.
3. **Clarification Gate** — deterministic `PROCEED | ASK | FREEZE` decision.
4. **Friction Budget** — detects excessive/repeated clarification without weakening correctness.
5. **Intent Drift Detector** — classifies `NONE | LOW | MATERIAL | AUTHORITY_BREAK`.
6. **Scoped Preference Record** — blocks inferred durable preferences.
7. **Decision Record** — machine-readable reason/evidence surface for downstream orchestration and audit.

## Non-goals

- no claim that HICF exists in current NEXY implementation;
- no modification of NEXY.AI source code;
- no attempt to redefine User Law or canonical authority;
- no learning from behavior into durable memory without explicit authority;
- no replacement for full policy, safety, risk, or security evaluation.

## Verification achieved in this lab

- Python compile: PASS (E1)
- JSON parse for schemas: PASS (E1)
- 15 unit tests: PASS (E2)
- 576-case deterministic state matrix: PASS (E2-style exhaustive model validation)

No integration, browser, runtime, deployment, or production claim is made.
