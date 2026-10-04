# Scope Audit — Pre-Persistence

- Authorized durable target: `goif74945-crypto/AI-CONTEXT` only.
- Authorized write prefix: `คลังข้อมูลเสริม/CHAT-20261005-0156-NEXY-EXECUTION-INTELLIGENCE-FABRIC/` only.
- Repositories whose names contain `NEXY.AI`: read-only by contract; no mutation action invoked.
- Existing AI-CONTEXT files outside the work prefix: read-only; no mutation action invoked.
- Local runtime work occurred only in an ephemeral `/mnt/data/nexy_eif/...` workspace.
- Final post-persistence scope status must be established from GitHub commit/read-back evidence.
