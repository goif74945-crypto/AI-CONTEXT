TASK_ID: NEXY-WHOLE-PROJECT-AUDIT-E54ABD3-20261003
mode: AUDIT/CROSS
target_repo: goif74945-crypto/NEXY.AI-
target_branch: NEXY.ai
frozen_head: e54abd3122427dcfc27f81cc725ec0f43ff00837
frozen_tree: 0ad78e8f8fcdbbeb3141e483fa31e70172e2a08c
timestamp_source: 2026-10-03T00:03+07:00
canonical_design_sha256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
sanitization: no secrets, credentials, private keys, tokens, or sensitive PII stored

CASE_ID: CASE-NEXY-CURRENT-EVIDENCE-STALE-E54ABD3
severity: S4
cause:
- live exact-head Railway campaign executed at e54abd3122427dcfc27f81cc725ec0f43ff00837
- repository files named current still bind older revisions
proof:
- docs/evidence/current/README.md -> 0d0d82bdc7d04ef8248f310d106cf5e4c1dd7a3d
- docs/evidence/current/E11-release-signoff.md -> same old revision
- docs/evidence/current/E12-rollback-execution.md -> same old revision and stale BLOCKED state
- evidence/current-head-attestation.json -> 7eb83a88eee1eb9d6357577ad937a82248933091
- live DOC-E campaign at e54abd3122427dcfc27f81cc725ec0f43ff00837: E1-E10 PASS, E11 BLOCKED_EXTERNAL, E12 PASS
impact:
- repository current evidence is not current truth
- stale E12 contradicts current live exact-head E12 PASS
- release evidence cannot be audited from repository current namespace alone
fix:
- generate exact-head evidence artifacts from the current execution
- replace the current namespace only with revision-bound generated evidence
- preserve historical evidence separately
status: OPEN
