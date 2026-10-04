# NEXY Proof Sensitivity Lab — Temporary Execution Memory

## Identity
- Mission ID: `NEXY-PROOF-SENSITIVITY-LAB-20261005-0142`
- Conversation identifier: `PROJECT-CONVERSATION-2026-10-05T01:42+07:00`
- Chat-ID note: the internal ChatGPT UI chat identifier is not exposed to the available tools. The deterministic project-conversation identifier above is used as the durable conversation handle.
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Target folder: `คลังข้อมูลเสริม/CHAT-20261005-0142-NEXY-PROOF-SENSITIVITY-LAB`
- Persistence mode: `DURABLE_RESUMABLE`
- Execution mode: `ACTIVE_SYNC + LOGICAL_ISOLATION`
- Status: `IN_PROGRESS`

## Objective
Design, implement, test, audit, and persist a new executable supplemental project that can improve future NEXY.AI assurance without modifying any repository whose name contains `NEXY.AI`.

## Selected project
**NEXY Proof Sensitivity Lab (NPSL)** — an AI-proposed, non-canonical, deterministic semantic-mutation analyzer for measuring whether a declared proof/assertion suite is sensitive to explicitly declared requirement regressions.

The core question is:
> If a protected contract is weakened in a known dangerous way, do the declared proofs actually fail?

A mutant that is detected is **KILLED**. A non-equivalent mutant that still satisfies every declared proof is **SURVIVED** and represents a bounded proof-gap finding.

## Deduplication baseline
Repository path-tree inspection and GitHub code-search queries were performed for:
- `mutation testing`
- `mutant kill`
- `semantic mutant`
- `test adequacy`
- `proof sensitivity`
- `evidence sensitivity`

Observed result: no matching implementation was returned for those terms in the inspected AI-CONTEXT search surface.

Related but distinct existing work observed:
- `05_MUTATION_SAFETY.md` concerns safe state mutations, not mutation testing.
- `NEXY Oracle Forge` compiles requirement-to-test oracles and is currently marked IN_PROGRESS.
- adversarial-oracle and metamorphic-testing notes exist, but no semantic-mutant kill-score implementation was observed in the inspected scope.

This is bounded deduplication evidence, not a universal proof that no semantically similar idea exists anywhere.

## Scope lock
### IN SCOPE
- Create new files only under this mission folder.
- Standalone Python 3.11+ standard-library implementation.
- Explicit JSON contract input.
- Deterministic JSON Pointer access.
- Declarative proof assertions.
- Explicit semantic mutation operators.
- Mutation execution and KILLED / SURVIVED / EQUIVALENT / INVALID_MUTANT classification.
- Fail-closed baseline validation.
- Deterministic canonical JSON + SHA-256 digests.
- CLI integration.
- Unit, integration, deterministic-output, negative-path, and bounded adversarial tests.
- Design, failure model, integration contract, evidence, and resume state.

### PROTECTED / OUT OF SCOPE
- Any write to any repository whose name contains `NEXY.AI`.
- Any claim that NPSL is canonical NEXY law.
- Any claim that a bounded mutation score proves universal correctness or security.
- Arbitrary command execution from mutation specifications.
- Network/model calls from the reference implementation.
- Secrets, credentials, production mutation, deployment, or destructive Git actions.
- Editing existing supplemental projects or shared index files.

## Authority
1. Current explicit user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. NEXY project authority boundary and current 837-row source-normalization rule.
5. Exact repository/tool/runtime evidence.
6. AI proposal/design inference.

## Truth boundary
- SOURCE_FACT: NEXY is evidence-first, freeze-on-ambiguity, deterministic-by-design, and separates design from implementation evidence.
- REPO_FACT: current source normalization uses 837 rows; the legacy 215-entry registry is deprecated for current counting.
- REPO_FACT: the related artifacts listed above were observed in AI-CONTEXT.
- PROPOSAL: NPSL architecture, algorithms, schemas, operators, and future integration model.
- RUNTIME_FACT: none yet at this checkpoint.
- NOT_VERIFIED: implementation correctness until executed tests produce matching evidence.

## Work DAG
- W01 authority/context/deduplication baseline — PASS
- W02 durable mission checkpoint + task contract — PASS
- W03 architecture + requirement ledger — IN_PROGRESS
- W04 TDD RED tests — PASS
- W05 implementation GREEN — PASS
- W06 refactor + static validation — PASS
- W07 focused/unit/integration/determinism tests — IN_PROGRESS
- W08 independent review/security/truth audit — PENDING
- W09 repository write + read-back verification — PENDING
- W10 final audit/completion certificate — PENDING

## Invariants
1. Same normalized input + implementation version => byte-stable canonical result.
2. Core engine performs no network, shell, model, clock, random, or environment-dependent behavior.
3. Baseline proof suite must pass before mutants are scored; otherwise analysis FREEZEs.
4. Mutation intent is explicit. Missing mutation values are not guessed.
5. Invalid mutation paths/operators are surfaced, never silently repaired.
6. Equivalent mutants are excluded from the eligible score denominator.
7. A SURVIVED mutant is a bounded finding, not proof of an implementation bug.
8. Killing all declared mutants proves only sensitivity to the declared bounded mutant corpus.
9. IDs/digests are deterministic and content-derived.
10. Output ordering is deterministic and independent of proof/mutant input order when IDs and semantics are unchanged.
11. No existing file outside this mission folder is modified.

## Next legal action
Finalize the architecture and tests locally, execute the RED phase, implement the minimum complete engine, execute GREEN/regression verification, then persist the exact tested content into this folder and read it back.

## Resume rule
On resume: read this file, root `INDEX.md`, `AI-EXECUTION-KERNEL.md`, re-check the target folder and latest commit, then continue from the first non-PASS work item. Never promote planned/unverified work to fact.


## Checkpoint — implementation wave 1
Observed local verification against the current authored workspace contents:
- Python test suite: 42 tests PASS after multiple RED→GREEN cycles.
- Static compile: `python -m compileall -q src tests` exited successfully.
- Deterministic malformed-input sweep: 1,000 generated malformed/invalid inputs; 0 unhandled exceptions; all 1,000 returned FREEZE.
- Import audit over `src/**/*.py`: no imports of socket, requests, urllib, httpx, subprocess, random, secrets, or time.
- Confirmed repaired hostile-input defects: unknown fields, irrelevant fields, invalid metadata types, non-finite JSON values, numeric overflow, duplicate JSON keys, non-standard NaN literal, huge array indices, cyclic programmatic input, and raw declared-mutant denominator accounting.
- Runtime claims above are local E1/E2 observations only. Repository persistence/read-back and final integration evidence remain pending.

### Current next action
Finish architecture/integration/threat-model documents and examples, run final E1/E2/E3 regression against the frozen local artifact set, then persist the exact tested contents into this mission folder and read them back.
