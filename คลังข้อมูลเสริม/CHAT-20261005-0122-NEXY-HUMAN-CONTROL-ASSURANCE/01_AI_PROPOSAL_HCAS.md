# AI Proposal — Human Control Surface Assurance Layer

Status: **PROPOSAL / NOT APPROVED / NOT IMPLEMENTED IN NEXY.AI**

## Problem
A deterministic backend can still lose user trust or safety if its human-facing controls misrepresent state. Typical failures include role-hidden buttons being mistaken for authorization, pending animation implying success, destructive controls omitting irreversible consequences, FREEZE being visually suppressible, or a failure path having no explicit user-visible outcome.

## Proposal
Represent critical UI/control semantics as a small manifest and lint it before implementation/release. The manifest is not authority. It is an inspectable contract connecting product design to backend and verification obligations.

Pipeline:
`SOURCE REQUIREMENT -> CONTROL MANIFEST -> HCAS STATIC CHECK -> IMPLEMENTATION -> E3/E4 BEHAVIOR PROOF -> RELEASE EVIDENCE`

## Design properties
1. Deterministic: no clock, network, randomness or model calls in validation.
2. Provider-independent: pure JSON input + Python standard library.
3. Fail-closed: malformed or contradictory high-impact action metadata is an ERROR.
4. Evidence-aware: every action names the evidence class expected for its claim.
5. Human-truth-aware: FREEZE/pending/failure outcomes are explicit.
6. Advisory-only: cannot mutate NEXY or override User Law/spec.

## Non-goals
- no runtime authorization;
- no browser/E2E proof;
- no access-token or identity implementation;
- no automatic requirement promotion;
- no inference of missing user intent;
- no edits to NEXY.AI repositories.

## Failure semantics
If HCAS fails, the safe result is `FAIL` with rule IDs. It never auto-patches the manifest and never downgrades a required rule silently.
