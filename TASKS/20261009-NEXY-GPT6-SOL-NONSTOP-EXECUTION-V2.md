# TASK 20261009-NEXY-GPT6-SOL-NONSTOP-EXECUTION-V2
MODE: ตรวจ / COMMAND_REPAIR
TITLE: Fix premature-termination loopholes in GPT-6 Sol builder prompt
GOAL: Make active-session behavior continue real tool-backed engineering cycles while safe READY work remains.
INPUT: User identified previous V1 command allowed premature stopping.
SOURCE: Live V1 GitHub blob 06f2bb82625bbaadd073effea3bd7415a92fc9f4; actual new V2 command blob c7637f076f93099c206a579bc54b965bbab147e6.
OBSERVED PRODUCT_HEAD_AT_START: 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992.
OBSERVED CONTEXT_HEAD_AT_START: a81a1c6cc078a4efa989b3ba647f8daee83a5fef.
OUTPUT: COMMANDS/20261009-NEXY-GPT6-SOL-NONSTOP-EXECUTION-V2.md.
CHANGE: priority-zero state machine; checkpoint may not become voluntary final; errors freeze action not mission; explicit real external scheduler boundary; Railway fallbacks; cycle index and readback.
EXEC/VALIDATION: Actual GitHub create_file + fetch_file readback; 22/22 structural requirements checked.
TESTS: Prompt review only, no product runtime tests or new Railway deployment.
RISKS: no prompt can override platform session/tool limits or approval boundaries. User wants long-running autonomy; real cross-session runner needs permission and verified invocation.
SUCCESS: Auditable V2 instruction with explicit continuation protocol.
FAILURES: Normal chat alone cannot guarantee background work.
ROLLBACK: Control-repo forward revert after review; no Product mutation.
FINAL_STATUS: COMMAND_VERIFIED_WITH_LIMITS / PRODUCT_BUILD_UNCHANGED_BY_AUDITOR.
VERSION: 2.
TIMESTAMP_SOURCE: 2026-10-09 user local date.
TRACE_ID: 20261009-NEXY-GPT6-SOL-NONSTOP-EXECUTION-V2
