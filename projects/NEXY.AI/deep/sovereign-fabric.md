# NEXY.AI — Sovereign Fabric / Universe / Recovery Deep Context

## Status
SOURCE-DESIGN / NOT VERIFIED RUNTIME. This file records architecture found in the full design source; it does not claim that these mechanisms are implemented or in current DOC-C scope.

## 1. System characterization
A consolidated source section characterizes the large-form NEXY architecture as an **Executable Constitutional State Machine** with a bias of **Integrity > Availability**. It distinguishes a local execution fabric from a global authority/anchor fabric. The four named layers in that consolidation are:
1. Kernel — authority, Vault, Canon, recovery.
2. Universe Runtime — isolated execution boundary.
3. Builder Engine — deterministic app fabrication.
4. Global Anchor Kernel — authority, canon and signature root.

The stated model is hybrid: local execution may continue under constrained conditions while global mutation/authority is gated by anchor/quorum rules.

## 2. Authority / region quorum
SOURCE-DESIGN:
- Region anchors: 5.
- Fixed override threshold: 3/5.
- No adaptive quorum or dynamic weights.
- Valid override requires enough region signatures, matching Canon hash and valid time window; emergency paths additionally depend on CompromiseFlag semantics.

This is an authority mechanism, not an AI voting mechanism.

## 3. Time authority
SOURCE-DESIGN:
- Primary time authority: TSA.
- Witness: chain timestamp.
- TSA set size: 3, with 2-of-3 valid signatures required.
- A degraded-time window of 24 hours appears in locked source material; after the bound, anchor mutation freezes.
- TSA/chain divergence beyond a fixed delta creates an anomaly state.
- Normal TSA rotation is described with a fixed rotation window; emergency replacement is bound to emergency governance.

## 4. Anchor publication FSM
The source defines an explicit publication chain:

`PROPOSED → QUORUM_SIGNED → MERKLE_UPDATED → CHAIN_ANCHORED → IPFS_PINNED → MIRROR_REPLICATED → FINALIZED`

Only `FINALIZED` is valid. Partial publication is invalid. Empty intervals still produce an anchored empty batch/root under the design. Reorg handling is described as a deterministic re-anchor event after a fixed confirmation rule.

## 5. Detection model
Two classes are described:
- Immutable Core Detection: detects signature failure, Merkle divergence, hash discontinuity, invalid TSA/quorum and key-reuse anomalies; source says this layer cannot be disabled/versioned.
- Extendable Detection Modules: versioned/approved/anchored additions that cannot suppress the core detector or change core thresholds. The design explicitly prefers binary logic over ML/probabilistic scoring in this authority path.

## 6. Universe isolation planes
Several source sections converge on three major execution planes:
- **CORE PLANE / CORE ZONE** — constitutional/deterministic protected authority.
- **UNIVERSE PLANE / USER UNIVERSE ZONE** — isolated per-app/per-user runtime.
- **QUARANTINE PLANE / SUSPECT state** — containment for an offending universe without freezing unrelated universes.

The isolation stack is described as layered, with combinations of:
- KVM / Firecracker microVM
- container runtime such as runc/Kata
- gVisor syscall interception
- optional WASM sandbox

Design intent: no shared mutable memory with Core, no parent FS mount, no privileged container spawn, no self-escalation of resource profiles, no post-seal spec mutation, and no authority override.

## 7. Quarantine / local containment
The source describes machine-checkable triggers such as memory abuse, sandbox escape attempts and related invariant violations. Offending universes can be frozen/killed locally while Core and unrelated universes continue. Whole-ecosystem freeze is reserved for higher-order integrity failures.

A two-hour quarantine protocol appears in an earlier design section and explicitly tries to avoid trusting raw system clock time; state/log hashes and sealed snapshots are used as recovery evidence. Treat the exact timing protocol as SOURCE-DESIGN rather than proven implementation.

## 8. Host Survival Protocol (HSP)
The host-protection architecture monitors host pressure outside the user runtime. It includes warning/critical zones, cgroup/memory-pressure observation, freezing/ejecting the offending universe, detaching runtime resources and prioritizing survival of Core/Vault/Guardian over the app instance.

Named architecture:
- Host Execution Layer
- Core Vault + Canon Engine
- Universe Runtime
- Host Sentinel / Guardian Daemon

