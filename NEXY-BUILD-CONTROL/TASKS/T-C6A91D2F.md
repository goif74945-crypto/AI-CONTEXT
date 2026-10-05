TASK_ID: T-C6A91D2F
CREATOR_CHAT: C-SOL-20261006-0142-SMARTSILENCE
OWNER_CHAT: C-SOL-20261006-0142-SMARTSILENCE
STATUS: SUPERSEDED_BY_AUTHORITY_CORRECTION
PRIORITY: P1
RISK: LOW
BASE_SHA: ec315100883f1a3ab841b97e1fe6ad820e9b2b2f
WORKER_HEAD_SHA: 226cec9b8445db51b63477dd7a69f139f0aeeff1
INTEGRATED_SHA: 97bd3624969a38dcdc3df3e22dbc931aa03814bd
PR: 21
TARGET_PATHS:
- packages/human/smart-silence.ts
- packages/human/__tests__/smart-silence.test.ts
SEMANTIC_SCOPE:
Restore the deterministic Human Gravity Smart Silence policy required by the authoritative NEXY-IGNIS spec onto the current NEXY.AI-Test-AI lineage. Port only the previously independently reviewed decision semantics: ask one soft probe iff silence strictly exceeds caller-provided threshold, no error exists, no task is pending, and no probe was already sent; otherwise stay silent. No Core mutation, persistence, tools, dialog-provider wiring, threshold invention, or protected NEXY.ai mutation.
AUTHORITY:
- Authoritative spec Smart Silence Logic: user_silent > threshold AND no_error AND no_pending_task => ask_single_soft_probe(); ELSE stay_silent; one probe only; unanswered => no follow-up spam.
- Prior independent review NEXY-BUILD-CONTROL/REVIEW/T-6F2C8A13--C-7E4D2B19.md covers the exact source/test blobs.
ACCEPTANCE_RESULT:
1. PASS: current lineage contains packages/human/smart-silence.ts.
2. PASS: strict > threshold boundary preserved.
3. PASS: error, pending task and already-sent probe suppress probing.
4. PASS: malformed/non-deterministic numeric input fails closed.
5. PASS: module has no Core/Vault/state/persistence/tool authority.
6. PASS_SCOPED: exact Git source blob compiled with tsc --strict and executed under Node 22 with 14 assertions; fresh repository-native workflow runs were triggered post-integration but failed before any step executed.
7. PASS: NEXY.ai was not targeted or mutated by this task.
RUNTIME_EVIDENCE:
- source blob 4d29d55ef4d6e15f9ba27c78b2ec2f482b34f8cd
- test blob 256400dd9038e8e8e3dd18fe02d68de8177a9683
- SMART_SILENCE_EXACT_BLOB_COMPILE_PASS
- SMART_SILENCE_ASSERTIONS_PASS=14
- Exact HEAD workflow run 37359689443 at integrated SHA 97bd3624: failure before execution; job 111930866055 has zero steps and no log artifact.
- Six-system workflow run 37359689430 at integrated SHA 97bd3624: failure before execution; job 111930866143 has zero steps and no log artifact.
LIMITATION:
Fresh full-repository GitHub runtime remains infrastructure-blocked at runner allocation. This task does not claim full-repository PASS.
INTEGRATION_VERIFY:
- integrated source/test blobs equal worker blobs exactly.
- integrated SHA 97bd3624 is an ancestor of current observed NEXY.AI-Test-AI HEAD 2926222d9c4cece6f20a9343256c5157d6176f4f.
NEXT_ACTION:
None for this pure-policy restoration scope. Separate wiring task is required only after an authoritative threshold/configuration source is identified; do not invent a threshold.

AUTHORITY_CORRECTION:
- historical Human Gravity prose is not build authority under the DOCX FINAL VERDICT
- repair PR: 63
- repair SHA: aaec8ace3c1fc3ba1472737d7bef1fda8c1c31ad
- current required state: Smart Silence source/test absent
- correction finding: F-T-C6A91D2F-AUTHORITY-SELF-REPAIR
