# NEXY.AI Cloud Android + ChatGPT 30-Minute Pilot
Date: 2026-10-10 Asia/Bangkok
Status: BRANCH_CREATED / PILOT_NOT_STARTED
Trial branch spelling is **exactly** `NEXY.AI-Teat-AI` (not Test-AI).
Experiment ID: CLOUD-ANDROID-30M-PILOT-20261010
Repository: goif74945-crypto/NEXY.AI-
BASE_BRANCH: NEXY.ai
EXPERIMENT_BRANCH: NEXY.AI-Teat-AI
BASE_AND_TEST_INITIAL_HEAD: 58b1200bd61b867e917057d0019eea78ea9f6b2a

## Verified Evidence (tool-backed)
1. GitHub search_branches on `NEXY.AI-` initially reported only `NEXY.ai`, and no exact `NEXY.AI-Teat-AI`.
2. GitHub branch creation returned `NEXY.AI-Teat-AI`, from exact base SHA above.
3. GitHub search_branches readback found the branch.
4. GitHub compare_commits(`NEXY.ai`, `NEXY.AI-Teat-AI`) reported `status=identical`, `ahead_by=0`, `behind_by=0`, `total_commits=0`, `files=[]`.
5. Repo Code Bridge `repo_catalog` reported the Product allowlist contains only branch `NEXY.ai`; it does NOT currently authorize the test branch. **DO NOT** use Repo Code Bridge to write to the test branch until an explicitly authorized allowlist change is verified. A separate connected GitHub tool or approved exact-branch runner is required.
6. Repo Code Bridge `repo_status` listed two active workflow names about pruning branches other than `NEXY.ai`; corresponding source paths returned 404 at current HEAD, so their execution triggers are **UNKNOWN**, not proof that pruning will occur. Re-check the test branch's existence before every mutation and after each cycle.
7. Prior architecture/proposal: `TASKS/20261010-NEXY-CLOUD-ANDROID-AUTOCLICKER-FEASIBILITY.md`.

## Objective
**Test**, not assume, whether a rented Cloud Android device running ChatGPT can send one continuation command every 30 minutes AND lead to objectively verifiable work. Track UI attempt success separately from actual engineering results and safety.

## Scope and immutable boundaries
IN SCOPE: isolated experimentation on exact test branch only; basic ChatGPT message delivery; branch reads; (if properly authorized and supported) minimum code/test change on the test branch; real focused test evidence; append-only experiment reports in AI-CONTEXT/main.
OUT OF SCOPE: changes/commits/CI dispatch on NEXY.ai; deletions of branches; modifying workflows, branch protection, secrets, permissions, production deployments or databases; spending money without approval; claiming spec compliance without authoritative DOCX+tests.
SPEC: actual byte-verified NEXY-IGNIS DOCX with SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7. Previous command `COMMANDS/20261009-NEXY-GPT6-SOL-143-FIX-UNTIL-VERIFIED-V4.md` defines initial gates; 143 are NOT all defects and not necessarily the full DOC-C inventory.

## Minimum practical pilot
PHASE P0 (initial 2-cycle test, then extend only after verification):
- In a rented Cloud Android instance, the owner logs in using a trusted provider. Do not put credentials/API keys into chat messages, macros or logs. Enable a kill switch and be ready for UI session expiration and provider screenshot access.
- Open ONE ChatGPT conversation. Select actual available model and connected GitHub tools; verify tools are authorized for the **experiment branch**. If the only write tool is Repo Code Bridge with current allowlist, record BLOCKED and DO NOT redirect writes to NEXY.ai.
- At T0, submit the initial task from the section below; record actual start time, assistant reply, tools used, repository branch+HEAD, test command/exit code, resulting commit SHA.
- At T+30m, submit a continuation only **if prior assistant/tool execution is complete and the chat is idle**. A blind timer is NOT evidence of idle status. If UI cannot check, stop the test rather than double-submit.
- At T+60m, independently inspect the test branch on GitHub. Compare HEAD / changed files / verified test receipts. Count scheduled taps, delivered messages, completed assistant cycles, valid test runs and current-head commits **separately**.
- If two cycles work, a 24-hour run has up to 48 half-hour opportunities, NOT a promise of 48 completed engineering changes. Never use automation to bypass ChatGPT usage limits/protective controls.

