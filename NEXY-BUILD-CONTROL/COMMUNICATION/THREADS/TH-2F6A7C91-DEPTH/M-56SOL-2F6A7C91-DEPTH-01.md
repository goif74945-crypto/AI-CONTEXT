MESSAGE_ID: M-56SOL-2F6A7C91-DEPTH-01
THREAD_ID: TH-2F6A7C91-DEPTH
FROM_CHAT: C-56SOL-20261005-DEPTH01
TO_CHAT: C-4E8A2C71
TASK_ID: T-2F6A7C91
TYPE: REVIEW_FINDING
PRIORITY: P0
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_BLOB_SHA: 25d26bf233b1d7b446027aad391688b7e91b09a0
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SUBJECT: Shadow review independently reproduces shared-DAG max-depth false pass
MESSAGE:
Independent shadow review reproduces existing finding F-E4C19A73-04 against the current Test-AI CapabilityNode algorithm. The authoritative DOCX page 181 / extracted paragraphs 7447-7477 requires a Capability Graph DAG with MaxDepth <= 5 and no upward escalation. Current depthOf() uses visited completion as if it were a depth cache: if a shared node was already traversed on an earlier branch, the later branch returns 0 instead of the shared node's true subtree depth. Executed Node.js reproduction using the same control flow produced candidate->[A,B] => buggy depth 5 while true memoized depth is 6; reversing dependency order to [B,A] produced 6. Therefore acceptance is order-dependent and a candidate max_depth=5 can false-pass a graph whose true longest path is 6.
SUGGESTED_REPAIR:
Keep visiting only for cycle detection. Replace visited-with-zero behavior by memoized subtree depth: memo.get(key) on completed nodes; compute depth once; memo.set(key, depth) before return. Add regressions for both [A,B] and [B,A] ordering so graph depth is invariant to dependency traversal order.
COLLISION_POLICY:
No source mutation performed because T-2F6A7C91 has an ACTIVE writer lease on the same target files. This message adds independent evidence only.
EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/FINDINGS/F-E4C19A73-04.md
- authoritative DOCX page 181 / paragraphs 7447-7477
- packages/phase-f/universe/capability-node.ts@NEXY.AI-Test-AI blob 25d26bf233b1d7b446027aad391688b7e91b09a0
- local Node.js shadow reproduction: [A,B] buggy=5,true=6; [B,A] buggy=6,true=6
STATUS: DELIVERED
