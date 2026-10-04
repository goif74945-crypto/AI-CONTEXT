# NEXY Oracle Forge — Execution State

## Identity
- Mission ID: `NEXY-ORACLE-FORGE-20261005-0125`
- Conversation identifier: `PROJECT-CONVERSATION-2026-10-05T01:25+07:00`
- Identifier note: the ChatGPT UI internal chat ID is not exposed to the available tools; this deterministic project-conversation identifier is used instead.
- Repository: `goif74945-crypto/AI-CONTEXT`
- Target folder: `คลังข้อมูลเสริม/CHAT-20261005-0125-NEXY-ORACLE-FORGE`
- Branch: `main`
- Persistence mode: `DURABLE_RESUMABLE`
- Status: `IN_PROGRESS`

## Objective
Design, implement, test, audit, and persist a new executable supplemental project useful to future NEXY.AI development without mutating any repository whose name contains `NEXY.AI`.

## Selected project
`NEXY Oracle Forge` — a deterministic requirement-to-test-oracle compiler that rejects/freeze-classifies underspecified requirements instead of inventing expected behavior.

## Deduplication evidence
Repository code search returned zero results for:
- `test oracle`
- `oracle compiler`
- `metamorphic`
- `property-based`
- `test synthesis`
- `requirement to test`
- `mutation testing`
- `scenario generator`

This does not prove metaphysical uniqueness; it proves no indexed matching implementation was found in AI-CONTEXT at the time of inspection.

## Scope lock
### IN SCOPE
- Create files only under this mission folder in `AI-CONTEXT/คลังข้อมูลเสริม/`.
- Design an AI-proposed concept clearly labeled experimental/proposal.
- Implement a standalone Python 3.11+ standard-library CLI/library.
- Define deterministic schemas and validation.
- Generate positive/negative test obligations and traceability artifacts from explicit requirement contracts.
- Reject or freeze requirements that lack an executable oracle contract.
- Add unit/integration tests and deterministic-output checks.
- Run tests in an isolated local runtime against the exact authored file contents.
- Read back all committed files and verify identity/content.

### PROTECTED / OUT OF SCOPE
- Any mutation to a repository whose name contains `NEXY.AI`.
- Any claim that this proposal is canonical NEXY law.
- Any claim that generated test obligations prove NEXY implementation behavior.
- Any deployment, production mutation, secret handling, credential storage, or destructive Git operation.
- Editing unrelated existing files in `คลังข้อมูลเสริม`.

## Authority
1. Current explicit user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`, `rules/MEMORY.md`.
4. NEXY project authority boundary and current 837-row source-normalization rule.
5. Exact repository/tool/runtime evidence.
6. AI proposal/inference.

## Truth boundary
- SOURCE_FACT: NEXY favors deterministic, evidence-first, freeze-on-ambiguity control.
- REPO_FACT: Current source normalization uses 837 rows; legacy 215-entry registry is deprecated for current counting.
- REPO_FACT: no indexed matches were found for the dedupe search terms above.
- PROPOSAL: Oracle Forge architecture, schema, algorithms, and integration model.
- RUNTIME_FACT: none yet; tests have not yet been executed.
- NOT_VERIFIED: implementation correctness until E1/E2/E3 evidence is produced.

## Work DAG
- W01 authority + dedupe baseline — PASS
- W02 task contract + durable checkpoint — IN_PROGRESS
- W03 architecture/specification — PENDING
- W04 implementation — PENDING
- W05 unit tests — PENDING
- W06 CLI integration test — PENDING
- W07 determinism/negative-path tests — PENDING
- W08 repository write/read-back verification — PENDING
- W09 final audit + execution record — PENDING

## Invariants
1. Same normalized input + compiler version => byte-stable canonical JSON bundle.
2. No expected behavior may be invented from missing data.
3. Ambiguous/underspecified executable oracle fields => deterministic FREEZE classification.
4. Generated IDs/hashes are content-derived, not random.
5. Input order must not alter canonical output semantics.
6. The tool emits obligations, not false implementation PASS claims.
7. No network, model call, telemetry upload, or external dependency is required.

## Next legal action
Create the schema/spec and implementation locally, execute verification, then persist only verified content into this mission folder.

## Resume rule
On resume: re-read this file, root `INDEX.md`, `AI-EXECUTION-KERNEL.md`, verify the target folder current state, then continue from the first non-PASS work item. Do not assume prior unverified work succeeded.
