# RCB-002 live connector verification correction

Task: RCB-OMEGA-RCB002-20261010
Date: 2026-10-10 (UTC)
Addendum to: EVIDENCE/RCB-002-FULL-TREE-EXPLORER-20261010-e6eccc6.md

## Correction

The prior report says the live authenticated `repo_tree` call returned HTTP 401 and remains unverified. That is accurate only for the direct raw HTTP request from the browser runtime. It does not describe the authenticated Repo Code Bridge connector call.

After v19 deployment, the configured Repo Code Bridge connector exposed `repo_tree`. A direct invocation through that authenticated connector succeeded against AI-CONTEXT/main at exact revision `110da12ec9ca78e83708910a524dc4b5b7bc9f2a`.

- Page 1: `max_entries=10`, returned 10 exact-revision tree entries, `revision_verified=true`, `complete=false`, `truncated=true`, `incomplete_reason=TREE_PAGE_CONTINUES`, and a continuation cursor. Provider pages: 10; errors: []; duration: 3371 ms.
- Page 2: supplied the returned cursor with the same repository and exact revision; returned the next 10 entries, `revision_verified=true`, `complete=false`, `truncated=true`, `incomplete_reason=TREE_PAGE_CONTINUES`, and a next cursor. Errors: []; duration: 3370 ms.
- The Site audit log showed `repo_tree goif74945-crypto/AI-CONTEXT PARTIAL` at 2026-10-10 08:42:11 and 08:42:25 UTC. PARTIAL is the expected bounded-page state, not a failed call.
- The live tool returned stable paths, Git tree/blob SHAs, modes, entry kinds, and file sizes where applicable.

Thus, the authenticated platform connector's live tree behavior is VERIFIED for exact-revision traversal and continuation across two bounded pages. Direct unauthenticated/raw HTTP invocation remains UNAUTHORIZED (HTTP 401) in this browser runtime; no claim is made that raw HTTP is authenticated. These two observations are not contradictory.

The 3370/3371 ms values are two individual calls, not a performance benchmark. No performance improvement is claimed. No repository was modified by these read-only live calls.

## Provenance

The source implementation is Site v19, source commit `e6eccc6e0fd210b6f690fdb535e6a816a14f82c3`, deployed as `appgdep_6ac9fa11cd8c819199db1730bf203171`. Evidence append is a separate AI-CONTEXT record and is not product-source evidence.
