FAILURE_ID: F-7297BBB-CONTRACT-ORACLE
REPORTER_CHAT: C-6F42A9D1
TASK_ID: T-6F42B8E1
STATUS: DIAGNOSED
PRIORITY: P1
CATEGORY: CONTRACT_TEST_ORACLE_STALE
HEAD_SHA: 7297bbbff42ce8c5236c2fc551a4b29893be2a73
WORK_BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai

FACT:
- Exact-head Railway validation deployment 644b3185-5d1e-4ca2-9fe5-588d127940f6 passed DOC-E source identity binding and Rust core tests.
- npm run test:contract then failed exactly 1 of 651 tests.
- Failing test: tests/contract/release-attestation.test.ts, canonical workflow targets NEXY.ai and keeps Phase-F advisory.
- Old assertion requires deploy.yml to contain "branches: [NEXY.ai]" and forbids "branches: [NEXY.ai,".
- T-8F3C2A91 explicitly requires static verification that push branch filter contains both NEXY.ai and NEXY.AI-Test-AI while preserving deploy authorization only for NEXY.ai.
- deploy.yml still restricts production deploy job to github.ref == refs/heads/NEXY.ai && push.

ASSUMPTION: none required for root-cause classification.

UNKNOWN:
- Coverage result at SHA 7297bbb because contract gate stops Docker build before coverage.

ROOT_CAUSE:
- Contract oracle encodes the superseded assumption that the canonical workflow must never trigger on a second push branch. The authorized work-branch validation trigger changed that assumption without changing protected deploy authorization.

TEST_ORACLE_CORRECTION:
OLD: expect source to contain only branches: [NEXY.ai] and reject branches: [NEXY.ai, ...].
NEW: require push branches [NEXY.ai, NEXY.AI-Test-AI], retain pull_request target NEXY.ai, and retain production deploy if-condition locked to refs/heads/NEXY.ai.
WHY: validation execution on the authorized work branch is required; deployment authorization must remain protected.
SOURCE:
- NEXY V4 constitution work branch NEXY.AI-Test-AI / protected upstream NEXY.ai
- Task T-8F3C2A91 semantic scope and test plan
- .github/workflows/deploy.yml
EVIDENCE:
- Railway exact-head deployment 644b3185-5d1e-4ca2-9fe5-588d127940f6
- tests/contract/release-attestation.test.ts:245-246
- NEXY-BUILD-CONTROL/TASKS/T-8F3C2A91.md

NEXT_ACTION:
- Correct only the stale contract oracle, rerun exact-head validation, and do not relax deploy-job branch protection.
