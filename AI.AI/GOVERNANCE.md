# Supplemental versioning notes for AI.AI

**AUTHORITY:** [CONSTITUTION.md](CONSTITUTION.md), [REGISTRY.md](REGISTRY.md) and [TEMPLATES/SUBMISSION.md](TEMPLATES/SUBMISSION.md) are canonical. This file is only a supplemental interpretation of the owner's version-specific request. In any conflict, follow CONSTITUTION.md.

- Scope: AI-CONTEXT/AI.AI/** on main only; never mutate PROJECTS/AI.AI or any NEXY.AI* repository.
- No existing file in any directory named `โค้ดโปรเจคปัจจุบัน` may be changed, and DO NOT create/update/move/delete contents there. Version archives and test candidates go into `AI.AI/versions/vX.Y.Z/` and `AI.AI/PROPOSALS/` instead.
- Every chat states the product version, pinned SHA, unique chat/proposal ID, reproducible criticism, one nonduplicate idea, complete real source code, tests (positive and negative), and integration patch.
- Versions do not advance merely because an idea was submitted. Use v0.4.0 until a separately evidenced product release occurs; create v0.5.0 ONLY after proof of that version.
- An existing version folder is append-only for distinct submissions; do not overwrite others' files.
- A version snapshot marked FULL must contain ALL source files, with checkable SHA manifests. A link or hash alone is not the source. Declare SNAPSHOT_INCOMPLETE if GitHub lacks actual full source bytes.
- Every proposal MUST match canonical REGISTRY and PROPOSALS scheme, use exact pinned source, apply integration.patch to a disposable COPY, and report command output. Merge to a product repository is not implied by a proposal.
- GitHub writes: first check main HEAD and all path collisions, then read back resulting blob and commit. On conflict or uncertainty: FREEZE the affected change; no force updates.
- Only exact evidence merits PASS. Tests on mocks are distinct from physical devices, and passing tests are not an accuracy percentage.
- Version archive file roles: VERSION.md contains provenance, critique pointers, verified code candidates, test evidence, source completeness and release blocker list.

**Status:** reference only; see canonical CONSTITUTION.md.
