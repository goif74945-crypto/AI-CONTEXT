# NEXY PREFLIGHT LAB

**Status:** PROPOSAL + reference implementation. Not a NEXY.AI current-build requirement.

NEXY PREFLIGHT LAB is an additive AI-CONTEXT research/reference project for deterministic task admission before an autonomous agent mutates anything.

It answers a narrow question:

> Given a normalized task contract, what actions are admitted, what actions must freeze/block, and what verification obligations must exist before execution can honestly claim success?

The project is deliberately outside the NEXY.AI implementation repository. It does not change current NEXY behavior. It is a future-facing safety/quality tool that can later be evaluated against authoritative NEXY requirements before any integration decision.

## Why this is different from the existing supplemental packs

Existing packs cover evidence graphs, retrieval/context, agentic security, failure taxonomy, eval architecture, and a future research backlog. PREFLIGHT LAB turns several cross-cutting principles into an executable *admission contract* without claiming authority over NEXY.AI.

Its unique focus is the boundary **before mutation**:

`REQUEST → NORMALIZED TASK CONTRACT → PREFLIGHT DECISION → EXECUTION ENVELOPE OR FREEZE`

## Core guarantees of this reference implementation

- deterministic canonicalization and envelope hashing;
- no hidden clock, randomness, network, filesystem, environment, or model calls in the decision core;
- explicit `PASS / FAIL / PARTIAL / BLOCKED / NOT_VERIFIED / UNKNOWN / CONFLICT` vocabulary where applicable;
- protected-scope mutation detection;
- irreversible-action approval gate;
- authority-source completeness checks;
- required evidence-class derivation from declared claim types;
- scope-drift detection between contract revisions;
- stable reason codes designed for machine consumption;
- no optimistic fallback when the contract is materially incomplete.

## Important authority boundary

This repository entry is **ADVISORY**. If it conflicts with DOC-B, DOC-C, current build authority, user law, repository truth, or runtime evidence, it loses. Do not promote this proposal merely because code/tests exist.

## Quick run

```bash
python verify.py
python -m unittest discover -s tests -v
python -m py_compile nexy_preflight.py cli.py
python cli.py fixtures.json  # fixtures.json is a corpus, so use a single extracted contract for CLI runs
```

For a direct CLI run, write one task-contract object from `fixtures.json` to its own JSON file and pass that file to `cli.py`. `verify.py` executes the bundled acceptance corpus directly.

## Layout

- `README.md` — consolidated charter, AI proposal, architecture, contracts, threat model, integration notes, and future research directions.
- `nexy_preflight.py` — pure-Python deterministic reference implementation.
- `cli.py` — single-contract command-line adapter.
- `verify.py` — local compile/unit/acceptance/determinism verification harness.
- `tests/test_nexy_preflight.py` — deterministic unit/regression suite.
- `fixtures.json` — fixed acceptance corpus keyed by fixture name.
- `schemas.json` — task-contract and admission-envelope JSON Schemas.
- `evidence/LOCAL-VERIFICATION.md` — executed local evidence and evidence boundary.
- `evidence/verification-summary.json` — machine-readable verification summary emitted by `verify.py`.
- `MANIFEST.sha256` — SHA-256 inventory for the compact artifact set.
- `SESSION_REFERENCE.md` — non-fabricated work-session reference.
- `WORK-STATE.md` — streaming checkpoint/resumption state.


---

# Project Charter

## OBJECTIVE
Create a deterministic, model-agnostic preflight checker that can reject unsafe or under-specified autonomous work before mutation begins.

## REQUIRED OUTPUT
1. Machine-readable task contract model.
2. Deterministic admission result.
3. Stable reason codes.
4. Verification obligations derived from declared claims/actions.
5. Scope-drift analyzer for revised contracts.
6. Reproducible tests and local execution evidence.

## INPUTS
- Authorized scope.
- Protected scope.
- Proposed operations.
- Declared authority sources.
- Preconditions.
- Approval state.
- Claims expected at completion.
- Evidence already available.

## CONSTRAINTS
- Reference implementation only.
- Standard library only.
- Decision core must be deterministic for equal normalized inputs.
- No network/model/tool calls in core.
- No mutation of NEXY.AI.
- Never upgrade PROPOSAL to current requirement.

## IMMUTABLE REQUIREMENTS
- Protected-scope writes are never silently admitted.
- Irreversible actions without explicit approval are never silently admitted.
- Materially incomplete target/scope/authority fields produce freeze-style outcomes, not guessed defaults.
- Claimed completion evidence must be at least the required evidence class for each claim.
- Contract identity is content-addressed through canonical JSON.

## ACCEPTANCE CRITERIA
- E1: all Python sources compile.
- E2: unit suite passes.
- Deterministic replay: same semantic contract with different key order produces same contract hash and result.
- Negative cases prove protected writes, authority gaps, irreversible actions, evidence shortfall, and unauthorized scope expansion are detected.

## AVAILABLE TOOLS
- AI-CONTEXT GitHub connector for authoritative project context and write-back.
- Isolated local container for implementation/test evidence.

## RISKS
- False authority promotion.
- Accidentally treating path-prefix matching as a security boundary stronger than declared semantics.
- Over-generalizing evidence classes.
- Mistaking static/unit reference evidence for NEXY integration evidence.

## STOP CONDITIONS
- A task requires changing NEXY.AI.
- A project-authority conflict cannot be resolved.
- Verification evidence fails and cannot be repaired.


---

# AI Proposal: Deterministic Preflight Admission Envelope

**Classification:** PROPOSAL generated by AI for evaluation. Not authoritative project law.

## Idea
Before an autonomous agent receives write-