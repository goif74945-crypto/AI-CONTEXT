# NEXY Lo4 Adversarial Innovation Lab

Status: `Lo4_AI_PROPOSAL_ONLY`
Conversation code: `CHAT-20261005-0222-NEXY-LO4-ADVERSARIAL-INNOVATION-LAB`
Target persistence: `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0222-NEXY-LO4-ADVERSARIAL-INNOVATION-LAB`

## Purpose

This lab proposes and executes five deterministic assurance mechanisms intended to be compatible with future NEXY.AI integration while remaining outside Canon until formal proof and promotion. The work intentionally does **not** mutate any repository whose name contains `NEXY.AI`.

The five mechanisms are:

1. **AURORA** — Abstention Utility & Risk-Oriented Reliability Analyzer.
2. **MARGIN** — Decision Legality Margin Sentinel.
3. **UPA** — Unknown Propagation Algebra.
4. **TRACEWEIGHT** — Agent Influence Dominance Auditor.
5. **CONTRACT-DRIFT** — Task Contract Drift Budgeter.

## Why these five

NEXY already emphasizes deterministic adjudication, zero-guess behavior, verification, freeze semantics, multi-agent orchestration, authority boundaries and provenance. These prototypes target gaps adjacent to those principles without claiming the gaps are current NEXY defects:

- measure whether an agent abstains at the right time rather than rewarding answer rate alone;
- distinguish robust legality from a pass that sits dangerously close to a boundary;
- represent UNKNOWN and CONFLICT as first-class values instead of coercing them to booleans;
- detect pseudo-multi-agent decisions whose causal influence is dominated by one upstream agent;
- detect silent weakening or expansion of a structured Task Contract during long execution.

## Implementation surfaces

- Python 3.11+ reference implementation using only the standard library.
- TypeScript 5.x parity implementation aligned with the current NEXY build direction of Next.js + TypeScript.
- Cross-runtime fixture verifying semantic parity for representative inputs.
- Deterministic unit, negative-path, fuzz/property-style and integration tests.

## Evidence boundary

What this lab can prove locally:

- E0: artifacts exist in this lab.
- E1: Python compilation and TypeScript strict compilation succeed.
- E2: unit and deterministic fuzz tests succeed.
- E3: local cross-module integration and Python/TypeScript parity fixture succeed.

What it does **not** prove:

- integration with the actual NEXY implementation repository;
- NEXY runtime behavior;
- deployment readiness or production performance;
- canonical requirement status;
- security properties beyond the executed local tests.

## Promotion rule

Nothing in this folder may be interpreted as NEXY Canon merely because it is useful or tested. Promotion requires explicit authority, mapping to governing requirements, implementation review against the exact NEXY revision, matching evidence, regression analysis and an authorized promotion decision.