The Guardian must sit outside the Universe runtime.

## 9. Deterministic Resurrection / recovery
The design includes a resurrection protocol built around sealed state rather than ad-hoc restart. Named recovery evidence includes:
- `universe_id`
- `last_state_hash`
- `build_hash`
- sealed snapshot identity

Recovery checks include host cleanliness, snapshot/state-hash match and build-hash match. Mismatch leads to freeze rather than forced recovery. Replay must resume through legal states with no jump-state behavior. Repeated resurrection failure leads to a frozen/manual-recovery state.

## 10. HSR-A / auto-recovery controller
A later section combines Host Survival + Auto-Recovery:
- Guardian detects failure.
- Universe is frozen/state-locked.
- Runtime memory/resources are released.
- A recovery marker is written.
- Restart occurs in `SAFE_RUNTIME` after checks/cooldown.
- Repeated failure or memory-leak patterns lead to lock/freeze and manual intervention.

Design rule: app failure must not corrupt Vault/Core state.

## 11. Memory governance at host level
The source describes hard resource partitioning such that a Universe receives a bounded pool and cannot consume reserved Core/host memory. Mechanisms named include cgroup hard limits, OOM priority and a memory sentinel daemon. Exact numeric examples are design examples, not portable canonical defaults unless repeated in a later locked spec.

## 12. Builder Engine
Canonical source flow:

`User Intent → AppSpec → Canonical JSON → SHA-256 SpecHash → Build → Seal → Deploy`

The `SpecHash` is stored in the Kernel/Vault; runtime must match it. Drift is a freeze condition. AppSpec contains identity, runtime, resources, permissions, storage and public-mode declarations.

## 13. Reproducible build envelope
The source requires rebuild equivalence to the artifact hash and locks compiler/container/environment inputs. Named controls include:
- pinned compiler/toolchain
- container digest
- UTC locale/timezone normalization
- deterministic flags
- path normalization
- `build_env_hash`
- reproducible tooling such as Nix/Guix

Later implementation-verification law strengthens this into seal → verify signature → verify build hash → deploy, with rebuild-from-source as supply-chain defense.

## 14. Cross-Universe permission model
Permission grants are explicit bilateral records with source app, destination app, scope, rate limit, expiry and signatures. Revocation is designed as immediate in later locked Creator-Fabric law. No implicit cross-universe privilege is allowed.

## 15. Creator Fabric inside Universe architecture
The source introduces a `CREATOR_APP` universe type distinct from SYSTEM/SOVEREIGN_APP. Creator apps may build web apps, game engines, AI workflows and nested builders, but cannot mutate constitutional authority.

Creator AppSpec expands capability declarations for network scope, storage scope, SDK modules, cross-app links, economy/monetization and public mode. Any undeclared capability use is a hard-failure/kill condition in the design.

Public deployment FSM:
`CREATED → BUILT → SEALED → VALIDATED → ANCHOR_QUEUED → FINALIZED → PUBLIC_ACTIVE`

Rule: not FINALIZED = not public.

## 16. Resource-survival law for creator apps
Soft threshold breach → graceful shutdown path. Hard threshold breach → kill. Kernel survives; app dies; no automatic global freeze solely for app overload. Security breach is treated more aggressively than ordinary overload.

## 17. Creator economy containment
Creator apps may use the Constitutional Settlement Unit through bounded APIs but cannot mint constitutional value or mutate the constitutional formula. Revenue-split rules are bound to `spec_hash`. Economic exploit response is scoped to affected account/app where possible instead of global corruption.

## 18. Recursive sandbox depth
A later source section locks recursive app creation to a finite tier graph:
- Tier 0 Kernel
- Tier 1 Sovereign App
- Tier 2 Creator
- Tier 3 Sandbox
- Tier 4 Nested Sandbox
- Tier 5 Final Depth
- Tier 6 impossible / undefined → freeze

The limit is enforced at build time. Purpose: bound permission evaluation, forensic reconstruction, resource cascade, kill cascade and economic propagation.

## 19. Scope boundary
Important: the full document contains both future constitutional/universe design and a narrower vNEXT/DOC-C build specification. Presence in this file does **not** mean current DOC-C authorizes Universe, blockchain/anchor, quantum-safe or public creator features. Always resolve build authorization against the current authoritative build spec.
