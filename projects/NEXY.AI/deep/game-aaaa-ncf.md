# NEXY.AI — Deterministic AAAA Game Fabric + NCF Deep Context

## Status
SOURCE-DESIGN / FUTURE-FABRIC unless current build spec explicitly promotes it. NOT VERIFIED RUNTIME. This architecture is intentionally separated from the narrower DOC-C/vNEXT build.

## 1. Fundamental split
The game architecture exists specifically because modern games contain nondeterministic timing, GPU behavior, floating-point physics, networking, asset streaming and large-scale concurrency that would violate the constitutional Core.

Canonical split in source:

`Kernel (deterministic constitutional Core) → Universe Runtime (isolated boundary) → Game Engine Fabric (AAAA sandbox)`

Game Fabric may not directly access Vault, Canon, Anchor, authority or cross-universe resources without explicit grants.

## 2. G1 — Game Fabric Architecture
Runtime types considered:
- WASM game runtime;
- WebGPU/WebGL rendering;
- native containerized runtime;
- hybrid runtime.

Preferred architecture in source: **Hybrid**.
- authoritative logic: deterministic/WASM-oriented;
- rendering: GPU/nondeterministic sandbox;
- sovereign/economic state: deterministic ledger-bound.

## 3. G2 — Game State Law
Two classes:
### Gameplay / volatile state
May include physics, animation and frame timing. Nondeterminism is tolerated when it cannot mutate sovereign truth.

### Sovereign state
Includes asset ownership, economy, match result, rankings, rewards and publish rights. This state must remain deterministic and hash/replay controlled.

Key design principle:
**render/gameplay chaos may exist; sovereign/economic chaos may not.**

## 4. G3 — GameSpec binding
Every deployed game declares a bounded GameSpec including:
- engine version;
- physics model;
- RNG model;
- network-sync model;
- tick rate/resource profile;
- public mode.

GameSpec contributes to SpecHash. Runtime drift from GameSpec is a freeze condition.
No hot patch / live code injection; game update means a new spec hash.

## 5. G4 — Map / Creator System
Creator sandbox may build:
- maps;
- logic modules;
- mini-games;
- nested creator content.

But it cannot mutate:
- base engine authority;
- sovereign economy;
- anchor;
- permission system.

Recursive depth and resource envelopes inherit the general Universe/Creator laws.

## 6. G5 — AAAA Performance Model
The architecture anticipates:
- streaming assets;
- large world partition;
- matchmaking;
- AI NPCs/crowds;
- real-time sync.

Separation:
- GPU/render may be nondeterministic;
- authoritative CPU/simulation path is isolated;
- economic ledger commit is post-match / bounded, not arbitrary per-frame mutation.

## 7. G6 — Anti-Cheat Law
Core does not attempt to police every gameplay cheat. Core authority focuses on:
- ledger tampering;
- spec tampering;
- cross-universe injection;
- permission abuse.

Ordinary game-level cheat detection belongs to the game sandbox unless it crosses sovereign boundaries.

## 8. G7 — Game Economy Binding
Possible game economic objects include skins/items/map revenue/tournament rewards/asset trades.

Rules:
- constitutional settlement uses CSU;
- app-local currency may exist;
- conversion to CSU uses deterministic declared formula;
- no constitutional inflation/reversal/retroactive rewrite in the locked source branch.

## 9. G8 — Public Deployment
Public game deployment includes DNS/SSL/rate/DDoS/resource-quota concerns.
Overload is contained to the game/app: graceful shutdown → kill. It must not propagate into Kernel failure.

## 10. G9 — Update Law
Game update = new `spec_hash`.
No hot patch.
No live code injection.
Source design uses freeze → rebuild → redeploy semantics.

## 11. G10 — Hard Limits
Even AAAA workloads remain bounded:
- recursion depth ≤ locked universe maximum;
- universe tier bounded;
- no dynamic engine replacement;
- no adaptive governance inside game;
- no implicit authority escalation.

## 12. Drift vs Fork
A major source section formally distinguishes:
### Drift = corruption
Examples:
- policy/runtime/authority changes without version boundary;
- replay producing different state;
- config drift;
- silent operator patch;
- hidden maintenance mode;
- retroactive economic rewrite;
- floating-point entropy leaking into Core;
- recursive authority escalation.

### Fork = evolution
Explicit, versioned, hash-visible, replayable, auditable divergence from a declared snapshot/Canon boundary.
The design concept is a **finite deterministic state machine with explicit branching evolution**.

## 13. G11 — Multiplayer Deterministic Consensus
Preferred model: **region-sharded deterministic clusters**.

Topology:
`Global Fabric → Region Cluster → Shard → Client Render Shell`

Per-shard:
- fixed tick;
- deterministic WASM simulation;
- fixed-point math;
- event-driven processing;
- authoritative state hash per tick.

