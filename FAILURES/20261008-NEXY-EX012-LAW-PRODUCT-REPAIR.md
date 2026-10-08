# FAILURE 20261008-NEXY-EX012-LAW-PRODUCT-REPAIR
STATUS: UNRESOLVED_BROAD_SUITE_AND_RELEASE_BLOCKERS
BROAD_RUN: Windows isolated checkout Vitest tests/contract tests/coverage JSON 905/911 pass; 6 failures:
1 core-kernel-no-authoritative-rng.test.ts: cargo ENOENT
2 core-kernel-rust.test.ts: cargo ENOENT
3-4 core-kernel-tier-depth-compile.test.ts: failed Tier5 expected null vs 0 and Tier6 stderr undefined
5-6 current-head-attestation.test.ts: tests expected exit0 received exit1
ROOT_CAUSES: Cargo binary absent for two; remaining four need independent environment/test setup diagnosis, NOT attributed to LAW patch without proof.
SETUP_RECOVERY: npm ci --ignore-scripts initially left Prisma client ungenerated; initial 2 suite import failures; solved with real Prisma generate exit0 and repeat GREEN 58/58.
CI_NEW_HEAD: Four workflows conclusion=failure on 90fac4835788e867559858fc92d093ded3dcb1eb; exact-head evidence run 37811868233 steps=[] runner empty, cause UNKNOWN.
G3: real Postgres Redis tests NOT_RUN; Cage/worker not verified; DOC-E release NOT_AUTHORIZED.
NEXT_SAFE_ACTIONS: investigate cargo/compilation runner, current-head fixture failures with minimal tests; operate safe isolated G3 only with authorized local services. Do not drop tests, fabricate pass or deploy.
