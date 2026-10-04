# Remote Read-back Evidence

Status: **PASS**

Work code: `CHAT-20261005-0228-NEXY-LO4-DETERMINISTIC-OPTIMIZATION-FOUNDRY`

## Release identity
- Release commit: `fb6a029d2cf011c42022c5a0a343d5541988633e`
- Parent at release commit: `4fabcef33336a459545ef933de029bfc2f6fc26e`
- Release tree: `9ebc832e2179bf8ff9c95c0a54c5394c94d176fd`
- Release archive SHA-256: `65f4c271de2e75e93121f8bc71ae0b8728cb55d944f466f64cfef46c0d8a0cfc`
- Release archive byte size: `34206`

## Exact remote part identity
The committed tree was read back recursively. Every release-part path resolved to the exact Git blob SHA created from the locally tested archive bytes.

| Part | Bytes | SHA-256 | Git blob SHA | Result |
|---|---:|---|---|---|
| part-00 | 8000 | `6fe8dc2b2e5b952f78c0805a2fc356c5e6851d55676d8e32167a9374533b8ed4` | `781f78587fcdc02802ba76caab9f5587d5eae0c1` | PASS |
| part-01 | 8000 | `057975056545c91118d3abe34773de744a7eaddb029397c6cb898a70ec965466` | `500bef87a3747ed1451f9bb584e406d718cff7e9` | PASS |
| part-02 | 8000 | `0a91fc4a6fea5a8502d5592e64e2c0b78f3f70c2341d773206b784605f1c0e4c` | `55ec5fe6ca2e17c23e8a5800eff16aa28bf9a40f` | PASS |
| part-03 | 8000 | `d6c01283ddf5c0d39b97078a6765201f5dc308d989dcbaa1cd62117c7377422e` | `931e50c0cb6c3e2d52e54cf597f5287657d36b69` | PASS |
| part-04 | 2206 | `550f45eb6de16a6c803185ad553d5b15453b11bec64e3553447f494132cc8ef8` | `471726636bd88cfe95fe8413cafcfab9731ff27a` | PASS |

## Mutation-scope proof
Commit comparison `4fabcef33336a459545ef933de029bfc2f6fc26e..fb6a029d2cf011c42022c5a0a343d5541988633e` reported:
- status: ahead
- ahead_by: 1
- behind_by: 0
- total_commits: 1
- changed paths: 7
- every changed path begins with:
  `คลังข้อมูลเสริม/CHAT-20261005-0228-NEXY-LO4-DETERMINISTIC-OPTIMIZATION-FOUNDRY/`

The release commit therefore did not contain a mutation outside the authorized work namespace.

## What this proves
E0/persistence identity for the release bundle and readable final index/state metadata at the stated commit.

## What this does not prove
It does **not** prove:
- adoption by NEXY Canon;
- compatibility against a current NEXY implementation revision;
- NEXY runtime behavior;
- deployment behavior;
- production security or performance;
- physical-system safety.

Those remain separate evidence obligations.
