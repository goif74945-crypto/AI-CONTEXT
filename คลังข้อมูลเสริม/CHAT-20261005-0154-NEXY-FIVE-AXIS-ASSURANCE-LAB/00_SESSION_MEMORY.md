# Temporary / Resumable Session Memory

Status: EXECUTING
Persistence mode: DURABLE_RESUMABLE
Storage: goif74945-crypto/AI-CONTEXT
Branch: main
Work reference: CHAT-20261005-0154-NEXY-FIVE-AXIS-ASSURANCE-LAB
Platform conversation ID: UNKNOWN / not exposed to this assistant runtime
Created: 2026-10-05T01:54+07:00

## Objective

Create five new, non-NEXY-repository experimental assurance concepts that are useful to NEXY.AI, implement reference code for all five, execute tests, repair failures, preserve Design + Code + Test + Evidence, and keep NEXY.AI repositories read-only.

## Authority

1. Explicit current user directive.
2. AI-CONTEXT/AI-EXECUTION-KERNEL.md.
3. AI-CONTEXT rules and workflows.
4. projects/NEXY.AI context for design compatibility only.
5. Current AI-CONTEXT repository state and executed test evidence.

## Authorized scope

WRITE:
- only this project root under `คลังข้อมูลเสริม/`

READ:
- AI-CONTEXT as needed
- NEXY project context in AI-CONTEXT
- read-only NEXY implementation evidence if needed

## Protected scope

- Any repository whose name contains `NEXY.AI`: NO WRITES.
- Existing sibling supplemental projects: NO MODIFICATION.
- AI-CONTEXT canonical project context/rules: NO MODIFICATION unless explicitly required by this project, which is not currently required.
- Secrets/credentials/private tokens: NEVER persist.

## Observed sibling work that must not be duplicated

Recent AI-CONTEXT inspection found active/implemented sibling work including:
- Evidence Architecture / Context Engine / Agentic Security / Failure Taxonomy / Evals
- NEXY_PREEXEC_PARTIAL_STATE_LAB
- PRIVACY-CONTEXT-FIREWALL
- PRIVACY-EGRESS-FIREWALL
- MULTI-PRINCIPAL-AUTHORITY-LAB
- FREEZE-BRIDGE-LAB
- OPERATOR-CONTRACT-COMPILER
- HUMAN-AGENCY-LAB
- INTENT-INTEGRITY-LAB
- PREFLIGHT-LAB
- PROOF-CAPSULE-COMPILER
- CHRONO-INTEGRITY-LAB
- DETERMINISTIC-INTERCHANGE-KERNEL
- DIRECTIVE-EPOCH-FIREWALL
- CONTEXT-RELEASE-FIREWALL
- SEMANTIC-LOCALIZATION-INTEGRITY-LAB
- ACCESSIBILITY-INTEGRITY-LAB
- TRUST-UX-CONTRACT-LAB
- SUPPLEMENTAL-COLLISION-GUARD
- NEXY Proposal Forge
- NCVG

Non-overlap is proven only against the inspected scope; absence outside that scope is UNKNOWN.

## Five selected experimental concepts

### C1 — Uncertainty Propagation Kernel
Purpose: preserve uncertainty/conflict/staleness across derived claims so downstream layers cannot silently become more certain without explicit proof.

### C2 — Change Impact Frontier
Purpose: map a changed source/module/requirement to impacted tests, evidence, claims and revalidation paths using deterministic dependency closure.

### C3 — Swarm Independence Planner
Purpose: measure structural correlation between candidate agents and select a bounded verification set that minimizes false-independence risk.

### C4 — FSM Composition Guard
Purpose: validate cross-FSM event bridges while keeping each state machine semantically separate and detecting missing references, illegal bridges and event-loop cycles.

### C5 — Provenance-Preserving Context Compressor
Purpose: reduce structured context cost while preserving authority, unresolved conflict, requirement coverage, dependency closure and provenance.

## Integration concept

The five modules form an advisory assurance pipeline:
CHANGE -> IMPACT FRONTIER -> UNCERTAINTY UPDATE -> INDEPENDENT VERIFICATION PLAN -> FSM COMPOSITION CHECK -> PROVENANCE-SAFE CONTEXT HANDOFF

This pipeline is experimental and does not become NEXY authority by existing here.

## Requirements

R1. All five concepts must have explicit design contracts.
R2. All five concepts must have executable reference code.
R3. Production code must be created test-first under the TDD cycle.
R4. Tests must include normal, edge, invalid-input and determinism cases.
R5. No core module may require network, subprocess, wall clock or randomness.
R6. Numeric assurance logic must use bounded integers, not floating-point probability claims.
R7. Canonical outputs must be deterministic for equal canonical inputs.
R8. Failure states must be explicit; no hidden fallback to success.
R9. At least one integration test must exercise all five modules together.
R10. Evidence files must contain actual executed command output.
R11. Final repo write must be read back and verified.
R12. NEXY.AI repositories remain unmodified.

## Planned local verification

- RED: `python -m unittest discover -s tests -v` before implementation
- GREEN: same full suite after implementation
- Static: `python -m compileall -q src tests`
- Policy/static audit: custom verifier scanning core imports and float constants
- Determinism replay: repeated canonical report hashes
- Manifest: SHA-256 of persisted project files

## Current phase

AUTHORITY_SEAL -> BASELINE_VERIFY -> DAG_BUILD -> READY -> EXECUTE_WAVE

Current state: READY / beginning TDD implementation.

## Work DAG

W1 design contracts -> PASS when persisted locally
W2 RED tests for five modules -> depends W1
W3 implement C1 -> depends W2
W4 implement C2 -> depends W2
W5 implement C3 -> depends W2
W6 implement C4 -> depends W2
W7 implement C5 -> depends W2
W8 integration orchestrator -> depends W3-W7
W9 full verification + repairs -> depends W8
W10 evidence + manifest -> depends W9
W11 publish to AI-CONTEXT -> depends W10
W12 read-back + final audit -> depends W11

## Freeze conditions

- target path collision with unrelated existing work;
- implementation requires modifying a NEXY.AI repository;
- authority conflict material to correctness;
- required proof cannot be executed;
- project would need invented external/runtime facts;
- secret or sensitive material would be persisted.

## Resume rule

On resume, read this file, refresh target repo state, inspect latest project files, invalidate stale evidence after code changes, and continue from the first non-PASS work item.
