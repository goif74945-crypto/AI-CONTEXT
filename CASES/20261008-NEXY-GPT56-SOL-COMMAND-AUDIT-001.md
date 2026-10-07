# Case — Concurrent Branch Drift During Command Audit

CASE_ID: 20261008-NEXY-GPT56-SOL-COMMAND-AUDIT-001
CAUSE: Another concurrent workflow/chat changed branch topology while the command audit was running.
VIOLATION_RISK: Hardcoding an earlier live branch would have produced a stale command and likely immediate BLOCKED/no-start behavior.
OBSERVED:
- earlier: NEXY.ai + NEXY-IGNIS, NEXY-IGNIS@72b105be..., ahead 31
- final gate: NEXY.ai only, HEAD 9e615b04...
IMPACT: Required command architecture change from fixed NEXY-IGNIS target to live existing user-authorized branch resolution, with branch creation forbidden.
FIX: Re-query branch topology before every mutation; freeze only mutation on unexpected drift; continue safe read-only work.
PREVENTION: Never convert a mid-run branch observation into permanent authority.
REGRESSION: Final command explicitly contains branch topology recheck and no-branch-create law.
STATUS: CLOSED_FOR_COMMAND_DESIGN