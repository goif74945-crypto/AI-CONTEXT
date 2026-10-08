# NEXY Spec Authority Resolution — 2026-10-08

STATUS: VERIFIED_SOURCE
SOURCE_FILE: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SOURCE_PATH_IN_AUDIT_ENV: /mnt/data/แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
HASH_MATCH_REQUIRED_AUTHORITY: YES

## Authority hierarchy from the DOCX
- P9837–P9845: DOC-A = VISION CANON; DOC-B = SYSTEM LAW; DOC-C = BUILD SPEC; DOC-D = PRODUCT DESIGN PACK; DOC-E = DEPLOYMENT EVIDENCE PACK.
- P9843–P9845: the five documents are not equal build authority; build obligation comes from DOC-C only; deploy approval comes from DOC-E only.

## AUTH-03 resolution evidence
- Early prose (P1 and P2665) contains temporary-auth language with OTAC TTL 10–15 minutes and session TTL 1–6 hours.
- Final DOC-C canonical defaults (P9910–P9938) define otac_ttl_ms = 300000, otac_max_attempts = 5, otac_lock_window_ms = 900000, session_ttl_ms = 21600000, concurrent_sessions_per_user = 5.
- Because P9844 states build obligation comes from DOC-C only, the DOC-C values are the build authority. The earlier auth prose remains historical/conflicting prose and must not override DOC-C.

## Scope fence authority
- P9644–P9689 defines 17. SCOPE FENCE / NON-GOAL CONTRACT.
- vNEXT includes deterministic directive execution, multi-agent pipeline, consensus + release policy, vault revisioning, auth/session/OTAC, observability + incidents, RBAC + UI truth layer.
- Explicitly excluded: voice orchestration, blockchain integration, real-time 3D UI, public anonymous write access (NEVER), AR/VR/XR, IoT device control, quantum-safe cryptography layer for vNEXT, holographic UI.
- Deferred: advanced policy simulation dashboard, multi-tenant org hierarchy, fine-grained per-project config policy, provider marketplace layer.
- Outside-vNEXT features require explicit spec extension and dependency impact review.

## Time authority evidence from the broader DOCX
- P4001–P4011: Dual Source Time; TSA set size 3; valid signatures >= 2; degraded time max 24h; excessive TSA/chain delta => anomaly; normal rotation 180 days; emergency replacement via compromise flag + 3/5 quorum.
- P4510–P4511: 3 TSA set, 2-of-3 required, rotation window.
- IMPORTANT AUTHORITY NOTE: these time-authority sections are outside the final DOC-C build-spec section. They may constrain broader sovereign/experimental architecture, but they must not silently become a vNEXT build obligation unless an explicit DOC-B/DOC-C dependency establishes that bridge.

## Sandbox/isolation evidence
- P4137–P4149: isolation via container sandbox, namespace isolation, syscall filter, memory isolation, optional WASM mode.
- P4886–P4927: sandbox tiers must never climb back to kernel/anchor, capabilities may only shrink, sandbox app cannot spawn privileged containers or mount external FS; actions go through parent mediation.
- The source does not prescribe a specific host filesystem path set such as /usr-only or /opt-only. Any runtime-root fix must preserve isolation and prevent guest-controlled arbitrary host mounts.

## DOC-E release evidence
- P10917–P10948: DOC-E must contain proof artifacts, including contract test report, API schema snapshot, migration+rollback proof, state-machine tests, RBAC tests, auth-abuse report, queue-worker readiness, observability/alarm verification, incident drill, deploy runbook, release signoff, rollback playbook execution proof.
- P10949–P10960: evidence item format includes artifact name, commit hash, environment, date, operator, command/test ID, result, log link, screenshot/output excerpt, pass/fail.
- P10975–P10982: no deploy without engineering, security, migration signoff, rollback verification, monitoring verification.
- P10991–P10999: monitoring verification must prove alerts for auth abuse, freeze incident, worker down, queue backlog, DB failure, release-policy failure.

## Audit consequences
- AUTH-01 may be reclassified from SPEC_SOURCE_ACCESS_BLOCKED because the exact required SHA was verified.
- AUTH-02 may be reclassified after current implementation is compared to the documented authority split.
- AUTH-03 is not a product-code mismatch if current code matches DOC-C canonical defaults; preserve the historical prose conflict in notes.
- SCOPE-01 may be reclassified after current repository scope is compared to Section 17.
- Release/deploy signoff rows remain NOT_VERIFIED until real DOC-E artifacts/signoffs exist.