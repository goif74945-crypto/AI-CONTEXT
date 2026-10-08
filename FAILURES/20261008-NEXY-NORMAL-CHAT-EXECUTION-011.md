# FAILURE 20261008-NEXY-NORMAL-CHAT-EXECUTION-011
STATUS: PARTIAL / RUNNER_DEPENDENCY_NOT_VERIFIED
CONTEXT: EX010 worker reported real-producer harness strictly compiled, source-contract 5/5, but PostgreSQL/Redis and production worker NOT_RUN and no product commit. GitHub E7 workflow attempt2 failed pre-step, root cause UNKNOWN.
FAILED_APPROACH: treating mock/typecheck/source-contract passes as PG transactional correctness; repeatedly producing importable service harnesses without access to real service runner; overly general claim OWNER cancel lacks lock.
RECOVERY: re-read product run-state.ts and EX010 correction; issue command with finite authorized runner checks, true real PG/Redis execution if available, otherwise independently runnable RED/GREEN repair in separate DOC-C workstream; keep G3 frozen not entire project.
BOUNDARY: Command author did not run app tests or mutate product; cannot certify release.
PREVENTION: trace source contract and actual test executed; preserve HEAD and blobs; separate coverage and completion.
