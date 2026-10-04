# NCIF Final Main Persistence Proof

Classification: POST-TEST E0 / MERGE / READ-BACK EVIDENCE
Durable session code: `CHAT-20261005-0137-NEXY-CONSENSUS-INDEPENDENCE-FIREWALL`
Platform-native ChatGPT conversation ID: `UNKNOWN_NOT_EXPOSED_BY_AVAILABLE_TOOLS`

## Repository boundary

Authorized and actual write repository:
- `goif74945-crypto/AI-CONTEXT`

Protected mutation rule:
- repositories whose names contain `NEXY.AI` were not used as write targets in this mission.

## Merge evidence

- isolated branch: `chat-20261005-0137-ncif-lab`
- branch artifact/read-back receipt head: `de2296c2d3fc99c7a69d30a4d15e4872e2bc8138`
- pull request: `#48`
- merge method: normal GitHub merge, no force update/history rewrite
- merge result: `merged=true`
- merge commit: `bb13ef1ea9072fba63552e3b4651a9eada0d0ed0`

## Exact tested-artifact identity on main

After the merge, the 37-file pre-publication/tested artifact set was fetched from `main` and compared against the local Git blob SHA-1 identities that were calculated from the exact files subjected to local E1/E2 verification.

Read-back was split into two bounded batches:
- batch A: 18 checked, 0 mismatches, 0 missing
- batch B: 19 checked, 0 mismatches, 0 missing

Total:
- **37 / 37 exact blob identities matched**
- **0 missing**
- **0 mismatches**

The earlier branch-level persistence receipt is also present on `main` with Git blob SHA:
`73cba33ee3cfb721fe5bd68f2fc09f8e555d37a8`.

## Executed local verification bound to those exact 37 files

Recorded evidence:
- Python compile: PASS
- unit/adversarial tests: 28 / 28 PASS
- bounded deterministic audit: 6,561 cases / 0 assertion failures
- structural stress: 5,000-node deep lineage PASS
- structural stress: 5,000 votes across 500 roots, observed 500 groups, PASS
- CLI candidate path: PASS
- CLI correlated false-consensus FREEZE path: PASS
- JSON parse checks: PASS
- one-command verifier: 7 / 7 checks PASS

The exact local/remote identity check binds those local results to the published pre-publication artifact bytes. This post-test receipt itself is intentionally not part of the tested 37-file hash set.

## Final bounded status

**PASS** for the standalone NCIF supplemental-lab acceptance contract:
- design/code/tests/evidence exist;
- requested AI-CONTEXT persistence is proven;
- exact tested artifact bytes are on `main`;
- protected repository mutation was not required or performed.

**NOT_VERIFIED / OUT OF SCOPE**:
- NEXY.AI runtime integration;
- NEXY.AI deployment;
- production security/performance/SLO;
- authenticity of caller-declared provenance;
- detection of undeclared hidden common causes;
- policy adoption by NEXY authority.

NCIF remains **AI-PROPOSED / EXPERIMENTAL / NON-GOVERNING**.
