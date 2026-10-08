# TASK — NEXY Codex Next Command 004 Closeout

TASK_ID: 20261008-NEXY-CODEX-NEXT-COMMAND-004
VERSION: 1
MODE: CROSS / AUDIT / COMMAND_ENGINEERING
FINAL_STATUS: VERIFIED_WITH_LIMITS
TITLE: Issue next Codex execution command with spec authority, time-boundary, and sandbox verification

SCOPE:
- Audit Codex's previous PARTIAL report and current AI-CONTEXT status matrix.
- Verify uploaded authoritative specification SHA-256 and record relevant paragraph locators.
- Prepare and adversarially review executable next command for Codex.
- Persist coordination records in AI-CONTEXT/main only.
OUT_OF_SCOPE:
- Modify NEXY.AI- product repository in this task.
- Claim current runtime PASS, release approval, or deployment readiness.

INPUTS / SOURCES:
- Product repository: goif74945-crypto/NEXY.AI-, branch NEXY.ai, observed HEAD 8b406a63f10aa1424225a80453393af2e4cb78b5.
- AI-CONTEXT main observed before this command's writes: 2e27e349e8dd3f6ae3c250588f11d8d31b9fd8da.
- User-provided Codex PARTIAL report, 98-row matrix, and original DOCX attachment.
- Spec exact SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (verified from uploaded bytes).
- EVIDENCE/20261008-NEXY-CONTINUOUS-REPAIR-EXECUTION-003.tsv and corresponding task report.

CURRENT CLAIMS / PROOFS:
- Current matrix baseline: total=98, verified=14, partial=9, mismatch=4, not_verified=62, spec_source_blocked=4, infra_blocked=5.
- Substantive review reported as 39/98; coverage/classification is 98/98.
- Uploaded authoritative DOCX SHA matches required hash.
- Verified DOCX distinguishes DOC-C build obligation and DOC-E deployment approval.
- Current source has queue dispatch dependence on currentTsaBatchTimeMs(); source search for production injection found definition and test callers but no confirmed production caller. This is a candidate integration gap, not a proved absence.
- Linux bwrap source at observed HEAD binds selected /usr,/lib,/lib64,/etc/ssl roots; prior experimental test report describes an executable under /opt inaccessible to bwrap. Current-run reproduction required.

ACTIONS:
1. Read current product and control HEADs and their relevant current source.
2. Inspect hash-verified DOCX and extract authority / scope / time / sandbox / release source locators.
3. Design next executable command with fail-closed, no-fake-pass, scope/branch/concurrency gates.
4. Perform and record 28 distinct prompt adversarial review rounds.
5. Write and read back command, authority evidence, and audit evidence in AI-CONTEXT/main.
6. Close out TASKS / LEDGER / CASES / FAILURES records (this record and associated records).

ARTIFACTS:
- EVIDENCE/20261008-NEXY-SPEC-AUTHORITY-RESOLUTION-004.md
- COMMANDS/20261008-NEXY-CODEX-NEXT-EXECUTION-COMMAND-004.md
- EVIDENCE/20261008-NEXY-CODEX-NEXT-COMMAND-AUDIT-004.md
- TASKS/20261008-NEXY-CODEX-NEXT-COMMAND-004.md
- LEDGER/20261008-NEXY-CODEX-NEXT-COMMAND-004.md

TESTS:
- Uploaded DOCX SHA-256 compared with required hash: MATCH.
- GitHub read-back of three first artifacts: PASS.
- Product runtime/test execution in this audit task: NOT_RUN.
- Command executed by Codex: NOT_YET_OBSERVED.

DECISIONS:
- Do not mass-promote four spec-blocked rows; compare per row using verified extracts and current code.
- Treat source-search lack of production TSA caller as a hypothesis to falsify; never inject arbitrary time.
- Do not weaken sandbox isolation merely to pass experimental tests.
- DOC-E signoffs must be real, not inferred from passing local tests.

RISKS / UNRESOLVED:
- Codex may not have original DOCX bytes; verified locator extraction is in AI-CONTEXT, but each other requirement may need further direct extraction.
- Actual TSA integration and runtime source of authority must be proved.
- Browser failures and bwrap test failures are previous-run observations; re-run at current HEAD before remediation.
- Current CI failure cause remains unknown.
- Final release evidence, rollback verification and human signoffs remain unverified.

ROLLBACK:
- AI-CONTEXT changes can be reverted by new forward commits after exact-head check; do not reset, force-push, create or delete branches.

NEXT_ACTIONS:
- Codex re-queries NEXY.ai HEAD and reads the command plus authority record.
- Codex reclassifies affected rows only from current evidence, traces TSA, tests/repairs confirmed defects, audits remaining rows, writes and reads back outcomes.

DEPENDENCIES:
- Authorized live product branch, current source, actual runner for executable proof, external TSA authority for production flows, DOC-E signoffs for release.

TIMESTAMP_SOURCE: date from conversation: 2026-10-08, Asia/Bangkok; no claim of wall-clock execution timestamp.
HASH: DOCX_SHA256_MATCH; task-record SHA256 not computed.
TRACE_ID: NEXY-20261008-CODEX-COMMAND-004
