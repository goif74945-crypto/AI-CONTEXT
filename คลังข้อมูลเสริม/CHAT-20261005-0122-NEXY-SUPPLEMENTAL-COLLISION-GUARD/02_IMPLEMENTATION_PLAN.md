# Supplemental Collision Guard — Executed Implementation Plan

> Execution mode: native implementation in the current session with logical role separation and TDD. This plan records the decisions and evidence path used; it does not claim physical sub-agent isolation.

**Goal:** deliver a deterministic, offline-capable supplemental-project collision preflight tool and persist it only inside the authorized AI-CONTEXT work directory.

**Architecture:** one standard-library Python module owns discovery, bounded fingerprints, scoring, classification, rendering, and CLI policy behavior. One unittest module exercises behavior and adversarial boundaries. Documentation/schema/manifest make the work resumable and auditable.

**Tech stack:** Python 3 standard library, `unittest`, JSON/Markdown artifacts, GitHub Git-data/contents APIs for persistence.

**Spec:** `01_PROJECT_SPEC.md`

## Global constraints

- Do not mutate any repository whose name contains `NEXY.AI`.
- Do not mutate existing sibling supplemental projects.
- No third-party runtime dependencies.
- No network calls in the reference engine.
- No destructive Git operations.
- Do not represent AI-proposed concepts as canonical NEXY requirements.
- PASS requires executed evidence matching the claim class.

## Task 1 — Fingerprint/discovery core

Files:
- `src/collision_guard.py`
- `tests/test_collision_guard.py`

Executed TDD cycle:
1. Define noise normalization behavior.
2. Verify RED before module implementation.
3. Implement normalized terms and immediate-project discovery.
4. Verify nested files contribute to a project but nested directories do not become separate projects.
5. Add generated-output isolation and relative-path fingerprint tests.
6. Repair until focused and full suite pass.

## Task 2 — Explainable overlap classifier

Interfaces:
- `Candidate`
- `ProjectRecord`
- `score_candidate()`
- `classify_score()`
- `analyze_candidate()`

Executed TDD cycle:
1. Near-duplicate fixture expected `HIGH_OVERLAP`.
2. Orthogonal fixture expected `DISTINCT`.
3. Exact duplicate fixture expected `LIKELY_DUPLICATE`.
4. Reversed record input expected identical ranked output.
5. First threshold design over-classified the near-duplicate fixture; raise duplicate threshold rather than weakening the test intent.

## Task 3 — CLI and automation gate

Interfaces:
- `scan`
- `check`
- `--fail-at`

Executed TDD cycle:
1. High-overlap fixture must return policy exit `2` at `HIGH_OVERLAP` threshold.
2. Distinct fixture must return `0` at the same threshold.
3. Invalid non-discriminating candidate must return argparse-style `2` without traceback.
4. Implement minimal CLI behavior, then rerun full suite.

## Task 4 — Security and containment hardening

Threat model:
- a project contains a symlinked file pointing outside its directory;
- an immediate project entry is itself a symlink to an outside directory;
- candidate contains no meaningful terms and would otherwise bypass overlap checking.

Executed TDD cycle:
1. Write symlink-file escape test and observe external terms are read.
2. Add file-symlink exclusion and verify green.
3. Write symlink-project escape test and observe outside project is scanned.
4. Add project-symlink exclusion and verify green.
5. Add blank/generic-only candidate tests and fail closed.

## Task 5 — Artifact contract and evidence records

Files:
- `README.md`
- `00_SESSION_MEMORY.md`
- `01_PROJECT_SPEC.md`
- `02_IMPLEMENTATION_PLAN.md`
- `03_AI_PROPOSED_FUTURES.md`
- `04_REQUIREMENT_EVIDENCE_LEDGER.md`
- `05_VALIDATION_REPORT.md`
- `schema/collision-report.schema.json`
- `PROJECT-MANIFEST.json`

Checks:
- no unfinished placeholder markers in shipped artifacts;
- JSON parses;
- SHA-256 manifest covers immutable payload;
- source/test syntax compiles;
- full tests pass after documentation creation.

## Task 6 — Safe persistence and read-back

Target:
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-SUPPLEMENTAL-COLLISION-GUARD/`

Procedure:
1. Re-fetch current main HEAD and verify target path does not already exist with unrelated content.
2. Persist the initial verified project using non-force Git writes.
3. Re-fetch committed files.
4. Compare remote immutable payload against `PROJECT-MANIFEST.json` hashes.
5. Update dynamic session/validation records with persistence evidence if needed.
6. Re-fetch final records and final HEAD.
7. Do not claim COMPLETE unless the read-back/evidence gates pass.
