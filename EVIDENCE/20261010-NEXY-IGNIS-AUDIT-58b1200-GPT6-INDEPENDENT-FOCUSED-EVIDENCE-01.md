# NEXY-IGNIS independent exact-head focused audit — 2026-10-10
STATUS: PARTIAL / NOT_VERIFIED / NOT A 100% PRODUCT CERTIFICATION
SOURCE_PRODUCT_REPO: goif74945-crypto/NEXY.AI-
PRODUCT_BRANCH: NEXY.ai
PRODUCT_HEAD_OBSERVED_AND_RECHECKED: 58b1200bd61b867e917057d0019eea78ea9f6b2a
CONTROL_REPO: goif74945-crypto/AI-CONTEXT
CONTROL_HEAD_INITIAL_OBSERVATION: 1e40252b5cdd199593ca30ce589e8d920786dc1d
CONTROL_HEAD_RECHECK_BEFORE_APPEND: 280a238d6645b6c036e85e27f076212841e6e32b
ORIGINAL_DOCX_SHA256_CALCULATED: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
DOCX_PARAGRAPH_SLOTS: 12537
DOCX_NONEMPTY_PARAGRAPHS: 10979
AUTHORITY_ANCHORS: P09837-P09845 DOC-C-only build obligation; DOC-E-only deploy approval
FINAL_DOC_C_WINDOW: P09886-P10499; DOC-D starts P10500, DOC-E starts P10917
SOURCE_TREE: git/trees/6fd81ae8150aecc341f8a49f65e3c050f559c51f?recursive=1
TREE_API_COMPLETE: true (truncated=false)
TRACKED_BLOBS_INVENTORIED: 889
TREE_DIRECTORIES: 203
TREE_ENTRIES: 1092
TRACKED_FILES_SEMANTICALLY_REVIEWED_ALL: NO

## Live CI evidence
All four exact-HEAD GitHub Actions workflows reported conclusion=failure:
- 37899764374 NEXY CI / Deploy Gate: 9 jobs failure, 3 jobs skipped.
- 37899764452 Layer8 Cargo lock evidence: failure.
- 37899764383 Exact HEAD test evidence: failure.
- 37899764371 Six-system exact HEAD evidence: failure.
GitHub job logs fetched for jobs 113719322485, 113719323063, 113719321967 all returned BlobNotFound 404. Runner-versus-source root cause remains UNKNOWN. Do not label test assertions failed without actual step log.

## Local source tests, independently executed at exact Git blobs
- packages/core/canonical-json.ts — Git blob SHA c0c14ca5a6fa16e2ebc9da191774d3306fc6c1ee, independently hash-matched, compiled with TypeScript 5.8.3 and executed with Node.js 22.16.0: 24 PASS / 0 FAIL. Tests included deterministic nested sorting; primitive domain; array order; sparse arrays; NaN; bigint; undefined; Date/Map/Set; symbols; non-enumerables; accessor nonexecution; cycles; repeated acyclic refs; null prototype; array prototype/properties. This does not validate every consumer.
- packages/api/vnext-config.ts — Git blob SHA a3141a649be7e40ec79f417f53bba9b73081232b, independently hash-matched, compiled with TypeScript 5.8.3 and executed with Node.js 22.16.0: 26 PASS / 0 FAIL, comparing 26 runtime constants to **source-original-DOCX-extracted** P09912-P09949 numeric defaults. This does not validate consumers or external runtime behavior.
TOTAL FOCUSED_CHECKS: 50/50 PASS. PRODUCT_ACCEPTANCE: NOT_VERIFIED.

A temporary clone of the exact HEAD was confirmed on a connected Windows device, but full npm/Cargo tests did not complete because remote process execution failed with Windows cwd/path issues and later timed out. Never claim these full gates were run/passed.

## Follow-up for Codex
Must independently hash-verify original spec; refresh HEAD; enumerate/review all tracked source; derive every atomic DOC-C requirement beyond the historical 143-point register; map every clause to implementation and positive, adversarial, integration and external DOC-E evidence; run full npm and Cargo suite on isolated exact-head checkout; diagnose CI execution provisioning versus actual failing tests; repair only proven defects; obey AGENTS.md NO BRANCH CREATION and only NEXY.ai; append unique evidence to AI-CONTEXT; never assert 100% until all denominators and gates proven. Use current-source files, not historical reports.
