TASK_ID: T-EMPTY-4C91E7B2
CREATOR_CHAT: C-SOL-20261006-EMPTY-4C91E7B2
OWNER_CHAT: C-SOL-20261006-EMPTY-4C91E7B2
STATUS: IMPLEMENTING
PRIORITY: P2
RISK: LOW
BASE_SHA: 92aff2f532d30d81e74b8d2292a583edb77b5de8
SEMANTIC_SCOPE: DOC-D canonical empty-state copy and component binding for directive list and pipeline-run list only.
TARGET_PATHS:
- apps/web/app/directives/page.tsx
- apps/web/app/runs/page.tsx
- tests/contract/doc-d-empty-states.test.ts
PROTECTED_SCOPE:
- NEXY.ai
- API semantics
- auth
- state machine
- queue behavior
- Vault behavior
AUTHORITY:
- Authoritative DOCX DOC-D empty-state wording: "No directive yet" and "No active run"
- Existing canonical EmptyStateCard type contract
SUCCESS_INVARIANTS:
- /directives empty state renders EmptyStateCard with exactly "No directive yet"
- /runs empty state renders EmptyStateCard with exactly "No active run"
- No data-fetch, authorization, routing, or non-empty-list behavior changes
TEST_PLAN:
- Add focused static contract regression for canonical component/copy
- Inspect diff and exact worker SHA
- Use exact-head CI evidence if executable
FORBIDDEN:
- No NEXY.ai mutation
- No unrelated UI refactor
- No invented product copy
