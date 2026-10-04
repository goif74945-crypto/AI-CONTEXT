FINDING_ID: F-6A8F5C4D
FROM_CHAT: C-6A8F4D23
TASK_ID: T-B7E4C2A1
HEAD_SHA: d1d80ce99d533a79294425ebcfe132551b26cc43
SEVERITY: P0
TYPE: AUTHORITY_CONFLICT
OBSERVATION: Two active repair tasks hold contradictory DOC-C transition oracles. T-A6C4E9B2 plans to remove Rust error->FREEZE edges for INIT/READY/CONSENSUS/STABLE/FREEZE, while T-D4A71C2E states final DOC-C requires error->FREEZE from every state except STOP.
AUTHORITATIVE_RESOLUTION: The authoritative spec "แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx", DOC-C §5.4 Transition Table, explicitly states ANY except STOP + error -> FREEZE (always). Therefore removing those Rust edges is contrary to the authoritative spec. The TypeScript regression that denies READY/INIT/etc error transitions must be repaired instead of mirrored into Rust.
EXECUTABLE_EVIDENCE: Frozen Railway deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8 for exact SHA 5034debdadb1f21c7d5312e6f0ad7fd44280718c passed source identity and then failed 5 contract assertions. Failures include core-kernel-vnext-parity extra Rust error edges, hydration tick-ledger failure leaving INIT instead of FREEZE, and READY --error--> rejection breaking system-state persistence incident tests.
FACT:
- Authoritative DOC-C §5.4 says ANY except STOP error -> FREEZE.
- Current Rust contains the corresponding five edges that TypeScript commit 27af7f removed.
- Exact-head executable tests demonstrate the TypeScript denial causes fail-closed behavior regressions.
ASSUMPTION: None required to resolve the edge authority conflict.
UNKNOWN: Whether T-A6C4E9B2 has already produced an unpublished source mutation; work HEAD inspected before this finding showed no committed Rust removal.
EXPECTED: Preserve/restore error->FREEZE for every non-STOP state and align tests to the authoritative rule.
SUGGESTED_DIRECTION: T-A6C4E9B2 must stop the planned Rust edge removal. T-D4A71C2E should continue restoring the TypeScript non-STOP error edges and re-run exact-head validation.
EVIDENCE_REFS: authoritative DOC-C §5.4; Railway deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8; T-A6C4E9B2; T-D4A71C2E; F-B7E4C2A1
