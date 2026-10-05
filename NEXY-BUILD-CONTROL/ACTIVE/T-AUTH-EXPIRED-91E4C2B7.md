TASK_ID: T-AUTH-EXPIRED-91E4C2B7
OWNER_CHAT: C-SOL-20261006-0132
STATUS: RELEASED_TO_RUNTIME_VALIDATION
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
SEMANTIC_SCOPE: Make POST /api/auth/verify-otac return canonical 401 AUTH_EXPIRED only for an exact same-device unconsumed expired OTAC match, preserving constant-width security behavior.
TARGET_PATHS:
- packages/api/auth.ts
- tests/coverage/auth-decision-paths.test.ts
- tests/integration/auth/verify-otac.spec.ts
RED_TEST_COMMIT: 8edcb3d27cedf0fcf3d7aa9217055cbcea7b0971
SOURCE_FIX_COMMIT: 999cf6b6a64e1cb36a295f80af5cbbc3a97d5742
INTEGRATION_ORACLE_COMMIT: 364a67f16a17c12533e9a578586a0def648cd912
STATIC_INVARIANTS:
- fixed for-loop remains i < SLOTS with no early return
- exactly one timingSafeEqual call in each scan iteration
- every real row uses its real salt/hash for classification; padding alone uses dummy material
- exact unconsumed same-device expired match sets expiredMatch but never matchedId
- exact consumed replay is recognized regardless of expiry and remains AUTH_INVALID plus suspicious-auth persistence
- existing DEVICE_MISMATCH branch precedes AUTH_EXPIRED
- wrong expired code falls through to AUTH_INVALID
- tests assert exact expired => AUTH_EXPIRED, wrong expired => AUTH_INVALID, consumed-after-expiry => AUTH_INVALID + security incident
GITHUB_ACTIONS_EVIDENCE:
- red test exact/six runs 37359413073 / 37359413210: failure before first step
- source fix exact/six runs 37359534703 / 37359534803: failure before first step
- integration oracle exact/six runs 37359613502 / 37359613591: failure before first step
- all observed jobs stepCount=0, classify EXECUTION_INFRA_FAILURE
ALTERNATE_EXECUTION:
- existing Railway branch validator is protected by another active lease and exact-SHA identity gate; not mutated
- isolated Railway service creation attempted, rejected before provisioning by Free plan resource provision limit
- Desktop Commander device DESKTOP-FOB7IK8 is offline; terminal unavailable
RUNTIME_VERDICT: NOT_VERIFIED
MUTATION_OWNER_ACTIVE: FALSE
NEXT_ACTION: Run focused auth coverage + verify-otac integration tests when an execution plane is available; preserve the reviewed error-precedence/security invariants.
