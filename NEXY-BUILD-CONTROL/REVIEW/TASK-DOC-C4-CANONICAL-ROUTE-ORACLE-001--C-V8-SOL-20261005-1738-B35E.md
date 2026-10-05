TASK_ID: TASK-DOC-C4-CANONICAL-ROUTE-ORACLE-001
REVIEWER_CHAT: C-V8-SOL-20261005-1738-B35E
ROLE: INDEPENDENT_SPEC_ORACLE_REVIEWER
STATUS: REVIEW_CONFIRMS_ACTIONABLE_GAP
PRIORITY: P1
RISK: MEDIUM
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_AUTHORITY: final DOC-C §4.2 route matrix, primary DOCX paragraphs 10038-10352

FACT:
- Final DOC-C §4.2 declares exactly twelve canonical routes:
  1 POST /api/auth/request-otac
  2 POST /api/auth/verify-otac
  3 GET /api/session/me
  4 POST /api/auth/logout
  5 POST /api/directives
  6 GET /api/directives/:id
  7 GET /api/runs/:id
  8 POST /api/freeze/recover
  9 POST /api/vault/commit
  10 GET /api/artifacts/:id/revisions
  11 GET /api/incidents/:id
  12 GET /api/audit-logs
- scripts/check-doc-c.ts blob 5d60b3b8bcce8d11988fd971679eb9685177cc43 promotes fifteen routes as DOC-C routeFiles.
- The three extras are GET /api/directives, GET /api/runs, and GET /api/artifacts. They are implementation surfaces, but they are not in final DOC-C §4.2.
- The current route oracle primarily verifies adapter existence/exported HTTP method and a small set of source-string guards; this is insufficient to prove the complete §4.2 auth/RBAC/idempotency/retry/audit/error semantics.
- Keeping implementation-only collection endpoints is not itself a defect; misclassifying them as canonical DOC-C obligations is the oracle defect.

OBSERVED:
Canonical denominator = 15 implementation routes.

EXPECTED:
Canonical final-DOC-C denominator = exactly 12 routes, with semantic checks derived from §4.2 rather than adapter existence alone.

CLASSIFICATION:
TEST_ORACLE_DEFECT + AUTHORITY_DRIFT + MISSING_REQUIRED_TEST.

ASSUMPTION:
None required.

UNKNOWN:
No exact-candidate execution is available yet because source mutation is blocked by INC-BRANCH-NAMESPACE-001 and hosted exact-head CI is zero-step EXECUTION_INFRA_FAILURE.

VERDICT:
ACTIONABLE VERIFICATION GAP CONFIRMED. Preserve non-canonical endpoints unless separately out of scope; repair only the DOC-C oracle/classification and missing semantic assertions.
