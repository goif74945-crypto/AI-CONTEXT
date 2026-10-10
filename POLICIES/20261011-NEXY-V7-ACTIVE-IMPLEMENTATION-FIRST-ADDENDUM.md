# NEXY V7 active implementation-first execution rules

**STATUS:** Active coordination addendum for participating authorized Codex builders (2026-10-11).
**PRECEDENCE:** Original SHA-verified NEXY-IGNIS DOCX + Product AGENTS.md + explicit authorized user constraints always override this throughput guidance. Existing \`POLICIES/20261010-NEXY-EVIDENCE-GATED-CONTINUOUS-UPDATE-V1.md\` remains active. No policy alone operates an unattended agent.

## 1. Mandatory engineering output
- An active builder must preferentially produce **a real tested source correction** for a verified and authorized in-scope defect/requirement. Reporting/spec mapping/test-design does not replace implementation if READY work exists.
- Each completed iteration should contain at least one of:
  - \`VERIFIED_CHANGE\` (committed source and test fix at current Product HEAD, with proof);
  - \`PROVEN_COMPLIANT\` (no edit needed, with runtime proof and precise spec atom);
  - \`REPRODUCIBLE_DEFECT\` (red test and minimal fail case, with next fix action);
  - \`BLOCKED_WITH_ALTERNATE_PROGRESS\` (real blocker + independent completed checks).
- A response that only says "will do", contains only a new speculative roadmap, or invents PASS without executable evidence is an invalid engineering iteration.

## 2. Capacity management
- Parallelize isolated reads and tests where resource budget permits; serialize all Product repository mutations and remote HEAD advancement.
- Maintain explicit \`READY / RUNNING / VERIFYING / DONE / FAILED / FROZEN\` per atomic task. Bound work in progress by actual runner capability; never create hundreds of concurrent jobs merely to look busy.
- Stop repeating equivalent tool failures without changing the diagnostic approach. After 2 indistinguishable failed attempts, classify failure and move to an independent READY task if available.
- Reuse frozen \`NAVIGATION/20261010-NEXY-IGNIS-SPEC-TO-CODE-ATLAS-V1.tsv\` and 889-file manifest as indexing hints. Validate new HEAD with exact Git blobs to avoid unnecessary full rediscovery; still read actual original spec and full source as necessary.
- Before final handoff, reconcile job results to the actual checked HEAD and artifact hashes. Persist temporary memory and append clean evidence to AI-CONTEXT.

## 3. Testing quality floor
- A code fix must have meaningful RED evidence where feasible, GREEN proof, affected contract/integration regression, negative/adversarial cases, and build/lint/typecheck as applicable.
- P0 security and storage changes require auth and concurrency abuse checks, state persistence/rollback tests as appropriate, and no weakening of fail-closed release controls.
- Re-run dependent tests when changed code or interface affects them. Distinguish test assertion failures, runner failures, infrastructure blocks, and unavailable external signoffs.
- Mark an entire subsystem \`VERIFIED\` only with current-HEAD behavioral evidence, not 1 smoke-test pass or a source path match.
- All test results must include actual invocation, environment, exit code, exact HEAD, artifact reference; unknowns remain explicit.

## 4. Source update continuity
- Continue actual READY engineering work in the active Codex session without asking for "continue" after each small slice when permissions suffice.
- **No arbitrary time-interval commits**. Source code is updated only for true spec-conformant fixes and independently useful tests; zero source diffs are acceptable when evidence shows compliant code.
- Product mutation is confined to existing \`NEXY.ai\`, with current remote HEAD CAS, no branch/fork creation, no history rewrite, no destructive operation without explicit owner authorization.
- If Codex's environment requires a new branch, stop that workflow and use only an authorized existing-branch-compatible executor.
- A persistent 24/7 system requires separately configured and acknowledged automation; this policy does not claim continuous background execution by itself.

## 5. Review gates & stop behavior
- Independent review is encouraged; a reviewer must not be mistaken for a separate writer with inherited Product write rights.
- On missing spec SHA, contested requirement, unsafe data access, stale competing HEAD, or unapproved production execution, **FREEZE affected action**, preserve other unrelated safe READY engineering.
- Exit only at actual session, budget, resources, permission, irreducible dependency or safety stop. Persist next exact executable action for resumption.
- Never claim 100% until all in-scope original DOC-C atoms, supported DOC-D and applicable storage/auth requirements, full runnable verification and mandatory DOC-E E1–E12 approvals are independently proven.

**Required start:** \`START-HERE-NEXY-IGNIS-CODEX-20261010.md\` → \`COMMANDS/20261011-NEXY-CODEX-MAX-ENGINEERING-THROUGHPUT-V7.md\` → work queue → original DOCX + live HEAD.
