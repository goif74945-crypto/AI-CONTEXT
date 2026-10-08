# FAILURES 20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS
Product HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Control precommit HEAD: fdb9ebf97ac7e993bdcf656c87c268ee7ab71ed2
Task ID: 20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS
Canonical DOCX SHA256 matched in this conversation: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE: NEXY.ai packages/queue/dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29; local patched blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af.

(1) Expected RED regression: 5 fails of 9 at original HEAD with live production exported code, mocked Prisma/BullMQ. RED exit=1 is desired defect reproduction; post-patch 9/9 exit=0.
(2) Initial TypeScript backend check exit=2 because Prisma Client was not generated in fresh npm install; corrected by locally running prisma generate exit=0, repeated full backend typecheck exit=0. Do not count first environment setup failure as permanent implementation failure.
(3) No Docker, PostgreSQL cli or Redis server on connected Windows host; REAL_POSTGRES_REDIS_TESTS=NOT_RUN. No product commit authorized by current test depth.
(4) E7 current-head GitHub Actions job pre-step failure and logs 404 BlobNotFound; INFRA_ROOT_CAUSE_UNKNOWN.
(5) Linux bwrap/seccomp/cgroup security runtime NOT_RUN (only Windows runner connected).
(6) TSA time-signature binding not established; freeze only TSA change.
(7) DOC-E human signoffs/application rollback/monitoring not evidenced.
