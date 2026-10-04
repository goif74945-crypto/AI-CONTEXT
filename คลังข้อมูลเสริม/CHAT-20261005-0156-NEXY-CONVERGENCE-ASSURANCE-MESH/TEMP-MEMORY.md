# Temporary / Resumable Mission Memory

- WORK_CHAT_ID: `CHAT-20261005-0156-NEXY-CONVERGENCE-ASSURANCE-MESH`
- PLATFORM_INTERNAL_CHAT_ID: `UNKNOWN` — not exposed by available tools.
- TARGET_REPO: `goif74945-crypto/AI-CONTEXT`
- TARGET_BRANCH: `main`
- AUTHORIZED_WRITE_ROOT: `คลังข้อมูลเสริม/CHAT-20261005-0156-NEXY-CONVERGENCE-ASSURANCE-MESH/`
- PROTECTED: any repository name containing `NEXY.AI`; all pre-existing paths outside mission root.
- CURRENT_PHASE: LOCAL_IMPLEMENTATION_VERIFIED / GITHUB_PERSISTENCE_PENDING
- LOCAL_STATIC: PASS (`python3 -m compileall -q .`)
- LOCAL_TESTS: PASS (34/34, repeated under PYTHONHASHSEED=1 and 777)
- PROPERTY_TESTS: PASS
- SECRET_PATTERN_SCAN: PASS / 0 findings
- CONCEPTS: ICG, CNS, EAP, REC, IEQE
- INTEGRATION_CLASSIFICATION: advisory preflight only; never substitutes for NEXY::JUDGE.
- NEXT_ACTION: persist exact verified tree atomically to AI-CONTEXT, read back, hash-compare, record commit and final audit.
- RESUME_RULE: refresh current `main` before any ref mutation; use fast-forward only; on concurrent HEAD advance rebuild commit on latest base rather than force.
