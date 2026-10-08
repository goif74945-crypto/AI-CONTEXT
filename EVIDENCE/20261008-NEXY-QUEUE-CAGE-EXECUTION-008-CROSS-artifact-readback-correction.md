# Execution 008 artifact read-back correction
PRODUCT_HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 (unchanged); patch applies ONLY to exact source blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
Original stored EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cas.patch blob ac06e695aa6e4944acbbaf6d626b5f2a73e91ac8 is INVALID; Git reported 'corrupt patch at line 140' and exit 128. DO NOT USE THAT FILE. Reason proven: missing trailing newline (last characters ' /**' without LF). Remote original patch file had a final LF which Git accepted; read_file result extraction omitted it before the first AI-CONTEXT commit.
Corrected file: EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cas-FIXED.patch, restored LF at EOF from the previously read-back GitHub blob. Verified using that corrected content after rehydration onto isolated Windows runner:
- git apply --reverse --check: exit 0 on candidate
- git apply --reverse: exit 0, original source Git blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29
- git apply --check: exit 0 against original
- git apply: exit 0, candidate source Git blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af
- git diff --check: exit 0.
Also downloaded test artifact EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cancel-race.spec.ts from AI-CONTEXT commit 2f9ee7a02bbea5745770f053ffab97bfaace64c1 back into isolated checkout and executed it unchanged against local candidate: 9/9 passed, exit0.
CI/production status unchanged: REAL PostgreSQL and Redis NOT_RUN, NEXY.ai still unchanged, security/Cage unresolved, DOC-E release NOT_AUTHORIZED.
This is an append-only correction to former evidence: original patch must NOT be used.
