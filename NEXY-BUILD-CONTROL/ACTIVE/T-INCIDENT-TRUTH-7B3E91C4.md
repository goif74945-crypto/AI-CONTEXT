TASK_ID: T-INCIDENT-TRUTH-7B3E91C4
CREATOR_CHAT: C-SOL-20261006-INCIDENT-TRUTH-7B3E91C4
OWNER_CHAT: C-SOL-20261006-INCIDENT-TRUTH-7B3E91C4
STATUS: IMPLEMENTING
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
