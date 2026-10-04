# Limitations and Formal Promotion Path

## Known limitations
1. The exact authoritative DOCX body was not directly decoded/read from Drive in this session; exact source identity/hash is corroborated through the current NEXY repository and source snapshots. This is material for an EPC vote and therefore KEEP/CUT remain unused.
2. The package is a standalone reference implementation, not wired into NEXY runtime.
3. External thresholds are intentionally not claimed as Canon. Test thresholds are fixtures only.
4. TypeScript bigint gives deterministic exact integer arithmetic, but the package is not a drop-in replacement for NEXY Rust `Fixed128`; promotion should map/test semantics explicitly at the boundary.
5. Novelty was checked against inspected current neighboring EPC artifacts. Concurrent/future work can change overlap.

## Required path before promotion consideration
1. Re-read exact authoritative spec bytes/text with a working source path and bind to the recorded hash.
2. Refresh NEXY and AI-CONTEXT HEADs; re-run semantic overlap analysis.
3. Map each proposed mechanism to explicit canonical requirement or approved extension authority.
4. Decide which mechanisms, if any, belong in NEXY versus remaining external tooling.
5. Implement a version-pinned adapter against actual NEXY contracts in an authorized integration branch/workspace.
6. Run contract/integration/replay/security/regression tests at the exact candidate commit.
7. Generate a promotion dossier for existing JUDGE/LAW authority.
8. Only then consider an EPC KEEP receipt; a KEEP receipt itself still cannot promote anything.
