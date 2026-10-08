# EVIDENCE 20261008-NEXY-NORMAL-CHAT-EXECUTION-008 — command review
STATUS: COMMAND_VERIFIED_WITH_LIMITS
TARGET: the already-working ordinary ChatGPT execution conversation, not Codex.
VERIFIED LIVE AT REVIEW:
- product NEXY.ai HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
- 007 control commit fc7dc9570cbe2d3a9a287db1c2613b1f97739cb7
- all 007 evidence and model test read at 007 commit.
- Five current-head CI runs failed; exact-head and E7 examined jobs had steps=[].
- Command 008 present in AI-CONTEXT/main; initial review detected 1 wording omission ("CAS alone insufficient") and repaired via update_file commit 99593e57025475f731b430d6ba47d94fd0d4b3ee.
REVIEW_TOPICS: same chat, current HEAD fence, exact spec SHA, repo runner truth, actual product-linked RED tests, cancel-race CAS guards, external Redis job publication, worker claim pre-commit, no terminal resurrection, cage direct spawn, no seccomp-fake, TSA unchanged, CI pre-step source, no guessed root cause, DOC-E gate, 98-row audit, AI-CONTEXT close, no model-only completion.
AUDIT_RESULT: review of command structure, not of code/test success. Product tests executed by author: NONE.
