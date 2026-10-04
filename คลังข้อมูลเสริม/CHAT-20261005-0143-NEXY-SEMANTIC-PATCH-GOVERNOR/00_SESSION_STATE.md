# Session State — NEXY Semantic Patch Governor

- work_tag: `CHAT-20261005-0143-NEXY-SEMANTIC-PATCH-GOVERNOR`
- platform_chat_id: `UNKNOWN`
- platform_chat_id_note: The available tools do not expose an immutable ChatGPT conversation ID. This deterministic work tag is the durable session identifier; no platform ID is invented.
- local_time_anchor: `2026-10-05T01:43+07:00`
- persistence_mode: `DURABLE_RESUMABLE`
- storage_repository: `goif74945-crypto/AI-CONTEXT`
- writable_scope: `คลังข้อมูลเสริม/CHAT-20261005-0143-NEXY-SEMANTIC-PATCH-GOVERNOR/**`
- classification: `AI_PROPOSED_FUTURE_CONCEPT / RESEARCH_PROTOTYPE / NOT_NEXY_CANON / NOT_INTEGRATED`

## Mission objective

Design, implement, test, adversarially verify, and preserve a standalone deterministic Semantic Patch Governor that can interoperate with NEXY.AI through future adapters without modifying any repository whose name contains `NEXY.AI`.

The prototype governs an actual candidate code patch against a structured task contract before application or merge. It binds every changed file/hunk to authorized scope and explicit justification, freezes on protected or unexplained mutation, escalates sensitive surfaces, estimates deterministic mutation/blast-radius cost, and can select the least-authority legal candidate from multiple proposed patches.

## Authority and source facts

### SOURCE_FACT
- AI-CONTEXT requires Task Contracts, hard scope boundaries, evidence-matched PASS claims, fail-closed handling of material ambiguity, and durable checkpoints for long work.
- Current NEXY context defines NEXY as a deterministic control hub with verified-output-or-freeze behavior; design, implementation, runtime, and deployment are separate truth domains.
- The current normalized NEXY source matrix contains 837 normalized requirement rows and explicitly marks implementation as not verified by that matrix.

### REPO_FACT
- AI-CONTEXT `main` was observed at `13367411f8a8ba9904f5abf9a561cf190a89ac5c` before this project write.
- `goif74945-crypto/NEXY.AI-` branch `NEXY.ai` was observed read-only at `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- NEXY.AI- `AGENTS.md` states that protected branches/paths must not be mutated outside explicit task scope.
- Searches in AI-CONTEXT found no direct hit for `semantic patch governor`, `unexplained hunk`, `patch minimality`, `diff scope protected path`, or `requirement to diff`.
- Adjacent supplemental projects already cover side-effect transactions, effect contracts, collision/orthogonality admission, causal merge, context delta, proof systems, and tool-contract drift.

### INFERENCE
There is a useful orthogonal gap between declaring a task's allowed mutation surface and mechanically proving that an actual proposed unified diff stays inside it. This prototype targets that gap.

### UNKNOWN / NOT VERIFIED
- No claim is made that NEXY.AI currently lacks every equivalent semantic mechanism; repository search is not a formal proof of absence.
- No NEXY.AI integration, runtime, deployment, or product benefit has been verified.
- User preference/impact is a design hypothesis until measured in a real integration.

## Scope lock

### IN SCOPE
- deterministic unified-diff parsing and normalization;
- task-contract scope and protected-surface enforcement;
- change-justification binding to file/hunk/requirement IDs;
- sensitive-surface risk classification;
- mutation budget and blast-radius scoring;
- fail-closed malformed/binary/ambiguous patch handling;
- least-authority candidate ranking;
- deterministic decision/fingerprint certificate;
- JSON/CLI boundary;
- schemas, fixtures, tests, benchmark/evidence, design and integration guidance;
- future ideas clearly labeled as AI proposals.

### PROTECTED / OUT OF SCOPE
- every repository whose name contains `NEXY.AI`: READ/ANALYZE ONLY;
- no writes, branches, commits, merges, PRs, issues, workflows, settings, renames, deletes, or pushes in NEXY.AI repositories;
- no production deployment;
- no claim of canonical NEXY law;
- no execution of arbitrary candidate patch content;
- no credentials/secrets;
- no mutation outside this project folder in AI-CONTEXT.

## Core invariants

1. Identical canonical inputs produce byte-stable semantic verdict data.
2. Any protected-path mutation freezes.
3. Any changed file/hunk lacking required justification freezes when justification mode is strict.
4. Path traversal, malformed headers, ambiguous rename metadata, and unsupported binary diffs freeze.
5. Risk/scope decisions never depend on model prose or floating-point randomness.
6. Candidate ranking never allows a lower-cost illegal patch to beat a legal patch.
7. The prototype never applies patches; it only analyzes and certifies/refuses them.
8. NEXY.AI repositories remain unchanged by this mission.
9. PASS claims require matching E1/E2/E3 evidence from exact published bytes where feasible.

## Planned deliverables

- `00_SESSION_STATE.md`
- `00_TASK_CONTRACT.json`
- `01_CONCEPT_AND_NOVELTY.md`
- `02_ARCHITECTURE.md`
- `03_REQUIREMENT_LEDGER.md`
- `04_INTEGRATION_CONTRACT.md`
- `05_FAILURE_MODEL.md`
- `06_IMPLEMENTATION_PLAN.md`
- `07_AI_PROPOSED_FUTURE_IDEAS.md`
- `README.md`
- `schemas/*.schema.json`
- `src/**`
- `tests/**`
- `fixtures/**`
- `EVIDENCE.md`
- `EXECUTION_RECORD.json`
- `FINAL_AUDIT.md`
- `MANIFEST.sha256`

## Work DAG

`CONTEXT_LOCK -> NOVELTY_GATE -> DESIGN -> TEST_RED -> IMPLEMENT -> TEST_GREEN -> ADVERSARIAL -> STATIC -> INTEGRATION -> PUBLISH -> READ_BACK -> RETEST_PUBLISHED_BYTES -> FINAL_AUDIT`

## Current state

- CONTEXT_LOCK: PASS
- NOVELTY_GATE: PASS with limitation that search cannot prove absolute absence
- DESIGN: IN_PROGRESS
- IMPLEMENTATION: NOT_VERIFIED
- TESTS: NOT_VERIFIED
- PUBLICATION: PARTIAL (this checkpoint only)
- FINAL_AUDIT: NOT_VERIFIED

## Next legal action

Create the local isolated reference implementation using TDD, execute static/unit/integration/adversarial verification, repair failures, then publish only verified artifacts into this folder and read them back.

## Stop / freeze conditions

- any required write to a repository containing `NEXY.AI`;
- any required write outside this project folder;
- material authority conflict that cannot be resolved;
- inability to prove a required implementation claim;
- test failure that cannot be safely repaired inside this standalone project;
- evidence mismatch between locally tested and published source bytes.
