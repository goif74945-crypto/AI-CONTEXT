# Design — NEXY Independent Assurance Five-Pack

## Status and authority boundary

Everything in this document is an **AI-proposed supplemental concept**. It is not a claim about current NEXY implementation or governing law. Where a proposal conflicts with DOC-B/DOC-C or another higher authority, the proposal loses. The package is designed to integrate only through explicit contracts and must never obtain authority merely because it exists in AI-CONTEXT.

---

## 1. IAQ — Independence-Aware Quorum

### Problem
NEXY::SWARM can use multiple workers, but worker count is not evidence independence. Agents sharing the same provider/model family, source lineage or toolchain can fail together. Counting correlated replicas as separate votes can turn one failure mode into a fake quorum.

### Design
Each vote carries `provider`, `model_family`, `data_lineage`, `toolchain_fingerprint`, and a verdict. Pairwise correlation creates clusters. The quorum is then evaluated over clusters, not raw votes. Cluster resolution is conservative: any FAIL makes the cluster FAIL; all PASS makes PASS; mixed/unresolved evidence becomes FREEZE.

### Invariants
- duplicate agent identity is invalid;
- provider, model-family, data-lineage and toolchain correlation metadata must be complete and nonblank; unknown metadata cannot be counted as independent evidence;
- correlated replicas cannot increase independent-cluster count;
- an independent FAIL cannot be hidden by a large correlated PASS population under the default policy;
- vote ordering does not change the result;
- no votes or insufficient independent support freezes.

### NEXY fit
IAQ preserves the existing split `SWARM = labor` and `CORE/JUDGE = authority`, and concretizes the no-single-point-trust principle. It does not grant worker agents final authority.

### Non-goals
It does not claim NEXY currently records the required correlation metadata, nor that the simple Jaccard rule is a calibrated production estimator.

---

## 2. ECG — Evidence Contamination Guard

### Problem
Verification can be circular even when it uses a separate process. Examples: expected output derived from the candidate itself, target and oracle generated from the same untrusted root, or cyclic lineage that makes provenance undecidable.

### Design
Represent derivation as directed `child -> parent` edges. A claim defines target artifacts, oracle artifacts and explicitly trusted roots. The analyzer detects direct overlap, oracle ancestry that includes the target, shared untrusted roots and cycles.

### Invariants
- direct target/oracle identity is contaminated;
- an oracle derived from a target is contaminated;
- shared lineage counts only when the shared root is explicitly trusted;
- lineage cycles are INDETERMINATE, never CLEAN;
- edge ordering does not affect the result.

### NEXY fit
ECG strengthens evidence-before-release, provenance and JUDGE verification. It complements, rather than replaces, E0–E7 evidence classes. Evidence can have the right class and still be contaminated.

---

## 3. RAAS — Risk-Adaptive Assurance Scheduler

### Problem
Maximum assurance on every action wastes resources; minimum assurance on consequential actions is unsafe. The missing bridge is an explicit, testable mapping from action risk to required proof and control gates.

### Inputs
Integer 0–5 dimensions: impact, irreversibility, externality and sensitivity; plus production, permission-change and compensation-availability flags.

### Outputs
Required evidence class E1–E6, explicit confirmation requirement, rollback/compensation requirement, independent-quorum requirement, negative-path test requirement, and an ALLOW_WITH_ASSURANCE or FREEZE disposition.

### Safety rules
- high-impact + highly irreversible + no compensation path freezes by default;
- high-impact production actions are promoted to E6;
- permission changes require confirmation, independent quorum and negative-path tests;
- the mapping is deterministic for equal inputs.

### NEXY fit
RAAS is a candidate implementation detail beneath RSEL/RUN/JUDGE. It may only tighten/rout requirements under approved policy. It cannot weaken DOC-C release gates.

### Non-goal
The score is an engineering routing heuristic, not a universal probability or scientific risk equation.

---

## 4. CTR — Capability Tombstone Registry

### Problem
Append-only registries preserve old capabilities by design. That is historically correct, but stale runtime snapshots can accidentally re-offer a capability that authoritative governance has retired. Positive presence alone is therefore insufficient for admission.

### Design
Maintain append-only RETIRE/RESTORE events with strictly increasing per-capability epochs. Active retirement blocks admission regardless of the candidate's claimed snapshot epoch. Restore is explicit and newer; snapshots older than the restore epoch remain blocked. Canonical digest sorts unrelated event streams for deterministic identity.

### Invariants
- retirement never deletes history;
- a future-looking/stale snapshot cannot bypass active retirement;
- restore requires a prior active retirement and a newer epoch;
- self-replacement is invalid;
- canonical digest is deterministic and independent of unrelated insertion order.

### NEXY fit
NEXY future capability governance already defines governed sunset and retained history. CTR is not replacement governance. It is a proposed admission-side enforcement cache derived from already-authoritative retirement/sunset events. It may not invent a tombstone.

---

## 5. AIG — Attention Integrity Governor

### Problem
PULSE/VIEW must reveal real state and freeze conditions, but repeated identical alerts can create operator fatigue. Simple rate limiting is unsafe because it can hide a new critical state.

### Design
Each alert contains a semantic key, severity, evidence fingerprint, state fingerprint and monotonic timestamp. Exact duplicates inside a dedup window can be suppressed. Repeated noncritical noise can be coalesced under an attention budget. A materially changed CRITICAL state is always delivered.

### Invariants
- changed CRITICAL state is never hidden by dedup or noncritical budget;
- escalation from any noncritical severity to CRITICAL is material and is never hidden by dedup, even when the state and evidence fingerprints are unchanged;
- exact CRITICAL duplicates may be suppressed to prevent duplicate storms;
- evidence change is material even when the state fingerprint is unchanged;
- alert time cannot regress;
- the governor never fabricates success, alters Core state, or converts FREEZE into a non-freeze state.

### NEXY fit
AIG belongs only in PULSE/VIEW presentation/attention policy. CORE/JUDGE truth remains authoritative.

---

## Cross-system reference flow

A high-risk production action can be routed through RAAS, require IAQ-independent quorum, require ECG-clean evidence, reject execution through CTR if its capability is retired, and surface the final state through AIG. The reference test proves those modules can compose locally. It does **not** prove NEXY integration.

## Security and failure model

The five mechanisms follow fail-closed behavior for material ambiguity. Metadata supplied to them is treated as asserted input, not magically trustworthy data. A production integration must authenticate provenance, bind records to exact versions/commits, protect configuration authority, and persist audit evidence under NEXY's governing contracts.

## Promotion requirements

Before any mechanism becomes current NEXY behavior, at minimum: resolve exact implementation interfaces and HEAD; map every proposal to current DOC-C requirements; threat-model metadata spoofing and bypass paths; replace heuristics with governed policy/config where required; add contract/integration/E2E tests; collect runtime/deployment evidence at the class required by the claim; and explicitly promote the feature through project authority. Until then: **PROPOSED / NOT NEXY-RUNTIME-VERIFIED**.
