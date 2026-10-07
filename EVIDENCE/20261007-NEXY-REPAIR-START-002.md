# Evidence — NEXY Repair Start Blocked

EVIDENCE_ID: EVIDENCE-20261007-NEXY-REPAIR-START-002
TASK_ID: 20261007-NEXY-REPAIR-START-002
MODE: CROSS / EXECUTE_NOW / EVIDENCE_DRIVEN / FAIL_CLOSED
STATUS: BLOCKED_WITH_RESUME
OBSERVED_UTC: 2026-10-07T14:10:59Z

## Exact authority and heads

- DOCX: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- DOCX SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7` (fresh local hash match)
- Product repository: `goif74945-crypto/NEXY.AI-`
- Product branch: `NEXY.ai`
- Product HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- AI-CONTEXT repository: `goif74945-crypto/AI-CONTEXT`
- AI-CONTEXT branch: `main`
- AI-CONTEXT parent HEAD: `a28a94c72ea40fe9083d6ca536c668649fec5926`

## Capability observation

The live authorized gateway reports:

- product `read_only=true`
- product `gateway_write_policy=DENY`
- GitHub permission fields pull/push/admin=true
- AI-CONTEXT `read_only=false`
- AI-CONTEXT `gateway_write_policy=ALLOW`

The configured gateway policy is the controlling boundary. No product write or CI dispatch was attempted.

## Baseline

The existing controlled matrix remains 98 unique rows: VERIFIED=71, PARTIAL=15, MISMATCH=5, NOT_VERIFIED=7. The previous exact-head failures and stale attestation remain non-passing evidence. This checkpoint does not promote any row.

## Stop and resume

The locked command requires stopping when product write or CI dispatch is DENY/read-only. Resume only after both capabilities are explicitly ALLOW, then use a newly frozen product HEAD and the required RED → minimal fix → GREEN → full verification loop.

## Integrity

- Product files changed in this attempt: NO
- Product branch changed: NO
- CI dispatch: NOT ATTEMPTED
- Alternate backend bypass: NO
- PASS_100: NO
