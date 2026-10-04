# Test Matrix

| Test family | Cases | Required result |
|---|---|---|
| valid manifest | noncritical, critical | PASS |
| mode contract | unknown, duplicate | FAIL |
| operations | missing cancel | FAIL |
| authority | direct release/write/core mutation/retry | FAIL |
| security | embedded/persisted secret declaration | FAIL |
| timeout validation | critical != 30s | FAIL |
| result semantics | valid result | continue to cross-verify only |
| schema failure | invalid agent result | FREEZE |
| critical timeout | any quorum state | FREEZE |
| noncritical timeout | quorum survives | exclude + continue |
| noncritical timeout | quorum fails | FREEZE |
| noncritical timeout | quorum unknown | FREEZE |
| dependency failure | provider failure | FREEZE |
| determinism | reordered JSON keys | identical digests |
| language parity | Python vs TypeScript | identical case matrix |
| JSON Schema | valid fixtures / invalid fixtures | accept / reject |
