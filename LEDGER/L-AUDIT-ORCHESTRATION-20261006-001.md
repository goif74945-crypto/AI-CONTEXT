# LEDGER L-AUDIT-ORCHESTRATION-20261006-001
| ID | Source | Claim | Proof | Deps | Risk | Status | Confidence |
|---|---|---|---|---|---|---|---|
| L1 | product branch API | NEXY.ai audit snapshot head observed as 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43 | GitHub branch read | GitHub connector | head may later move | VERIFIED | 1.0 |
| L2 | local attached spec | canonical spec SHA-256 is b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 | sha256sum on attached DOCX | attachment bytes | none at observation | VERIFIED | 1.0 |
| L3 | AI-CONTEXT overview/matrix | current normalization is 837 rows, 773 current build rows, 52 deployment evidence, 8 excluded, 4 deferred | read from current source-normalization records | AI-CONTEXT main | context could later change | VERIFIED | 1.0 |
| L4 | AI-CONTEXT directive | only NEXY.ai is authorized product branch by latest explicit single-branch directive | commit 8d6a8f1719c78b18eacbe144458fd3dfb770a382 | user directive lineage | branch cleanup may still be pending | VERIFIED | 1.0 |
| L5 | persisted auditor directive | auditor command exists and was read back | commit 79b12f049aa8ec18fd25767193ae2d4f21c6290a + blob 2cb2e2b9b71ee7a26a5cfed86f37b51a918855a1 | AI-CONTEXT write permission | none observed | VERIFIED | 1.0 |
| L6 | task scope | no downstream builder command was created in this coordinator task | persisted directive only instructs auditor to generate it later | task scope | audit not yet executed | VERIFIED | 1.0 |
