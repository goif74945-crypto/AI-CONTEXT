# AI.AI Criticism and System Idea Registry

Every chat must check the entire directory, not merely this table, before proposing new work. IDs/fingerprints are a mechanical collision check; semantic equivalence is judged from code and behavior. Recheck at newest AI-CONTEXT/main HEAD immediately before publication.

| ID | Critique signature | Idea fingerprint | Source pinned | Status |
|---|---|---|---|---|
| [AAI-20261009-001](PROPOSALS/AAI-20261009-001-file-read-integrity/) | F-01 / executor.file.read / silent truncation of output at 20,000 chars | read-integrity/file-read/fail-closed-on-result-truncation | v0.2.0 zip / 0b226669d5635339c00c3836d91dca9bfbf63cea | TESTED_ON_PINNED_REVISION, v0.3 NOT_VERIFIED |
| [AAI-20261009-002](PROPOSALS/AAI-20261009-002-adaptive-ocr-click/) | F-02 / executor._desktop_text / initial OCR center used for click after <=8px target drift | desktop/ocr-click/third-frame-recheck-when-offset-and-click-latest-confirmed-center | v0.4.0 zip / 95741bede86405685a022633df03a2c39ce7fc4c | TESTED_ON_PINNED_REVISION, 224 local Python PASS, physical E2E NOT_RUN |

| [AAI-20261009-003](PROPOSALS/AAI-20261009-003-chrome-companion/) | F-03 / browser adapter isolated Playwright + 180s plan TTL / no user Chrome MV3 long-running workflow | chrome-mv3/sidepanel/optional-origin/alarms-checkpoints/manual-uncertain-resolution | v0.4.0 zip / 95741bede86405685a022633df03a2c39ce7fc4c | TESTED_ON_PINNED_REVISION, Python 216 + Node 14 + Chromium DOM 13 PASS, Chrome install BLOCKED |

Future AI chats MUST NOT resubmit AAI-001's file-read truncation critique or AAI-002's adaptive OCR click-stability critique or AAI-003's Chrome MV3 resumable workflow gap or semantically equivalent fixes as new. If no unique proposal is verifiable, stop with BLOCKED_UNIQUE_IDEA. The historical PROJECTS/AI.AI v0.3 release record does not prove this v0.2-specific patch works on v0.3.
