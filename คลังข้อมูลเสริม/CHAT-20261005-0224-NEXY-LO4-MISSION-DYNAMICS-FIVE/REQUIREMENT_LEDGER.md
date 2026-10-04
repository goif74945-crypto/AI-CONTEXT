# Requirement Ledger

| ID | Requirement | Proof required | Status |
|---|---|---|---|
| R01 | Exactly five distinct Lo4 concepts | E0 + final inventory | IN_PROGRESS |
| R02 | Proposal-only, no Canon authority | E0 static labels + audit | IN_PROGRESS |
| R03 | Q64.64 used materially | E1 source audit + E2 numeric tests | PENDING |
| R04 | Signed-128 overflow fails closed; no saturation | E2 boundary tests | PENDING |
| R05 | MLCM design/code/tests/evidence | E0/E1/E2 | PENDING |
| R06 | CERS design/code/tests/evidence | E0/E1/E2 | PENDING |
| R07 | ADA design/code/tests/evidence | E0/E1/E2 | PENDING |
| R08 | HSPG design/code/tests/evidence | E0/E1/E2 | PENDING |
| R09 | NCBC design/code/tests/evidence | E0/E1/E2 | PENDING |
| R10 | Cross-concept integration | E3 executed integration test | PENDING |
| R11 | Negative/freeze paths | E2 executed negative tests | PENDING |
| R12 | No hidden network/provider dependency | E1 source audit | PENDING |
| R13 | No mutation to NEXY.AI-named repository | mutation journal + final audit | IN_PROGRESS |
| R14 | Durable temp memory/checkpoints | GitHub write/readback | IN_PROGRESS |
| R15 | GitHub post-write readback | fetch_file SHA/content verification | PENDING |
| R16 | No runtime/deployment promotion claims | final truth audit | PENDING |

## Status rule
Only executed evidence can move an item to PASS. Code presence alone is not behavior proof.
