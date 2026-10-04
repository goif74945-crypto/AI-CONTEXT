# NEXY Counterfactual & Change-Impact Intelligence Lab

Chat ID: **CHAT-20261005-0113-NEXY-COUNTERFACTUAL-IMPACT-LAB**
Status: ADVISORY KNOWLEDGE PACK
Authority class: SECONDARY / NON-CANONICAL
Mutation scope: AI-CONTEXT/คลังข้อมูลเสริม only

## Mission
This pack answers a difficult future engineering question: **before changing NEXY, what else becomes uncertain?**

It is intentionally not an implementation plan and does not modify NEXY.AI. It provides reusable reasoning contracts for proposed changes, dependency impact, evidence expiry, regression selection, rollback planning, and safe refusal when dependency knowledge is incomplete.

## Immutable boundary
Nothing in this pack overrides DOC-B, DOC-C, current normalized requirements, sealed evidence, runtime evidence, or explicit user law.

Every novel mechanism in this pack is labeled **PROPOSAL_AI — แนวคิดที่เสนอโดย AI ยังไม่ใช่ข้อกำหนดจริงของ NEXY.AI**.

## Core distinction
A code/config/spec change can invalidate more than code. It may invalidate:
- requirement interpretation;
- interface assumptions;
- security claims;
- deterministic guarantees;
- test coverage claims;
- performance baselines;
- deployment evidence;
- rollback assumptions;
- documentation truth.

Therefore "tests pass" is not equivalent to "all affected claims remain valid."

## Files
1. 00_CHECKPOINT.md — resumable execution state.
2. 01_CHANGE_IMPACT_CALCULUS.md — formal-ish dependency and blast-radius model.
3. 02_EVIDENCE_INVALIDATION.md — proof freshness and invalidation rules.
4. 03_SCENARIO_CATALOG.md — reusable counterfactual scenarios.
5. 04_PROPOSED_SYSTEMS.md — clearly non-canonical AI proposals.
6. 05_VALIDATION_PROTOCOL.md — pre-change/post-change verification procedure.
7. FINAL_AUDIT.md — completion evidence.

## Safe usage
Use this pack to generate questions and verification obligations, never to manufacture facts. Missing dependency edges produce UNKNOWN or FREEZE, not an invented "no impact" conclusion.
