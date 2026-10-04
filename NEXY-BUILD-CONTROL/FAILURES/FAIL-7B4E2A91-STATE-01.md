FAILURE_ID: FAIL-7B4E2A91-STATE-01
REPORTER_CHAT: C-7B4E2A91
TASK_ID: T-D4A71C2E
STATUS: OPEN
PRIORITY: P0
RISK: HIGH
NEXY_BRANCH: NEXY.AI-Test-AI
EXACT_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c
RAILWAY_DEPLOYMENT: 3356b6d7-a35c-4aa5-b25c-aedc67367ded
FAILURE_STAGE: BUILD_IMAGE / npm run test:contract

SUMMARY:
Exact-SHA executable validation confirms the state-machine authority regression introduced by 27af7f93893c7589e516c269fae41aa467c2cdb9.

EXECUTION_RESULT:
- Test Files: 3 failed | 114 passed (117)
- Tests: 5 failed | 647 passed (652)
- Contract command exited 1.

FAILED_TESTS / OBSERVED EFFECTS:
1. tests/contract/core-kernel-vnext-parity.test.ts
   Rust transition set has 5 additional required error->FREEZE rows relative to the narrowed TypeScript oracle:
   - Consensus|Error|Freeze
   - Freeze|Error|Freeze
   - Init|Error|Freeze
   - Ready|Error|Freeze
   - Stable|Error|Freeze
2. tests/contract/hydration-fail-closed.test.ts
   bootstrap failure expected FREEZE but remained INIT.
3. tests/contract/hydration-fail-closed.test.ts
   READY --error--> FREEZE was denied by VNextStateTransitionDeniedError.
4. tests/contract/system-state-persistence.test.ts
   READY --error--> FREEZE was denied for CORE.
5. tests/contract/system-state-persistence.test.ts
   expected AUDIT_PERSIST_FAILED_FREEZE path was pre-empted by STATE_TRANSITION_DENIED on READY/error.

AUTHORITY:
Final DOC-C §5.4 explicitly defines ANY except STOP + error -> FREEZE. Therefore these are not merely legacy tests resisting a new design; they exercise the final fail-closed law.

ROOT_CAUSE:
T-D4A71C2E misclassified five final-DOC-C error edges as unauthorized and removed them. Its exact-set regression oracle encoded the narrowed relation.

SAFE_REPAIR:
Restore the five deleted error->FREEZE rows in packages/core/vnext-state-matrix.ts and align tests/contract/state-matrix.test.ts with the final DOC-C ANY-except-STOP error law. Then rerun exact-SHA contract validation. Do not weaken/remove the failing downstream tests.

EVIDENCE_REFS:
- Railway deployment 3356b6d7-a35c-4aa5-b25c-aedc67367ded
- exact commit 5034debdadb1f21c7d5312e6f0ad7fd44280718c
- F-7B4E2A92
- E-7B4E2A91-02
- authoritative DOCX final DOC-C §5.2/§5.4/§5.6

TRUE_BLOCK: false
