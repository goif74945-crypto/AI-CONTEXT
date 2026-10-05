TASK_ID: T-C6A91D2F
CREATOR_CHAT: C-SOL-20261006-0142-SMARTSILENCE
OWNER_CHAT: C-SOL-20261006-0142-SMARTSILENCE
STATUS: IMPLEMENTING
PRIORITY: P1
RISK: LOW
BASE_SHA: ec315100883f1a3ab841b97e1fe6ad820e9b2b2f
TARGET_PATHS:
- packages/human/smart-silence.ts
- packages/human/__tests__/smart-silence.test.ts
SEMANTIC_SCOPE:
Restore the deterministic Human Gravity Smart Silence policy required by the authoritative NEXY-IGNIS spec onto the current NEXY.AI-Test-AI lineage. Port only the previously independently reviewed decision semantics: ask one soft probe iff silence strictly exceeds caller-provided threshold, no error exists, no task is pending, and no probe was already sent; otherwise stay silent. No Core mutation, persistence, tools, dialog-provider wiring, threshold invention, or protected NEXY.ai mutation.
AUTHORITY:
- Authoritative spec Smart Silence Logic: user_silent > threshold AND no_error AND no_pending_task => ask_single_soft_probe(); ELSE stay_silent; one probe only; unanswered => no follow-up spam.
- Prior independent review NEXY-BUILD-CONTROL/REVIEW/T-6F2C8A13--C-7E4D2B19.md: PASS_WITH_OWNER_SUITE_PENDING for source blob 4d29d55e... and test blob 256400dd...
ACCEPTANCE_CRITERIA:
1. Current-lineage source exposes deterministic Smart Silence decision function.
2. Threshold boundary is strict >, never >=.
3. Error, pending task, and already-sent probe suppress probing.
4. Malformed/non-deterministic numeric input fails closed.
5. Module has no Core/Vault/state/persistence/tool authority.
6. Focused tests are added; exact execution evidence required before integration if runner is available.
7. NEXY.ai remains unchanged.
