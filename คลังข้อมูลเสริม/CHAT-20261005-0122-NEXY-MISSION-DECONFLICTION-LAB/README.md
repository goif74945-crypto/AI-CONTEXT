# NEXY Concurrent Mission Deconfliction Lab

AI_PROPOSED_CONCEPT / ADVISORY ONLY.

NCMDE is a deterministic preflight gate for multi-agent or multi-chat engineering. Repository permissions stop some low-level corruption, but they do not stop two agents using distinct paths to build substantially the same subsystem, or agents claiming intersecting write trees, protected scopes, exclusive resources, or exclusive authorities.

Input: mission intent + active mission registry + explicit time + policy.
Output: exactly one of PROCEED, COEXIST, DECONFLICT, FREEZE.

Hard collisions always FREEZE. High declared semantic overlap yields DECONFLICT. Moderate overlap yields COEXIST. Low overlap yields PROCEED.

No embeddings are used as hidden authority. Missions explicitly declare domains, capabilities and deliverables. The cost is possible false negatives when metadata is poor; the benefit is reproducibility and inspectability.

The reference implementation has no third-party runtime dependency, injects time explicitly, requires bounded leases, structurally distinguishes FILE/TREE claims, canonicalizes set-like metadata, sorts registry entries, and SHA-256 seals the complete decision state.

DECONFLICT is a coordination requirement, not permission to merge/delete/cancel another mission.