# Future Concepts

**AUTHORITY LABEL: AI-PROPOSED CONCEPTS ONLY.**
These are not current NEXY.AI requirements, not implementation truth, and not authorization to modify NEXY.AI.

1. **Signed Provenance Adapter**: ingest Sigstore/SLSA attestations and bind artifact digests to builder identity and workflow provenance.
2. **Reproducible-Build Comparator**: build the same dependency artifact in two isolated builders and compare content digests before promotion.
3. **Transitive Reachability Gate**: combine dependency graph reachability with feature usage to distinguish installed-but-unreachable packages from executable paths.
4. **Registry Quorum Check**: compare metadata from multiple independently trusted registries/mirrors without letting any single registry become authority.
5. **Policy Epochs**: version policy bundles and require explicit migration evidence when changing allowed drift classes.
6. **Binary Artifact Fingerprinting**: extend snapshots beyond package metadata to native binaries, container layers, WASM modules and model weights.
7. **Dependency Blast-Radius Graph**: map a changed artifact to NEXY subsystems, tests and release gates that must be re-run.
8. **Air-Gapped Evidence Capsule**: export a self-contained signed evidence bundle for offline verification by NEXY::JUDGE or another independent verifier.

Each concept requires a separate task contract, threat model and evidence plan before implementation.
