# LEDGER — 20261007-REPO-CODE-BRIDGE-CROSS-CAPABILITY-002

| Source | Claim | Proof | Dependency | Risk | Status | Trace |
|---|---|---|---|---|---|---|
| Live runtime_status | Bridge/GitHub/D1/read/write/CI backends available | Runtime returned CONNECTED/READY | Site gateway and auth | Provider state can change | VERIFIED_WITH_LIMITS | RBC-CROSS-002 |
| Live AI-CONTEXT status | main was pinned at pre-write HEAD 9ebce59a... | repo_status exact branch/head | GitHub access | Concurrent write after snapshot | VERIFIED | RBC-CROSS-002 |
| Live catalog + product status | exact NEXY.AI- is selectable read-only on NEXY.ai | catalog entry + status read_only=true, DENY | Allowlist and policy | Policy can drift | VERIFIED | RBC-CROSS-002 |
| Live product read/search | Bridge can read exact product HEAD | README read; DOC-C search; SEARCH_SCOPE_PARTIAL retained | Product HEAD 9e615b04... | Search not exhaustive | VERIFIED_WITH_LIMITS | RBC-CROSS-002 |
| Live open_vscode | Web handoff returns exact head and read-only metadata | vscode.dev URL, URL-only launch status | Browser session required | Not a desktop launch | VERIFIED_WITH_LIMITS | RBC-CROSS-002 |
| Existing task record | access was blocked | Conflicts with refreshed live state | Stale record | Misrouting | STALE | RBC-CROSS-002 |
| Existing evidence record | allowlist/read-only path existed | Consistent with refreshed live state | Evidence record freshness | Historical limits retained | SOURCE_PROVEN | RBC-CROSS-002 |

CHANGE: Added one evidence record at AI-CONTEXT pre-write HEAD 9ebce59a...; commit 065b539657f4376d949c8bf3d6808240728c7711.
READ_BACK: Evidence path exists at AI-CONTEXT post-write HEAD 065b539...; blob 507864c75f05cfd0eb5abcb5a8ea4398170a66ff.
PRODUCT_STATE: NEXY.AI- / NEXY.ai / 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43 unchanged; read-only/DENY.
VERDICT: PARTIAL / VERIFIED_WITH_LIMITS.
