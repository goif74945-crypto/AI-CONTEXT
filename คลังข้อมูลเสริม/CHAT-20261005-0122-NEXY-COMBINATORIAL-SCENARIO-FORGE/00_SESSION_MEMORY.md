# Temporary Execution Memory — NEXY Combinatorial Scenario Forge

Status: EXECUTING
Durable work code: CHAT-20261005-0122-NEXY-COMBINATORIAL-SCENARIO-FORGE
Platform-native ChatGPT conversation ID: UNKNOWN_NOT_EXPOSED_BY_AVAILABLE_TOOLS
Started local: 2026-10-05T01:22:00+07:00
Target repository: goif74945-crypto/AI-CONTEXT
Target branch: main
Observed starting HEAD: 4d90bdcf33e070ef096d2890ea9f98b94ffb2090

## Objective
Design, implement, execute, test, and document an additive standalone R&D tool useful to NEXY without modifying any repository whose name contains "NEXY.AI".

Selected AI-proposed concept: NEXY Combinatorial Scenario Forge (NCSF).

NCSF compiles a finite declarative test space into deterministic positive and negative scenarios with exact finite-domain interaction coverage evidence. Its purpose is to turn state/role/action/configuration laws into reusable test fixtures instead of relying only on manually written examples.

## Authority loaded
1. Current user directive.
2. AI-CONTEXT/AI-BOOTSTRAP.md.
3. AI-CONTEXT/INDEX.md.
4. AI-CONTEXT/AI-EXECUTION-KERNEL.md.
5. AI-CONTEXT/WORK-ROUTER.md.
6. rules/GLOBAL.md, SECURITY.md, VERIFICATION.md, AI-BEHAVIOR.md.
7. workflows/project-start.md, research.md, system-design.md, implementation.md, verification.md, memory-update.md.
8. projects/NEXY.AI/overview.md.
9. projects/NEXY.AI/deep/INDEX.md, human-control-surface.md, constitutional-locks.md, doc-c-vnext-build-spec.md.
10. projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md.

## Source-grounded NEXY facts relevant to this lab
- NEXY current build law separates specification, implementation, runtime, and deployment evidence.
- DOC-C defines finite states, roles, error classes, FSM transitions, release gates, RBAC, queue and test-gate obligations.
- Current exhaustive normalized source denominator is 837 requirement rows; that matrix is source normalization and not implementation proof.
- One legal verified output or FREEZE is a core behavioral boundary.
- Critical behavior requires negative-path proof, not only happy-path examples.

## De-duplication evidence
A recursive AI-CONTEXT path scan found existing work for assurance, epistemic control, verification, counterfactual analysis, reliability, clarification optimization, experience compilation, human-authority handling and operator contracts.
Path/content searches returned no dedicated "combinatorial", "pairwise", "covering array", "fuzz", or "scenario generator" implementation.
Therefore this mission targets test-space generation rather than another verifier or policy engine.

## Scope lock
IN SCOPE:
- New files only under `คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-COMBINATORIAL-SCENARIO-FORGE/`.
- Architecture, contracts, Python standard-library reference implementation, CLI, fixtures, tests, validation evidence, adoption proposal, research backlog and final audit.
- Read-only use of canonical NEXY context for representative fixtures.

PROTECTED / OUT OF SCOPE:
- Any mutation to a repository whose name contains "NEXY.AI".
- Any mutation to existing sibling supplemental work.
- Promotion of this proposal into canonical NEXY law/build scope.
- Claims that NCSF is integrated, deployed, or currently running in NEXY.
- Secrets, credentials, personal data, hidden model reasoning.
- Destructive Git operations or force-push.

## Required behavior
- Deterministic canonical output for equivalent normalized input.
- Structured constraint DSL only; no eval/exec.
- Exhaustive finite-domain enumeration bounded by explicit safety limits.
- Positive scenario generation with exact t-way interaction coverage over valid assignments.
- Stable deterministic greedy set-cover reduction.
- Negative scenario generation that violates exactly one constraint while satisfying all others when such a witness exists.
- Stable scenario IDs derived from canonical JSON.
- Explicit BLOCKED/FAIL behavior for invalid schemas, unsatisfiable spaces, excessive search space, impossible requested coverage, or scenario budget insufficiency.
- Machine-readable coverage report including numerator, denominator and uncovered interactions.
- No guessed values.

## Verification target
E0: committed files re-fetched from AI-CONTEXT.
E1: Python compilation + JSON fixture parsing + deterministic static validation.
E2: executed unit/negative/determinism/coverage tests in isolated local workspace.
No E3/E4/E5/E6 claim about NEXY.AI.

## Planned deliverables
1. README / manifest.
2. Task contract.
3. Architecture and algorithm spec.
4. Data-contract/schema documentation.
5. Python package implementation.
6. CLI.
7. representative NEXY control-surface fixture marked as test fixture, not runtime truth.
8. adversarial/edge fixtures.
9. unit and property-oriented deterministic tests.
10. validation script.
11. requirement/evidence ledger.
12. adoption proposal.
13. research backlog.
14. validation report.
15. final audit/resume capsule.

## Current execution state
COMPLETED:
- Boot/kernel/router/rules/workflows read.
- NEXY canonical context read for the relevant boundaries.
- Supplemental tree de-duplication scan performed.
- Mission direction selected and scope locked.

IN PROGRESS:
- Reference implementation and local test suite.

NEXT:
1. Build local artifact set.
2. Execute compile/tests.
3. Repair failures.
4. Re-run full validation.
5. Atomically persist verified artifacts to this directory.
6. Re-fetch persisted files and exact commit.
7. Final truth audit.

## Stop / freeze conditions
FREEZE if a required write would leave authorized directory, if branch drift cannot be safely reconciled, if validation cannot be executed, if a path collision appears, or if correctness would require inventing NEXY behavior not supported by the loaded authority.
