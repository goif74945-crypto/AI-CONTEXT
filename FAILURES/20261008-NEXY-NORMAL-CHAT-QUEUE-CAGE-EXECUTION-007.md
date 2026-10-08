# FAILURE 20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007
TITLE: Previous worker could not run integration/CI proof
CONTEXT: Handoff 006 product HEAD 44bcb851; worker claimed read/write but Repo Code Bridge ci_dispatch returned 403 REPOSITORY_READ_ONLY; product Vitest/Postgres/Redis/browser/bwrap not run in that chat.
CAUSE: specific integration access/capability gap; no evidence of global unavailability.
FAILED_APPROACH_TO_AVOID: Treat 403 for one endpoint as proof every runner is blocked, or count model-only assertions as integration proof.
RECOVERY: discover an actually authorized runner through available tools, or keep product changes frozen and write exact patch + negative test proposal to AI-CONTEXT while continuing audited READY work. Re-query GitHub Actions via supported lists instead of relying on PR-only filtered results.
LIMIT: Our command-generation turn did not run product tests or repair source; future execution required.
NEXT: same normal-chat worker executes COMMANDS/20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007.md
STATUS: BLOCKER_RECORDED_WITH_ALTERNATE_PATHS