## Initial task to paste in ChatGPT (owner action)
```text
EXPERIMENT: CLOUD-ANDROID-30M-PILOT-20261010
MODE: EXACT_BRANCH_ONLY / EVIDENCE_FIRST / FAIL_CLOSED / REAL_TESTING
REPOSITORY: goif74945-crypto/NEXY.AI-
EXACT BRANCH: NEXY.AI-Teat-AI
CONTROL LOG: goif74945-crypto/AI-CONTEXT / main
BASELINE BEFORE ANY TEST PATCH: 58b1200bd61b867e917057d0019eea78ea9f6b2a

Do not modify NEXY.ai or any other branch, GitHub settings, branch protections, workflows, secrets or production services.
Read exact current test HEAD and check the actual branch still exists. Obtain required authoritative DOCX and hash its bytes before claiming DOC-C spec verification.
Choose one small, READY, independently verifiable engineering task. If there is no safe authorized tool route to write to the exact test branch, run read-only checks and report BLOCKED; never substitute NEXY.ai.
For any code change: reproduce issue; run RED test; make minimal change to exact test branch; run GREEN and regressions; capture command, exit, blob/commit SHA, and readback. Do not claim test execution that did not happen.
Record truthful result and next READY item in AI-CONTEXT if the connected tool permits append-only, and cite its commit. End each cycle with a short machine-readable checkpoint.
If previous cycle is still running, branch changed unexpectedly, model/tools rate-limited, or a policy constraint applies: STOP the current action and report the evidence.
```

## Every 30-minute continuation text (only when idle)
```text
CONTINUE EXPERIMENT CLOUD-ANDROID-30M-PILOT-20261010. First read the last VERIFIED checkpoint from AI-CONTEXT, confirm NEXY.AI-Teat-AI still exists and capture its current HEAD. Select the next authorized READY item, run real source/test/audit steps, and record a truthful checkpoint. Never touch NEXY.ai. Do not duplicate a prior action or claim PASS without evidence. If the previous job is incomplete or a safe route is unavailable, report BLOCKED and stop.
```

## Checkpoint schema per cycle (never invent values)
```json
{"experiment_id":"CLOUD-ANDROID-30M-PILOT-20261010","cycle_id":null,"scheduled_time":null,"sent_at":null,"ui_delivery":"NOT_TESTED","assistant_completed":false,"selected_branch":"NEXY.AI-Teat-AI","start_head":null,"end_head":null,"changed_files":[],"test_runs":[],"verified_commit_shas":[],"checkpoint_location":null,"status":"NOT_STARTED","blockers":[]}
```

## Stop/Failure gates
- Missing or changed test branch; unauthorized write permissions; accidentally selected NEXY.ai; unexpected concurrent HEAD change.
- Long-running assistant reply at scheduled time, login/consent UI, UI layout drift, rate limit, no working runner or GitHub tool, unsafe external storage.
- Missing DOCX hash or ambiguous spec semantics: block spec-dependent writes only; evidence-based read-only tasks may continue.
- Never equate UI click count with engineering progress. Independently verify current GitHub HEAD, source, test outputs and checkpoints.

## Confirmed status when this record was authored
TEST_BRANCH_CREATED=true
BRANCH_READBACK_VERIFIED=true
INITIAL_COMPARE_IDENTICAL=true
CLOUD_ANDROID_RENTED=NOT_VERIFIED
AUTO_CLICKER_CONFIGURED=NOT_VERIFIED
CHATGPT_CYCLES_COMPLETED=0 VERIFIED
REAL_TESTS_EXECUTED=0 VERIFIED
PRODUCT_CODE_CHANGED=NO
AI_CONTEXT_RECORD=THIS FILE
