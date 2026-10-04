# Publication Readback Evidence

Work code: CHAT-20261005-0228-NEXY-LO4-Q64-HCCF20
Target: goif74945-crypto/AI-CONTEXT main
Classification: AI_PROPOSED / EXPERIMENTAL / NON-CANON

## Publication result
- Final publication method: direct GitHub Contents API writes to the unique supplemental subtree.
- Reason: concurrent sessions changed main repeatedly, causing pull-request merge attempts to fail with GitHub 405 "Base branch was modified".
- Recovery: no force push, no history rewrite, no overwrite of adjacent paths. Each unique-path write resolved the then-current default branch head; isolated 409 conflicts were retried.
- Protected repository names containing NEXY.AI were not used as mutation targets.

## Readback gate
Git blob identity was compared between the locally tested artifacts and main after publication.

- Documentation/task/evidence control files: 10/10 exact blob identity PASS.
- Package/source/tests/raw evidence/hash manifest: 11/11 exact blob identity PASS.
- Total: 21/21 exact blob identity PASS.
- Mismatch: 0.

## Runtime evidence carried by the exact published artifacts
- Python unit + integration discovery: 32/32 PASS.
- Focused integration: 2/2 PASS.
- Static compileall: PASS.
- Deterministic property sweep: 33,735 checks PASS.
- Initial DRM one-ULP defect was repaired by integer-weight normalized means before final evidence.

## Scope status
Standalone HCCF20 lab: COMPLETE.
NEXY.AI integration: NOT_VERIFIED.
NEXY runtime/deployment: NOT_VERIFIED.
Canon promotion: NOT_PERFORMED.
Global uniqueness/superiority: NOT_VERIFIED.

08_FINAL_AUDIT.md intentionally remains the pre-publication artifact covered by the frozen SHA-256 manifest. This file records the subsequent publication/readback gate without invalidating that manifest.