Outputs include tick/shard hashes.

Region root:
`region_root_hash = Merkle(shard_hashes)`

No probabilistic leader election / entropy-driven authority selection.

Client:
- never authoritative;
- sends input events;
- receives authoritative deltas;
- render may diverge;
- authoritative correction overwrites client state.

State mismatch → freeze shard + deterministic replay; no silent reconciliation.

## 14. Hybrid compute split
Large game architecture separates:
1. Constitutional Core;
2. sovereign game ledger;
3. deterministic simulation layer;
4. nondeterministic render/GPU layer;
5. cloud-assist layer for heavy compute only.

Cloud-assisted output must be reduced to canonical input events and hash-bound before it affects authoritative simulation. Cloud systems never write sovereign state directly.

## 15. G12 — Cross-Shard State Transfer
No live shared state between shards.

Primitive:
`EXPORT → COMMIT → IMPORT`

### Export
At deterministic boundary:
- freeze entity tick;
- produce entity snapshot/hash;
- append to shard WAL;
- include in shard Merkle;
- commit region root;
- only finalized root permits movement.

### Transfer record
Includes entity id, origin/destination shard, tick, snapshot hash, region root and quorum signature.

### Import
Destination validates root/signature/snapshot, maps deterministically into local coordinates/ids, appends local WAL and recomputes shard hash. Mismatch freezes destination shard.

### Duplication protection
Origin marks entity TRANSFER_PENDING until import is confirmed. Failed import is rolled back through deterministic replay; no dual residency.

### Tick alignment
Transfer only at fixed transfer windows / tick boundaries. No mid-tick migration.

### Economic coupling
Value-bearing entities include economic-state hash; ledger state must commit before export.

## 16. G14 — Deterministic AAA Toolchain
### Mesh
Lexicographic vertex order, normalized indices, deterministic duplicate collapse/tangent computation, canonical fixed/rational precision, mesh hash.

### Physics bake
Deterministic convex hull/contact ordering/broadphase; fixed seed; physics blob hash.

### NavMesh
Canonical node ids/edge order/grid partition; no random tie-break; nav hash.

### Shader
Canonical formatting/macro expansion, no timestamps, pinned compiler, digest bytecode, cross-compiler verification.

### Texture
Pinned compression settings, deterministic mip generation, explicit color space, no driver-only compression; texture hash.

### ToolchainHash
Includes compiler/build flags/container/OS/locale/UTC/target triple.

Parallel build is acceptable only when output hashes are identical.

### Cross-architecture
Assets baked on x86_64/aarch64 must match hashes or freeze/reject.

GameSpec includes asset Merkle root + toolchain hash + engine/physics/RNG model.

## 17. G15 — Authoritative Simulation Numeric Law
Game authoritative simulation is stricter than ordinary render:
- no float/double/half/SIMD-FP/FMA in authoritative layer;
- signed fixed-point model, source specifies Q64.64;
- integer-grid broadphase;
- deterministic SAT/GJK/canonical collision ordering;
- fixed-iteration constraint solver;
- deterministic sequential accumulation;
- integer SIMD only under fixed ordering;
- deterministic priority queues for AI;
- deterministic counter-based RNG permitted for game simulation when its algorithm/seed is part of GameSpec;
- LOD changes render only, not authoritative physics mesh;
- no epsilon comparisons.

Important domain distinction:
- Core Layer 9 states integer overflow → FREEZE.
- G15 source separately selects **deterministic saturating/clamped arithmetic** for game-authoritative overflow.
Do not merge these laws; they apply to different domains unless a later Canon unifies them.

G15 also calls for dual-compiler/cross-architecture state-hash equality.

## 18. G16 — World Topology Determinism
- fixed integer spatial grid;
- immutable chunk size per GameSpec;
- deterministic activation/deactivation radius;
- lexicographic chunk load order;
- chunk changes at tick boundary only;
- entity activity tied to active chunk;
- one-tick physics freeze on newly active chunks;
- LOD affects render only;
- simulation visibility uses deterministic adjacency/grid;
- assets loaded by canonical hash/order;
- cross-shard streaming only on boundary ticks;
- background I/O threads enqueue events but never mutate world state directly.

World hash:
`WorldHash = Merkle(active_chunk_hashes)`
with chunk hash built from sorted entity state.

Replay must activate identical chunks/entity sets per tick.

## 19. G17 — AI & Crowd Determinism
Authoritative game AI is a **Deterministic Agent Graph Machine**:
- integer perception grid;
- deterministic cell scan;
- perceived entities sorted by id;
- canonical path graph traversal;
- Q64.64 path costs;
- agent update ordered by agent_id;
- no parallel authoritative agent updates;
- behavior trees traverse canonically;
- deterministic goal comparator;
- influence map updates in fixed cell/agent order;
- fixed-iteration crowd collision solver;
- no same-tick recursive re-evaluation;
- deterministic priority queues;
- AI internal state contributes to shard hash;
- spawn/despawn only at tick boundaries;
- fixed per-tick budget, whole-agent deferral when over budget;
- cross-shard AI transfer includes full deterministic state.

