# Task Contract — NEXY Diagnostic Intelligence Mesh

## Classification
**AI-PROPOSED / EXPERIMENTAL / NON-AUTHORITATIVE.**
This work is a standalone reference package in AI-CONTEXT. It does not assert that NEXY.AI implements any concept here.

## Objective
Design, implement, test, and persist five deterministic supplemental engines that improve diagnosability, verification placement, drift detection, and fault containment for future NEXY-compatible systems without modifying NEXY.AI.

## Target
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Write root: `คลังข้อมูลเสริม/CHAT-20261005-0157-NEXY-DIAGNOSTIC-INTELLIGENCE-MESH/`

## Authorized scope
- Create new files only under the write root.
- Read AI-CONTEXT and NEXY project context as evidence/design input.
- Execute authored standalone code/tests in an isolated local environment.
- Use Python 3 standard library only for the reference package.

## Protected scope
- Any repository whose name contains `NEXY.AI`.
- Existing files outside this work root.
- Canonical NEXY law/spec/matrix.
- Production/runtime/deployment resources.
- Secrets, credentials, private data.

## Authority
1. Current user directive.
2. AI-CONTEXT execution/global/security/verification laws.
3. NEXY project context and current authority boundaries.
4. Read-only observations of sibling supplemental labs.
5. This AI-proposed design only where it does not conflict with higher authority.

## Five required engines
### C1 — ODS: Observability Discriminability Synthesizer
Given modeled failure modes and candidate signals, compute a deterministic minimal signal set that distinguishes every failure-mode pair when possible. Indistinguishable pairs must be explicit and must prevent a full PASS claim.

### C2 — CED: Counterexample Distiller
Given a declarative failing witness and declarative violation rules, remove irrelevant witness elements while preserving the same violation code. Output must be inclusion-minimal under the declared evaluator and deterministic.

### C3 — VCPO: Verification Checkpoint Placement Optimizer
Given a workflow DAG, modeled hazard origins, verification checks, and irreversible actions, place the lowest-cost deterministic set of checkpoints such that each covered hazard is detected before the first relevant irreversible descendant. Missing coverage must fail closed.

### C4 — BCSS: Behavioral Canary Set Synthesizer
Given a finite behavior matrix for multiple candidate implementations/providers, compute a minimum diagnostic scenario set that uniquely distinguishes candidates when possible. Behaviorally equivalent candidates must be reported as equivalence classes rather than falsely separable.

### C5 — FCRA: Failure Containment Radius Analyzer
Given a dependency/effect graph plus failed nodes and propagation edges, compute the deterministic impacted closure, safe-to-continue partition, and smallest explicit freeze radius under declared propagation semantics. Unknown references or inconsistent graphs fail closed.

## Immutable invariants
- Equal normalized inputs produce byte-stable canonical outputs.
- No network, wall-clock, randomness, environment, subprocess, eval, or arbitrary user-code execution in library cores.
- No missing/ambiguous input may silently become PASS.
- Every engine emits explicit `PASS`, `FAIL`, or `FREEZE` semantics with reason codes.
- No engine may grant NEXY authority or release/deploy permission.
- Every negative/freeze path is tested.
- Production code follows test-first RED → GREEN for new behavior.
- Exact persisted executable/test files must be read back and matched to the tested content.

## Non-duplication boundary
This mission does not implement:
- generic proof-lattice/evidence-class binding;
- authority conflict compilation;
- replay sealing;
- provider capability admission;
- delta-impact evidence invalidation;
- correlated agent routing;
- generalization boundary gating;
- work portfolio scheduling;
- failure-to-regression compilation;
- evidence independence auditing;
- general FSM consistency checking;
- semantic mutation sensitivity scoring;
- trust/freeze UI presentation.

## Deliverables
1. temporary memory and task contract;
2. design/architecture and requirement ledger;
3. shared deterministic canonicalization utilities;
4. five independently callable Python engines;
5. JSON CLI;
6. unit, negative, determinism, and cross-engine integration tests;
7. fixtures/examples;
8. validation log/evidence report;
9. exact-file hash manifest;
10. final audit and resumption record.

## Required evidence
- E0: GitHub persisted file presence + read-back.
- E1: Python compile/import checks.
- E2: executed unit/negative/determinism tests.
- E3: executed CLI/integration path spanning all five engines.
- Scope audit: writes limited to this mission root.

## Acceptance criteria
- exactly five engines exist and are callable independently;
- each engine has positive + negative/freeze tests;
- full suite passes after any repair;
- deterministic repeat results match;
- CLI integration returns expected machine-readable statuses;
- persisted source/tests hash-match the locally tested bytes;
- no protected repository is mutated.

## Stop conditions
Freeze the affected claim/work if:
- protected-scope mutation is required;
- target repository/branch identity changes materially;
- an authority conflict affects correctness;
- tests cannot be executed;
- persisted bytes cannot be matched to the tested bytes;
- a sibling path collision invalidates isolated ownership.
