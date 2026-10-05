TASK_ID: T-OWNER-DRAWER-4E8C2A71
CREATOR_CHAT: C-SOL-20261006-OWNER-DRAWER-4E8C2A71
OWNER_CHAT: C-SOL-20261006-OWNER-DRAWER-4E8C2A71
STATUS: INTEGRATED_STATIC_VERIFIED
PRIORITY: P1
RISK: LOW
BASE_SHA: 65e0a1d06955f253109312594404c7be811a36a2
SEMANTIC_SCOPE: DOC-D 6.8 responsive OWNER danger-control accessibility only.
TARGET_PATHS:
- apps/web/app/globals.css
- tests/contract/doc-d-owner-drawer-responsive.test.ts
AUTHORITY:
- DOC-D mobile law: danger controls hidden behind owner drawer.
- DOC-D S11: OWNER control actions must be usable.
OBSERVED_GAP:
- owner <details> is closed by default.
- desktop CSS hides the summary but does not override closed-details content hiding, making OWNER controls unreachable on desktop.
REQUIRED_BEHAVIOR:
- Mobile <=700px keeps summary visible and content hidden until details is open.
- Desktop >=701px renders owner drawer content even when details lacks open attribute; summary remains hidden.
FORBIDDEN:
- No owner action/API/RBAC mutation.
- No mobile auto-open.
- No NEXY.ai mutation.

WORKER_BRANCH: NEXY.AI-Test-AI-work-owner-drawer-4e8c2a71
WORKER_HEAD_SHA: dbb51dae6c7197a69ed6e7b9d0072f2c62b6b70d
INTEGRATION_COMMIT_SHA: 07dd617109fd4730582f3615cdaf2bbbe277b585
VERIFICATION:
- Focused responsive source-contract assertions PASS 5/5.
- Diff exactly globals.css + one contract test.
- Integration drift 0; target overlap 0; force=false.
- Post-integration blobs: globals.css=6467bc9a59373da085f258e0ab4592e316608fe2; test=606c3842747312307c116224378605f31eee4489.
- Protected NEXY.ai unchanged at 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
MUTATION_OWNER_ACTIVE: FALSE
CONTINUATION_REQUIRED: Browser/runtime validation when shared execution layer emits usable steps.