Same world + same inputs must yield same perception/path/crowd/shard state across regions/architectures/replay.

## 20. G18 — Deterministic Networking
Networking is modeled as an **ordered input conveyor**, not authority/state truth.

Core rules:
- authoritative server relay only;
- clients never authoritative/P2P state authority;
- canonical binary packet schema;
- fixed endianness/length/hash;
- tick-indexed input;
- monotonic input sequence;
- fixed input delay buffer;
- late/invalid input handled by explicit deterministic rule;
- state broadcast indexed by tick/world hash;
- client prediction allowed only as non-authoritative display optimization;
- canonical server tick is the authoritative time;
- rate/protocol versions locked in GameSpec;
- protocol mismatch rejects rather than silently negotiates;
- deterministic timeout/inactivity handling;
- packet loss becomes defined no-op/fallback semantics rather than uncontrolled rollback.

Same ordered input stream → identical tick/shard hash.

## 21. G19 — Hardware & Microcode Verification
Goal is not “perfect hardware,” but detectable hardware/firmware drift.

Design includes:
- CPU model whitelist in Canon;
- microcode hash in node boot hash;
- exact/pinned kernel version;
- FP/FMA protections even though authoritative FP is already banned;
- dual-compiler verification;
- cross-architecture canonical replay/state-hash test;
- ECC required for region/shard authority; non-ECC sandbox-only;
- TPM/HSM remote boot attestation;
- storage firmware hash;
- dirty-shutdown recovery path;
- invariant TSC/tick counter, not wall clock;
- periodic cross-replica state-hash comparison for bit-flip detection;
- divergence → isolate/replay/permanent quarantine if persistent;
- hardware replacement → full rebuild + re-attestation + snapshot rejoin, no hot swap.

Final design bias remains Integrity > Availability, including silicon-layer drift.

# NEXY Creative Fabric (NCF)

## 22. Identity
NCF is not merely a builder. It is a **Deterministic Creation Orchestration Layer** producing Universe-bound artifacts.

Topology:
`Kernel → Universe Runtime → NCF → Artifact Instances`

NCF has no constitutional authority and cannot directly rewrite ledger/cross-universe truth.

## 23. Creation scope
NCF is designed to produce:
- web apps;
- 2D/3D games;
- 2D/3D assets/models;
- documents;
- AI-driven tools.

Highest rule:
**Creation may be nondeterministic; deployment must be deterministic.**

Everything deployable passes:
`Spec → Hash → Seal → Deploy`

## 24. ArtifactSpec
Every artifact becomes an explicit spec with:
- artifact identity/owner/type/version;
- runtime/engine profile;
- asset root hash;
- code root hash;
- dependency-lock hash;
- resource profile;
- permissions.

No spec = no execution authority.

## 25. Game authoring/canonicalization/seal
Three stages:
1. Non-deterministic authoring: AI may generate scenes/physics/shaders/scripts/behavior trees.
2. Canonicalization: convert to Canonical Intermediate Representation (CIR), canonical mesh/texture/fixed physics/deterministic AI graph/shader digest.
3. Seal/bind: Merkle artifact root + SpecHash + signed UniverseSeal.

After seal, artifact is immutable. Modification means rebuild/new hash.

## 26. Web/document/assets
### Web app
Must declare framework, runtime mode, APIs, resource/network envelope. Dynamic floating dependency resolution is forbidden; dependency hashes are locked.

### 2D/3D assets
Canonical vertex/index/transform/compression/texture hashing before deploy.

### Documents
Canonical UTF-8/content formatting; no locale/time-dependent mutation in canonical document identity.

### AI-generated artifacts
AI may generate code/art/mesh/game logic, but output must pass AST/spec/dependency validation and may not inject runtime entropy into authority.

## 27. Deployment gate
Deploy only when:
- SpecHash valid;
- dependency lock matches;
- ArtifactRootHash matches;
- resource profile accepted;
- permissions bounded;
- Universe sealed.

No hot patch/live edit. Any modification creates a new build/hash.

## 28. Capability Graph
NCF replaces static “template types” with a DAG of versioned capabilities, e.g. runtime/render/storage/economy/AI/network/sandbox nodes.

Graph invariants:
- no cycles;
- bounded depth;
- no privilege escalation;
- explicit forbidden combinations;
- resource and permission scopes per node.

EnvelopeHash is derived from deterministically ordered capability IDs/versions. SpecHash binds EnvelopeHash + artifact/dependency roots.

Result: small apps use few nodes; AAAA apps use many nodes, while validation semantics stay the same.
