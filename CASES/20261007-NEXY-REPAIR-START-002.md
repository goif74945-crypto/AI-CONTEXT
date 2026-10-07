# Case — NEXY Repair Start Blocked by Product Gateway

CASE_ID: CASE-20261007-NEXY-REPAIR-START-002
TASK_ID: 20261007-NEXY-REPAIR-START-002
OPENED_UTC: 2026-10-07T14:10:59Z
STATUS: BLOCKED_WITH_RESUME

## Trigger

User requested: start fixing NEXY.ai to pass the locked specification.

## Reproduction

Query the authorized Repo Code Bridge for:

`goif74945-crypto/NEXY.AI-` on branch `NEXY.ai`.

## Expected

The product gateway must expose write capability and CI dispatch capability before any product edit, test commit, or exact-head validation can begin.

## Observed

- Product HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- `read_only=true`
- `gateway_write_policy=DENY`
- GitHub permission fields: pull/push/admin=true
- AI-CONTEXT `main`: write ALLOW at parent `a28a94c72ea40fe9083d6ca536c668649fec5926`
- Authoritative DOCX SHA: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

## Decision

Apply the locked command's mandatory stop condition. Product repair is paused. AI-CONTEXT checkpoint work is allowed; product mutation and CI dispatch are not.

## Expected impact

Until the gateway boundary changes, the product remains at the observed HEAD and the prior unresolved audit rows remain unresolved. No release or PASS_100 claim is valid.

## Resume

Re-query capability, freeze a new exact product HEAD only after write and CI are ALLOW, then begin Phase A with TDD for behavioral changes.
