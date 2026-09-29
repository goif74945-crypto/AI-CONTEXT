# FAILURE — VAULT false verification semantic claim

FAILURE_ID: NEXY-VAULT-FALSE-BLOB-VERIFIED-20260930
requirement: REQ-0374
source_rule: commit atomicity = DB transaction for metadata + pending blob verification
defect: commitVault emitted BLOB_VERIFIED without provider.verifyHash() on that path
risk: false evidence / semantic integrity failure
fix_commit: c2e7576fe960dc77cea9464bfc4a194e2ee3e917
test_commit: 0f9c8c65e2ab7b959f03264569430afc256f268a
recovery: event is now BLOB_VERIFICATION_PENDING; physical verification remains in provider-backed storage-control/cold-snapshot paths
status: FIXED_SOURCE_PENDING_RUNTIME_VALIDATION
