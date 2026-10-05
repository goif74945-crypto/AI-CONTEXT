TASK_ID: TASK-DOC-C4-RUN-OPTIONAL-NULL-001
REQ_ID: REQ-DOC-C-4-2-RUN-DETAIL
REVIEWER_CHAT: C-SOL-20261005-1743-CLOSURE
ROLE: SHADOW_REVIEWER / CONTRACT_CLOSURE_RECONCILER
STATUS: CHANGES_REQUIRED_BEFORE_TASK_CLOSE
PRIORITY: P1
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_MUTATION_BY_REVIEWER: NONE

## FACT

Final DOC-C GET /api/runs/:id declares five result members as optional non-null scalar types when present:
- accepted?: boolean
- releaseable?: boolean
- confidence?: number
- deterministic_match_score?: number
- primary_incident_id?: string

At the pinned integration SHA, handleGetRun always serializes all five members.
PipelineRun persistence can hold null for each of these members before the corresponding run result is available.
q64ToNumber(null) returns null.

Therefore the same optional-versus-nullable defect is not limited to primary_incident_id.

The supporting record FINDING-DOC-C4-RUN-READ-OPTIONAL-WIRE-001 already captures this broader evidence, but the canonical active task currently narrows SEMANTIC_SCOPE and acceptance to primary_incident_id only.

## CLOSURE RISK

Closing TASK-DOC-C4-RUN-OPTIONAL-NULL-001 after repairing only primary_incident_id can leave:
- accepted: null
- releaseable: null
- confidence: null
- deterministic_match_score: null

in successful canonical responses, while the active requirement still declares those fields optional boolean/number values.

That would be a false task close and would leave an ACTIONABLE_CODE_GAP.

## REQUIRED RECONCILIATION

Keep one writer and one canonical task. Do not create another semantic repair task.

Before TASK-DOC-C4-RUN-OPTIONAL-NULL-001 can close, its effective acceptance must cover all five optional fields:
1. omit accepted when persistence value is null; when present it is boolean
2. omit releaseable when persistence value is null; when present it is boolean
3. omit confidence when persistence value is null; when present it is number
4. omit deterministic_match_score when persistence value is null; when present it is number
5. omit primary_incident_id when persistence value is null; when present it is string

Tests must cover at least:
- an incomplete/READY run where unavailable optional fields are omitted
- a completed run where available optional values are present with exact declared scalar types
- preservation of run_id, state, tenant isolation, OWNER/OPERATOR/AUDITOR authorization, and PIPELINE_RUN_VIEWED evidence

INC-BRANCH-NAMESPACE-001 still blocks source mutation. This review changes no source and allocates no second writer.
