# NEXY.AI — Requirements Context

## Requirement authority

This document consolidates requirements stated in the source project document. It does not turn design aspirations into verified implementation facts.

- Source document SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- DOC-B is current system law; DOC-C is the current vNEXT build specification; DOC-D is current product design only where DOC-C supports it.
- The Final Architecture is conceptual; DOC-E is deployment/runtime evidence only.

## Product identity requirements

1. NEXY is a Core AI Control Hub, not merely a showcase website.
2. The product is deterministic/architect-first/verify-only by design.
3. NEXY is explicitly not AGI.
4. The human/user retains authority; User Law is a top-level user-defined constraint.
5. Hidden core logic must remain behind the user-facing surface; the user primarily receives controlled outputs.
6. The system must prefer freezing/silence over guessing or silently forcing an unsafe/incorrect result.
7. The release boundary is one legal verified output or freeze; it is not a promise that every request yields a result.

## Input and intent

1. Normalize and structure input before reasoning.
2. Resolve intent and constraints explicitly.
3. Detect ambiguity and missing information.
4. Do not guess material missing facts.
5. Uncertainty must be represented and propagated through the pipeline.

## Law / policy

1. User Law must be enforceable by downstream components.
2. Safety, logical, resource and temporal rules must be representable.
3. Policy conflicts are blocking conditions.
4. A rule that requires stopping must be able to stop downstream execution.
5. Policy changes require controlled evolution rather than silent drift.

## Reasoning

1. L1o is the Sovereign / Deterministic Logic Core.
2. L1o reasoning must be bounded by explicit domain/state/time constraints.
3. L1o truth tiers are T0 Unknown, T1 Heuristic, T2 Empirical, T3 Formally Verified and T4 Immutable Law.
4. Numeric CTS thresholds are not canonical in this context because the source contains an unresolved threshold conflict.
5. The system should collapse or reject inconsistent candidate paths.
6. The system should support state-transition reasoning.
7. The system must not rely on perfect knowledge or infinite reasoning.
8. Ambiguity should lead to a wait-for-clarity/blocking state rather than a guessed interpretation.

## Multi-AI / Swarm

1. Support multiple AI/model slots.
2. Support manual, semi-automatic and automatic routing modes as the design evolves.
3. Support parallel debate/work.
4. Support bounded adversarial review.
5. Support cross-verification.
6. Support proof-weighted consensus.
7. Support final adjudication by a judge layer.
8. External AI output is untrusted until filtered/verified.
9. Model hot-swapping should not alter the user's conceptual interface.
10. Model degradation should be detectable and may reduce the model's role or trigger a freeze.

## Output

1. One task should have a controlled final output rather than uncontrolled competing outputs.
2. Only verified output should pass the final release boundary.
3. Experimental outputs should require explicit verification and, where appropriate, user approval before durable Vault commitment.
4. The system should clearly distinguish conversational sandbox behavior from actual execution.

## Freeze / failure requirements

Freeze/block on conditions including unresolved ambiguity, insufficient evidence, AI/agent disagreement when no deterministic resolution exists, policy conflict, unsafe risk level, integrity/security violation, failed verification, state corruption or invalid replay, and inability to maintain required deterministic behavior.

Freeze is preferred to silent patching, silent fallback or forced execution.

## Memory / Vault requirements

1. Project truth must be stored in a persistent Vault.
2. Vault organization is file-based, project-based and timeline-based.
3. Task/session scoped memory must be distinguishable from persistent project truth.
4. Durable memory must be explicit, scoped and provenance-aware.
5. Experimental memory must not silently become immutable truth.
6. Memory conflicts require explicit resolution.
7. Support controlled pin/unpin and deletion/restore/permanent erase concepts.

## API requirements

1. Frontend → API Gateway → Core Logic → External APIs.
2. Frontend must not know provider secrets or direct secret-bearing API configuration.
3. API keys must be server-side and injected at runtime.
4. No hardcoded API keys.
5. Gateway must support rate limiting, authentication and logging.
6. Boundary/schema validation is required at interfaces.
7. External AI/provider output must be treated as untrusted input to the core.

## Auth requirements

The early V0 source direction of roughly 10–15 minutes is historical. Current DOC-C canonical defaults are:

