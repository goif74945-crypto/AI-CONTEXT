MESSAGE_ID: M-SOL-T044-DESIGN-PREFLIGHT
THREAD_ID: TH-T-04452B01-PREFLIGHT
FROM_CHAT: C-SOL-20261005-1709-B35E
TO_CHAT: FUTURE_OWNER_T-04452B01
TASK_ID: T-04452B01
TYPE: HANDOFF
PRIORITY: P0
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SUBJECT: G22 reason-code alignment preflight and minimal dependency option

FACT:
- Exact G22 static taxonomy already exists as exported STATIC_CODES in packages/phase-f/game/ncf-governance.ts.
- packages/phase-f/universe/capability-declaration.ts already imports canonical NCF types from ../game/ncf-governance.js.
- ncf-governance.ts imports core canonical-order and Node crypto; no direct import from packages/phase-f/universe was found in the inspected source/search path.
- Therefore reuse of STATIC_CODES from Universe has an existing dependency-direction precedent and no direct cycle is currently evidenced.
- Current capability-node.ts uses a separate incompatible taxonomy and returns de-duplicated encounter order rather than explicit lexicographic order.

SAFE DESIGN BOUNDARY:
Prefer the smallest change that guarantees canonical identity and sorting. Do not create a new shared reason-code module unless required, because that expands the mutation surface beyond the task's current two-file hotspot. Do not numerically remap legacy meanings when G22 semantics differ.

UNKNOWN:
G21 mandates syscall-scope and forbidden-collision checks but G22 gives no dedicated reason-code names for those exact conditions. Existing ncf-governance maps missing dependency/active forbidden collision to R008_SCHEMA_NONCANONICAL, but that is verified source precedent rather than explicit primary-spec mapping. Freeze those ambiguous mapping decisions unless authoritative interpretation is established.

REVIEW_REF: NEXY-BUILD-CONTROL/REVIEW/T-04452B01--C-SOL-20261005-1709-B35E.md
STATUS: READY_FOR_FUTURE_OWNER
