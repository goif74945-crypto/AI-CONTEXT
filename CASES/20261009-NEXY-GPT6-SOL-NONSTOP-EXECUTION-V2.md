# CASE 20261009-NEXY-GPT6-SOL-NONSTOP-EXECUTION-V2
CASE: PREMATURE_STOP_AFTER_BLOCKER_OR_CHECKPOINT
SEVERITY: S3 workflow reliability, not a security release proof.
CAUSE: V1 permitted a chat to emit status and RESUME_HANDOFF at arbitrary point; instructions lacked a strict tool-call transition after completed checkpoint.
IMPACT: Model could stop engineering even when alternative safe work remained.
FIX: V2 priority-zero execution state machine requires next READY tool-backed action in same active session after checkpoint; nonblocked tasks continue after Railway/Cargo/DB failure; auditable STOP_EVIDENCE for actual termination.
NEGATIVE_CONDITIONS: V2 forbids fabricated runtime, false approvals, force pushes, unsafe production DB writes and unbounded billing; cannot truly extend platform runtime.
REGRESSION_GUARD: Reviewer verified 22 critical prompt elements; prompt behavior still must be evaluated by real builder tools.
SCOPE: COMMAND only; no code fixes from auditor.
