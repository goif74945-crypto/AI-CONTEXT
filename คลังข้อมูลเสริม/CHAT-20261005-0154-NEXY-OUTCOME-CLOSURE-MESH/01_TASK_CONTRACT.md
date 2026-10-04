# Task Contract — NEXY Outcome Closure Mesh

Status: AI_PROPOSED_CONCEPT / REFERENCE_IMPLEMENTATION / NON_GOVERNING

## Objective
Create five novel, interoperable, deterministic reference systems that close a gap between “engineering activity happened” and “the requested outcome is actually proven, beneficial, and safe to present for human adoption review.”

## Authority
1. Current user directive.
2. AI-CONTEXT execution/security/verification rules.
3. Read-only NEXY authoritative implementation contracts at the observed snapshot.
4. Runtime evidence from this isolated reference project.
5. AI proposal/inference.

No proposal in this directory outranks NEXY authority.

## Scope
### IN SCOPE
- New files only under this task directory in `goif74945-crypto/AI-CONTEXT`.
- Read-only inspection of `goif74945-crypto/NEXY.AI-`.
- Deterministic TypeScript reference implementation.
- TDD, unit, adversarial, integration, demo, collision, compatibility, and persistence evidence.
- Fail-closed design.

### OUT OF SCOPE
- Any mutation to a repository whose name contains `NEXY.AI`.
- Automatic execution of planned probes against external systems.
- Automatic product adoption or canonical promotion.
- Replacing NEXY SystemState, Evidence, Directive, ReleasePolicy, or authority rules.
- Production deployment.

## Immutable requirements
- Unknown critical facts remain unknown.
- Protected-scope mutation causes FREEZE at the adoption boundary.
- Irreversible probes are never selected.
- Reversible writes without rollback are never selected.
- Completion cannot be claimed with UNKNOWN/BLOCKED/PENDING/FAIL obligations.
- Benefit cannot be claimed with missing required observations.
- Adoption output can be at most `READY_FOR_HUMAN_REVIEW`; automatic approval is structurally false.
- Equivalent normalized input ordering must not alter deterministic fingerprints where ordering is semantically irrelevant.

## Required deliverables
- Session/resume memory.
- Collision scan against prior supplemental work.
- Architecture and five concept designs.
- NEXY compatibility boundary.
- Source code.
- Tests.
- RED/GREEN/adversarial/integration evidence.
- Reproducible demo.
- Validation report.
- Manifest.
- Final audit and persistence record.

## Acceptance criteria
1. TypeScript compilation succeeds.
2. All authored tests succeed in a fresh direct run.
3. Integration test crosses all five modules.
4. Adversarial tests cover malformed/unsafe states.
5. No write is performed to NEXY.AI.
6. Target project is persisted only inside the authorized AI-CONTEXT directory.
7. Remote contents are re-read after persistence.
8. No completion claim is made if any critical criterion above lacks evidence.

## Stop conditions
- A required action would mutate NEXY.AI.
- AI-CONTEXT target directory collides with another concurrent task.
- Authority conflict cannot be resolved safely.
- Runtime tests fail and cannot be repaired within the isolated project.
- Remote persistence cannot be verified.
