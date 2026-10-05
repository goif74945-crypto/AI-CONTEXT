TASK_ID: T-OWNER-DRAWER-4E8C2A71
CREATOR_CHAT: C-SOL-20261006-OWNER-DRAWER-4E8C2A71
OWNER_CHAT: C-SOL-20261006-OWNER-DRAWER-4E8C2A71
STATUS: IMPLEMENTING
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
