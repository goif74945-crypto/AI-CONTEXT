# NEXY Deep Research Full Spec↔Code Audit Prompt V1

TASK_ID: NEXY-DEEP-RESEARCH-FULL-SPEC-CODE-AUDIT-PROMPT-V1
MODE: PROMPT_DESIGN + CURRENT_STATE_REFRESH
DATE: 2026-09-26

## User objective
Create a Deep Research instruction that must exhaustively compare the authoritative NEXY-IGNIS design source with the real NEXY implementation, read every tracked implementation file at a pinned revision, produce a file-completeness ledger and a system/requirement matrix, and classify implemented/missing/partially mismatched items without guessing.

## Verified current anchors before prompt creation
- AI-CONTEXT main observed HEAD: a8986f0baf0c769f64cf945f03c7b501bf76f0df
- Authoritative source file SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- Local source extraction: 12,537 paragraphs; 10,979 non-empty paragraphs; 17 sections; no Word tables; no Heading-style paragraphs.
- NEXY.AI- branches observed: NEXY.ai and astra/omega-full-spec-convergence.
- NEXY.ai observed HEAD: 42378126aed29a668f9f294a9100c62a66ff3753
- astra/omega-full-spec-convergence observed HEAD: 1714d8fbb78372e6bd5ddd9bcd8d58599d13dc32
- NEXY.ai tracked blobs at observed tree: 613
- astra tracked blobs at observed tree: 620
- Compare NEXY.ai→astra: diverged; merge-base d839ee6a0958be18173005d1356ccc738142523e; astra has 48 commits beyond merge-base and current diff contains 13 paths.
- AI-CONTEXT current snapshot is branch-specific to astra and records source/runtime gates validated but release authorization blocked.
- AI-CONTEXT latest mismatch matrix is stale (pinned to implementation head 317e619f5331a2d1ce9aa0016a18bc1d3f143270).
- AI-CONTEXT implementation/INDEX.md remains pinned to historical branch codex/spec-audit-20260919-78df350 / 9c9befd9..., so it must not be used as current implementation truth without refresh.

## Durable rules
- Refresh all refs before research; anchors above are evidence of this prompt-design pass, not permanent truth.
- Primary canonical audit target should follow current user/source authority; recent user direction identifies NEXY.ai as canonical. Audit astra separately as a divergent/latest development branch and never merge branch evidence silently.
- Build two denominators: all source obligations and all tracked implementation blobs.
- Every tracked file receives a terminal read/disposition status.
- Every source obligation receives a terminal implementation comparison status.
- Absence from one search is not MISSING.
- MATCHED_100 requires semantic match with no material unknown; file presence never proves it.
- Historical/stale tests/evidence cannot prove the pinned current HEAD.
- NEXY implementation remains read-only during Deep Research unless separately authorized.
- Persist checkpoints/results to AI-CONTEXT when write access is available and verify read-back; otherwise emit an AI_CONTEXT_IMPORT_PACKAGE.

## Final status
PROMPT_READY
