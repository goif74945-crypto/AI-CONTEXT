TASK_ID: T-INCIDENT-TRUTH-7B3E91C4
CREATOR_CHAT: C-SOL-20261006-INCIDENT-TRUTH-7B3E91C4
OWNER_CHAT: C-SOL-20261006-INCIDENT-TRUTH-7B3E91C4
STATUS: INTEGRATED_STATIC_VERIFIED
PRIORITY: P1
RISK: LOW
BASE_SHA: aec9afaa77213c37b223b7594b92eb81c7862f9a
SEMANTIC_SCOPE: DOC-D S7 Freeze Incident truth mapping only. Stop labeling request_id as trigger when canonical incident truth does not expose a trigger field.
TARGET_PATHS:
- apps/web/components/IncidentCard.tsx
- apps/web/app/incidents/[id]/page.tsx
- tests/contract/incident-card-truth.test.ts
AUTHORITY:
- DOC-D S7 requires display of primary incident code, trigger, blocking layer, recoverable.
- DOC-C FreezeIncident schema exposes primary_error_code, blocking_layer, request_id, trace_id, recoverable; no trigger field.
- UI truth law forbids inventing state/data.
REQUIRED_BEHAVIOR:
- Never map request_id into the trigger slot.
- Render trigger as explicit UNKNOWN when backend trigger truth is absent.
- Render request_id separately under its correct label.
- Preserve primary error, blocking layer, recoverable, trace, permissions and recovery behavior.
FORBIDDEN:
- No API/schema/persistence mutation.
- No inference of trigger from request_id, error code, trace, or UI context.
- No NEXY.ai mutation.
TEST_PLAN:
- Focused static truth-mapping assertions.
- Exact diff/overlap review before non-force integration.

WORKER_BRANCH: NEXY.AI-Test-AI-work-incident-truth-7b3e91c4
WORKER_HEAD_SHA: fea6cfdaf452cfeac2d4fc2b66b0a3528caacf6c
INTEGRATION_COMMIT_SHA: cf6d5cc7792cbed7e06018364e33be658f24010a
VERIFICATION:
- Focused source-contract assertions PASS 9/9 on exact worker SHA.
- Worker diff exactly 3 files.
- Integration drift 3 commits; target overlap 0; non-force fast-forward.
- Post-integration exact blobs: IncidentCard=26bf01d5080066606ff1b4b80c61b3e8b30826bd; incident page=44b7b60cac52fef83bf46c091431084ed2bd08ab; test=1336f38d66dfefad36b629bf05ed24832f494562.
- Protected NEXY.ai unchanged at 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
RUNTIME:
- Exact-head workflows were queued at last observation; no full-suite PASS claimed.
MUTATION_OWNER_ACTIVE: FALSE
CONTINUATION_REQUIRED: Independent runtime validation after shared execution-layer evidence is available.
