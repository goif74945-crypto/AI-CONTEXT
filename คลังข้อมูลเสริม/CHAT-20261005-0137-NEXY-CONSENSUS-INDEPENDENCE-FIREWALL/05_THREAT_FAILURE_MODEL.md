# NCIF Threat, Failure and Privacy Model

**Classification:** EXPERIMENTAL / AI-PROPOSED

## Assets protected

- integrity of independence counting;
- visibility of common evidence roots;
- separation between consensus candidacy and truth authority;
- provenance confidentiality where raw source labels may be sensitive;
- deterministic/replayable evaluation.

## Threats and reference behavior

### T01 — Sybil vote inflation
Attacker creates many actors on one root.

**Control:** shared root/token collapses actors into one independence group.

### T02 — Evidence-ID cloning
Attacker copies one source into multiple evidence objects with different IDs.

**Control:** identical declared root `source_identity` creates the same digested source token.

**Residual risk:** if attacker lies and supplies different source identities, NCIF cannot authenticate truth by itself.

### T03 — Derived-evidence laundering
Attacker wraps one source through several derived nodes.

**Control:** root ancestry propagates through the full DAG.

### T04 — Bridge laundering
A-B share common cause X, B-C share Y, so naive pairwise counting may treat A/C as independent.

**Control:** DSU connected components collapse transitive correlation.

### T05 — Missing provenance
A derived node references absent parent.

**Control:** FREEZE; no orphan is promoted to a root.

### T06 — Cyclic provenance
Invalid/crafted graph creates lineage loop.

**Control:** topological processing detects unresolved nodes and FREEZEs.

### T07 — Evidence-free agreement
Actors assert support/opposition without evidence.

**Control:** material evidence-free stance FREEZEs.

### T08 — Correlated disagreement
Same source is interpreted as both SUPPORT and OPPOSE.

**Control:** shared-root cross-stance conflict FREEZEs rather than treating disagreement as independent diversity.

### T09 — Provenance metadata disclosure
Raw source identifiers or correlation labels leak through diagnostics.

**Control:** ordinary output emits domain-separated digests rather than raw source/key values.

**Residual risk:** hashes are not encryption. Low-entropy labels can be guessed; evidence/actor IDs remain visible.

### T10 — Deep-lineage stack exhaustion
Recursive traversal crashes on valid deep DAG.

**Control:** iterative Kahn traversal. Local stress exercises depth 5,000.

**Residual risk:** extremely large inputs can still exhaust CPU/memory; no production quota/streaming admission layer exists.

### T11 — Correlation-key poisoning / denial of consensus
A malicious upstream adds a shared key to collapse otherwise independent votes.

**Control in v1:** none beyond explicit output and deterministic replay. This is safer than granting false independence but can cause denial-of-consensus.

**Required future work:** authenticate provenance assertions and restrict who may assert correlation metadata.

### T12 — Omitted common cause
Caller omits a real shared dependency.

**Control in v1:** impossible to infer universally from absent information. NCIF must not claim hidden-correlation detection.

### T13 — SHA-256 collision
Digest token collision could theoretically merge unrelated metadata.

**Control:** standard cryptographic digest and domain separation; no claim of mathematical impossibility.

### T14 — Threshold manipulation
Policy is configured to `min_support_groups=1` or excessive opposition tolerance.

**Control:** values are explicit/validated, but v1 does not own policy authority. Future NEXY adoption must bind policy to governing law and audit changes.

## Failure states

- malformed contract → `ContractError` / CLI nonzero;
- unsafe interpretable provenance → `FREEZE` with reason;
- insufficient independent support → `FREEZE`;
- excessive independent opposition → `FREEZE`;
- candidate threshold satisfied → `CONSENSUS_CANDIDATE`, still `NOT_VERIFIED_FINAL_AUTHORITY`.

## Security boundary

NCIF evaluates declared provenance. It does not authenticate actors, signatures, source origin, provider identity, dataset lineage, or evidence correctness. A production version requires a trustworthy provenance issuer/verifier upstream.
