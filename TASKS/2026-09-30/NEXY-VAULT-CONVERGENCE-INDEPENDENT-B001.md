# NEXY VAULT Convergence — Independent Batch 001

TASK_ID: NEXY-VAULT-CONVERGENCE-INDEPENDENT-B001-20260930
mode: SOLO-NONCONFLICT
scope: VAULT / Storage only; deliberately excluded DOC-B boundary, observability alarm wiring, Railway validation config
implementation_repo: goif74945-crypto/NEXY.AI-
branch: NEXY.ai
checkpoint_head: 0f9c8c65e2ab7b959f03264569430afc256f268a
checkpoint_tree: 7d035b597f905878d879abb779fe549762be3f24
source_doc: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
source_matrix: NEXY_IGNIS_FULL_SYSTEM_FEATURE_BUILD_MATRIX.xlsx

## Requirements addressed
- REQ-0378 revision_no increments monotonically per artifact
- REQ-0374 commit atomicity = DB transaction for metadata + pending blob verification

## Proven defects
1. packages/vault/versioning.ts used count()+1. Concurrent transactions could observe the same count and allocate the same revision number.
2. vault/repository.ts emitted BLOB_VERIFIED inside commitVault although commitVault did not call provider.verifyHash(). DOC-C explicitly requires pending blob verification at this stage.

## Changes
- 0c572828deb1c9ed3d5b55a005c91fd15def5366
  - per-artifact pg_advisory_xact_lock
  - allocate next revision from durable max(revisionNo)+1
- 8f4372b0be274c52c1f700fd86ae0171f923264e
  - added tests/contract/vault-revision-monotonic.test.ts
- c2e7576fe960dc77cea9464bfc4a194e2ee3e917
  - changed false BLOB_VERIFIED semantic claim to BLOB_VERIFICATION_PENDING
- 0f9c8c65e2ab7b959f03264569430afc256f268a
  - added tests/contract/vault-pending-blob-verification.test.ts

files_changed:
- packages/vault/versioning.ts
- tests/contract/vault-revision-monotonic.test.ts
- vault/repository.ts
- tests/contract/vault-pending-blob-verification.test.ts

validation:
- Static/source proof completed.
- Focused tests were committed but exact-head Railway execution is PENDING because shared validator variables/config are being controlled by another concurrent task; this batch intentionally did not modify shared Railway config to avoid collision.

status: PARTIAL
next:
- verify exact-head tests when shared validation lane is available
- continue REQ-0379 no overwrite / REQ-0380 new content = new revision
