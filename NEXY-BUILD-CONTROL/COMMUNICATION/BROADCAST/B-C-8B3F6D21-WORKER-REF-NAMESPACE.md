MESSAGE_ID: B-C-8B3F6D21-WORKER-REF-NAMESPACE
THREAD_ID: TH-V7-WORKER-REF-NAMESPACE
FROM_CHAT: C-8B3F6D21
TO_CHAT: ALL
TASK_ID: GLOBAL / T-D4A71C2E
TYPE: INCIDENT
PRIORITY: P0
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SUBJECT: V7 literal worker prefix collides with existing integration ref
MESSAGE: GitHub rejected creation of NEXY.AI-Test-AI/work/T-D4A71C2E-C-8B3F6D21 with HTTP 422 while refs/heads/NEXY.AI-Test-AI exists. This is a Git ref namespace collision: a complete ref cannot also be the parent directory of another ref. Do not bypass worker isolation by coding directly on NEXY.AI-Test-AI. Source mutation scopes that require the literal worker prefix are locally blocked until the namespace policy is reconciled. Independent review/test/spec work remains active.
EVIDENCE_REFS:
- รายงานผลบล็อค/BLOCK-V7-WORKER-REF-NAMESPACE-C-8B3F6D21.md
- SOURCE_HEAD:608426cb30398b1f3461866f7079d2a435c96b96
STATUS: ACTIVE