1. Email + one-time alphanumeric code.
2. Code length: `10` characters.
3. Single-use.
4. TTL: `5 minutes` / `300000 ms`.
5. Store a hash rather than the plaintext code.
6. Maximum verification attempts: `5`.
7. Resend cooldown: `60 seconds`.
8. Lock window: `15 minutes`.
9. Session TTL: `6 hours` / `21600000 ms`.
10. Maximum concurrent sessions: `5` per user.
11. The source explicitly says this V0 is not MFA and not a complete zero-trust authentication system.

## UI / UX requirements

1. Minimal and premium.
2. Information-dense but not confusing.
3. Chat-centric control-room experience.
4. Adaptive theme and multilingual direction.
5. Fast load and low-RAM safe behavior.
6. RUN, FREEZE, LOCK, EXPORT and KILL are source command concepts; they must not be presented as current API routes without exact implementation evidence.
7. Support text/code/files/links/images/video/3D/media concepts as the product expands.
8. Separate user-facing views from deep control panels.
9. UI labels must not redefine core authority.
10. User language should be natural and non-therapist.
11. Complexity should be hidden unless the user needs advanced control.

## Security requirements

1. Zero-trust input model.
2. Prompt-injection defenses.
3. Access control and authorization boundaries.
4. Tenant/session isolation where multi-user scope exists.
5. Server-side secret management.
6. Secret scanning.
7. Sandboxed execution where execution is permitted.
8. RCE blocking.
9. Immutable audit trail for critical actions.
10. Rate limits and abuse controls.
11. Anomaly detection and freeze/containment behavior.
12. Encryption/key-management controls as applicable.
13. No hidden privilege escalation.

## Backend / persistence requirements

The general source direction favors serverless and database-agnostic architecture. The current DOC-C reference target is Next.js + TypeScript, Route Handlers or Node API, Zod, PostgreSQL, Prisma, BullMQ + Redis, blob/object storage, structured JSON logs with trace IDs, and Vitest/Playwright/Prisma integration tests. These are build targets, not implementation proof.

1. Temporary session store.
2. Persistent Vault store.
3. Policy separation.
4. Immutable audit log.
5. Critical writes should be idempotent.
6. Recovery should be explicit and state-safe.

## Determinism requirements

The broader design constraints require avoiding implicit sources of nondeterminism in critical paths, including uncontrolled randomness, time-dependent decisions, environment-dependent behavior, shared mutable state, unspecified async ordering and hidden fallback behavior. Any production claim of determinism requires reproducible evidence.

## Lo2 learning / evolution requirements

1. Extract reusable verified logic/quanta.
2. Synthesize candidate laws.
3. Evolve laws through test/compare/verification.
4. Prevent poisoned inputs from becoming law.
5. Maintain explicit old/new law state and rollback/rejection conditions.
6. Do not silently drift core rules or self-patch the current runtime.

## Monitoring / operations requirements

1. Monitor errors, resources, performance, security and AI decisions.
2. Preserve traceability for critical operations.
3. Support rollback/recovery concepts.
4. Handle partial network failure, overload, race/duplicate execution and corruption scenarios.
5. Maintain a safe failure mode when normal execution is unavailable.

## Robotics requirements

1. Separate fast reflex control from AI reasoning.
2. Keep a dedicated Safety Kernel outside normal AI control.
3. Support sensor fusion.
4. Use a main compute layer for L1o/Lo3.
5. Use MCU control for real-time fast paths.
6. Support watchdog and emergency stop controls.
7. Safety must continue to function if AI fails.
8. Example stack: Jetson Orin-class main compute, STM32/Pico fast MCU, independent safety MCU, ROS2, FreeRTOS, ONNX/TensorRT, Gazebo/RViz.
9. Main and MCU communications may use ROS2 DDS plus UART/CAN.
10. Source examples include a fast path around 10 ms and a slower AI loop around 100 ms. Safe Path sections conflict between roughly 50–200 ms and 50–500 ms, so no single physical latency budget is canonical yet.
11. Robotics rollout is staged: simple prototype → added L1o/simple Lo3 → full dual-MCU safety/swarm design.

## Nonfunctional design goals

- controllability;
- explicit state;
- evidence-based output;
- reproducibility;
- low-resource operation;
- modularity;
- model/provider independence;
- strong separation of authority from execution;
- auditable evolution;
- failure containment.

## Acceptance note

These are requirements/design directions. They are not acceptance-test results. No item should be marked implemented/verified without corresponding repository artifacts, tests, logs or reproducible evidence.
