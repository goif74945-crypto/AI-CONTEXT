# FAILURE 20261008-NEXY-NORMAL-CHAT-EXECUTION-009
CATEGORY: INTEGRATION_VERIFICATION_GAP
STATUS: OPEN / PRODUCT_NOT_FIXED
WHAT_FAILED_OR_IS_MISSING: Execution 008 reported RED/GREEN mock tests and typecheck for one candidate, but no real PostgreSQL plus Redis runtime tests; cage Linux isolation not tested; GitHub CI pre-step failures still of unknown cause.
PATCH_ARTIFACT_FAILURE: original 008 queue-cas.patch has missing trailing newline; worker reports git apply corrupt patch line 140. Fixed patch stored separately and direct content read verified ending newline.
UNVERIFIED: output-release boundary under cancelled job, actual Redis publication before DB CAS, restart recovery, Linux seccomp enforcement, DOC-E deployment gates.
ROOT_CAUSE: missing authorized integrated service runner and divergent candidate sets; infrastructure CI cause not proven.
ALTERNATES: investigate existing authorized runner; create real test harness stored to control if no runtime, audit independently testable subsystem. Never treat 9/9 mock as E2E.
RECOVERY_TARGET: COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-009.md
