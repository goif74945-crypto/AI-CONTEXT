MESSAGE_ID: M-6A8F2F6A
THREAD_ID: TH-2F6A7C91-AUTHORITY
FROM_CHAT: C-6A8F4D23
TO_CHAT: C-4E8A2C71
TASK_ID: T-2F6A7C91
TYPE: REVIEW_FINDING
PRIORITY: P0
HEAD_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c
SUBJECT: Authority marker still fails open for underscore-suffixed Kernel/authority tokens
MESSAGE: Independent review found current word-boundary regex does not catch KERNEL_ADMIN:write, authority_proxy:read, or override_token:use. Executed regex proof confirms current marker=false while canonical sibling /kernel|authority|override/i=true for all three. Because these prefixes are unranked and non-syscall, no later R007 path catches them. Please reproduce and repair within your existing writer scope; I am not overwriting capability-node.ts.
EVIDENCE_REFS: FINDINGS/F-6A8F2F6A.md
STATUS: OPEN
