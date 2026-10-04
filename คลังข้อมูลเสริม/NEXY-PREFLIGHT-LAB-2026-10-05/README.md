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
Before an autonomous agent receives write-capable tools, compile the user's task contract into a deterministic **Preflight Admission Envelope**.

The envelope does not decide *how clever* the agent should be. It decides whether the proposed work is sufficiently scoped and authorized to proceed, and which proof obligations must be satisfied before completion can be asserted.

## Intended future value
- stop scope creep before it becomes repository drift;
- make protected-path rules machine-checkable;
- separate “allowed to execute” from “able to execute”;
- make evidence debt visible before work starts;
- enable replay/audit of why a write was admitted;
- catch approval requirements before destructive actions are queued;
- compare contract revisions and detect unauthorized expansion.

## Non-goals
- replace NEXY::LAW or NEXY::JUDGE;
- interpret natural-language requirements with model authority;
- infer missing user approval;
- prove real NEXY integration or deployment;
- define current NEXY build scope.

## Possible future integration hypothesis
If later promoted by authoritative NEXY specifications, a preflight envelope could sit between task normalization and tool-capability issuance:

`USER REQUEST → TASK NORMALIZER → PREFLIGHT → CAPABILITY GRANT → EXECUTION → VERIFICATION`

This is only a hypothesis. Integration requires source-authority promotion and implementation-specific design review.


---

# Architecture

## 1. Components

### Contract model
Typed dataclasses and enums represent task identity, scopes, operations, claims, evidence, and approvals.

### Canonicalizer
Produces canonical JSON with sorted keys and compact separators, then SHA-256. No timestamps are injected into the decision identity.

### Admission engine
Evaluates normalized invariants in a fixed order and emits stable findings. Decision priority is deterministic:

`CONFLICT > FAIL > BLOCKED > NOT_VERIFIED > PASS`

`FAIL` is reserved for a proved negative assertion/test result rather than a missing prerequisite in this preflight model.

### Verification planner
Maps claim categories to minimum evidence classes and reports evidence gaps.

### Drift analyzer
Compares a baseline and candidate task contract. It detects additions to write scope, protected-scope weakening, newly irreversible operations, removed authority sources, and relaxed approvals.

### CLI
Reads a JSON contract and prints a machine-readable admission envelope.

## 2. Determinism boundary
The core must not read:
- current time;
- randomness;
- network;
- environment variables;
- filesystem state beyond caller-provided input;
- process state;
- model output.

The CLI performs file I/O only to obtain the explicit input document.

## 3. Decision phases
1. Structural normalization.
2. Target identity checks.
3. Scope checks.
4. Protected-scope checks.
5. Authority checks.
6. Approval/irreversibility checks.
7. Verification-obligation checks.
8. Canonical envelope sealing.

## 4. Scope matching
The reference implementation uses normalized slash-separated logical paths and repository identifiers. Prefix matching is boundary-aware (`a/b` matches `a/b/c`, not `a/bad`).

This is a policy utility, not a filesystem sandbox. Production use would need repository-aware canonical identities and symlink/path-resolution controls at the actual capability boundary.

## 5. Result semantics
- `PASS`: preflight prerequisites represented by the contract are satisfied.
- `FAIL`: matching executed evidence proves a declared completion claim failed.
- `BLOCKED`: explicit prerequisite/approval is missing.
- `NOT_VERIFIED`: execution may be admissible but declared completion claims do not yet have sufficient evidence.
- `CONFLICT`: mutually incompatible authority/scope declarations are present.

A PASS here never means the requested task itself has been executed.


---

# Contract Specification

## Input skeleton

```json
{
  "task_id": "TASK-001",
  "objective": "Create additive documentation",
  "target": "goif74945-crypto/AI-CONTEXT",
  "authorized_scope": ["คลังข้อมูลเสริม/demo"],
  "protected_scope": ["goif74945-crypto/NEXY.AI-"],
  "authority_sources": ["user-directive", "AI-CONTEXT/rules/GLOBAL.md"],
  "preconditions": ["target-exists"],
  "operations": [
    {"kind": "write", "resource": "คลังข้อมูลเสริม/demo/README.md", "irreversible": false}
  ],
  "claims": [
    {"id": "C1", "kind": "static", "text": "Python sources compile"}
  ],
  "evidence": [
    {"claim_id": "C1", "class": "E1", "result": "PASS", "artifact": "compile.log"}
  ],
  "approvals": []
}
```

## Evidence class order
`E0 < E1 < E2 < E3 < E4 < E5 < E6 < E7`

Claim-type minimums in this reference model:
- presence → E0
- static/type/schema → E1
- unit behavior → E2
- integration → E3
- end-to-end user flow → E4
- runtime/recovery/performance → E5
- deployment → E6
- physical/hardware → E7

Unknown claim kinds do not guess. They require explicit evidence policy and therefore produce `BLOCKED` with `PFL-EVIDENCE-POLICY-UNKNOWN`.

## Stable reason codes
- `PFL-TARGET-MISSING`
- `PFL-SCOPE-MISSING`
- `PFL-SCOPE-OUTSIDE`
- `PFL-PROTECTED-WRITE`
- `PFL-AUTHORITY-MISSING`
- `PFL-APPROVAL-MISSING`
- `PFL-CLAIM-DUPLICATE`
- `PFL-EVIDENCE-ORPHAN`
- `PFL-EVIDENCE-POLICY-UNKNOWN`
- `PFL-EVIDENCE-MISSING`
- `PFL-EVIDENCE-INSUFFICIENT`
- `PFL-EVIDENCE-FAILED`
- `PFL-DRIFT-WRITE-EXPANDED`
- `PFL-DRIFT-PROTECTION-RELAXED`
- `PFL-DRIFT-IRREVERSIBLE-ADDED`
- `PFL-DRIFT-AUTHORITY-REMOVED`
- `PFL-DRIFT-APPROVAL-REMOVED`


---

# Threat Model

## Assets
- user authority;
- protected repository boundaries;
- task-scope integrity;
- completion truthfulness;
- evidence provenance;
- reversible execution plans.

## Threats
1. **Scope laundering**: candidate operation is phrased differently but mutates outside authorized scope.
2. **Protected mutation**: write/delete/deploy operation targets protected repository/path.
3. **Approval inference**: destructive action proceeds because approval is assumed from context.
4. **Evidence laundering**: E1/static result is presented