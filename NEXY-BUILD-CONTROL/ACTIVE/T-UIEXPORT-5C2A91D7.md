TASK_ID: T-UIEXPORT-5C2A91D7
OWNER_CHAT: C-SOL-20261006-UIEXPORT
STATUS: IMPLEMENTING
PRIORITY: P1
BASE_SHA: 822f54ab052f206ecfd43f9bf7a08c6a0e0b778d
SEMANTIC_SCOPE: DOC-B §16.4 / DOC-D S5 directive-detail export must remain disabled while backend release is blocked.
TARGET_PATHS:
- apps/web/app/directives/[id]/page.tsx
- tests/contract/directive-export-truth-gate.test.ts
MUTATION_BOUNDARY: Gate only the Directive Detail EXPORT UI action on canonical backend release truth. No API, LAW, auth, state-machine, Vault, or NEXY.ai mutation.
REQUIRED_EVIDENCE: focused test + type/static validation if executable; final diff inspection; exact worker/base SHA.
