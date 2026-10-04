# GitHub Readback Evidence

Authority class: E0 presence/content identity evidence plus repository-diff evidence.
Target repository: `goif74945-crypto/AI-CONTEXT`
Target path: `คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-SUPPLY-CHAIN-SENTINEL/`

## Initial code/evidence commit
- Commit: `10b7fbddff35353b9231110fa1af74df48abf637`
- Parent: `140b12b49383942c5c709466448284e93f865115`
- Project tree: `ffe327d71c94bc196e821ccf69f9618a5705bbf8`
- Commit relation: ahead by exactly 1 commit from its parent.
- Compare result: 30 files added, all under the unique target path; no deletions and no file outside the target path changed.

## Exact tested blob identity
Selected critical Git blob SHAs from the committed tree match the locally tested files:
- `tests/test_sentinel.py`: `72ea6e08b9fc8dc3fc15f9c61869b37986e5e9f4`
- `src/nexy_supply_chain_sentinel/engine.py`: `b0981ae9a3d092ebcae0535e0acdca7934da72d7`
- `src/nexy_supply_chain_sentinel/parsers.py`: `2f70f6c793c0424480d1d3a8ab3d9e3dd0b74c5d`
- `src/nexy_supply_chain_sentinel/diffing.py`: `38e2a88e049dcf5f596c5cfbdf569f5b7d6fdb9b`
- `src/nexy_supply_chain_sentinel/policy.py`: `3cee97fe6cfd2c2575e9f4d4842d79b06a01dae4`
- `src/nexy_supply_chain_sentinel/cli.py`: `c498c5316658ea4d4e73d3233380f1cc4566d129`
- `evidence/FINAL-UNIT-TEST.txt`: `0f7fb59c12fdf6216f2dbe6ef1a9dd6c6ec8df28`

## Concurrency observation
After the commit, other writers advanced `main`. A later readback observed `main` at `749ce17dd5db0d609622722cb78a9ffaf3413f06` while the target directory still resolved to the exact project tree `ffe327d71c94bc196e821ccf69f9618a5705bbf8`. This demonstrates the additive commit remained present through subsequent branch advancement.

## Protected-scope result
The commit diff contains only files under `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-SUPPLY-CHAIN-SENTINEL/`. No repository whose name contains `NEXY.AI` was mutated by this work.
