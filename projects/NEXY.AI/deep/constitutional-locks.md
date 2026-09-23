# NEXY.AI — Constitutional / Deterministic Lock Stack

## Status
SOURCE-DESIGN / CANON-LOCKED-IN-SOURCE where explicitly stated. NOT VERIFIED RUNTIME. These laws span the large constitutional architecture and are broader than the narrower DOC-C/vNEXT build scope.

## Layer 1 — Constitutional Lock
Locked source decisions include:
- Integrity is the final invariant.
- Root-authority loss resolves toward permanent freeze in the locked branch.
- Global freeze can be triggered by the defined root/emergency governance path.
- Anchor publication requires all required publication legs to succeed before FINALIZED.
- Time authority uses a 3-member TSA set with 2-of-3 validity.
- CompromiseFlag requires independent anomaly evidence plus regional participation.
- Economic model is dual-layer: Constitutional Settlement Unit + app-level ledger.
- Degraded policy permits existing execution while blocking mutation.
- Only FINALIZED state is valid.

## Layer 2 — FSM Lock
Global states:
`BOOT → CANON_LOADED → ANCHOR_SYNCED → ACTIVE → DEGRADED → FROZEN → TERMINATED`

Key rules:
- Invalid/illegal transition → immediate FREEZE.
- Freeze exit: Owner OR fixed 3/5 quorum in the source branch.
- DEGRADED maximum: 24h in the locked source.
- Spec mutation requires rebuild/new `spec_hash`.
- App lifecycle: CREATED, BUILT, SEALED, DEPLOYED, ACTIVE, FROZEN, TERMINATED, ARCHIVED.
- Cross-universe permission revocation: immediate.
- Resource overload: graceful shutdown → kill; security violation: hard kill.
- Reproducibility requires same hash + binary + container digest.
- Empty anchor batches still produce a new anchored root.

## Layer 3 — Economic Invariants
Source-locked direction:
- Dual-layer accounting: fixed constitutional base + app-local expansion.
- No balance reversal.
- Deterministic on-ledger escrow engine.
- Revenue-share formula immutable and bound to `spec_hash`.
- Freeze affected account rather than global economy when possible.
- Disputes resolved by deterministic engine only.
- In degraded mode, settlement may continue while anchoring queues.
- Constitutional inflation is disallowed in the locked branch.
- Economic DoS control uses a bond + fee-floor concept.
- Ledger finality only after FINALIZED anchor batch.
- Integrity outranks economic availability/profit.

## Layer 4 — Sovereign Continuity & Catastrophic Law
- Global internet partition: continue local execution, block mutation.
- Loss of 3/5 region reachability: DEGRADED, mutation blocked.
- Anchor compromise: emergency replacement via fixed quorum and future-anchor invalidation semantics.
- TSA collapse beyond bound: emergency TSA replacement procedure.
- Root key loss: permanent FROZEN in the locked branch.
- Mirror collapse: rebuild from IPFS + chain root.
- Region-key compromise: 3/5 required for eviction.
- Hardware compromise: quarantine node.
- Canon-hash drift: automatic FREEZE.
- Chain halt: continue local execution + queue.
- Escrow exploit: freeze affected account.
- Final catastrophic priority: constitutional integrity.

## Layer 5 — Versioning & Evolution Law
- Major version = constitutional rewrite.
- Major trigger = Owner + fixed quorum in source.
- Minor versions may change non-immutable layers only.
- Core detection kernel is immutable.
- Backward compatibility is intended to persist.
- Existing spec versions continue until terminated rather than silent migration.
- Deprecated features use a fixed sunset window.
- Constitutional economic rules are not mutated in place.
- Anchor-contract changes require a new contract/migration.
- Constitutional amendments require a complete system fork.
- Integrity wins over convenience during evolution.

## Layer 6 — Creator Fabric
Creator-Fabric law creates an execution-freedom layer below constitutional authority:
- creator apps may build/run/publish within declared capabilities;
- creator apps cannot mutate Kernel, Anchor, authority, constitutional economy or sealed spec;
- publication is FSM-bound and requires FINALIZED;
- resource violation is locally contained;
- cross-app access requires explicit grants;
- creator economy is isolated from constitutional minting/settlement authority.

See `sovereign-fabric.md` for Creator AppSpec, publishing and resource-containment details.

## Layer 7 — Sandbox Tier Law
Recursive creation is monotonic downward in privilege:
- `NewAppTier = ParentTier + 1`.
- Tier cannot be lowered, reset or overridden.
- Child capability set must be a subset of parent capabilities.
- Child cannot increase CPU/network/storage/SDK privilege.
- Nested apps cannot create top-level public roots, mutate revenue-share law, access cross-universe registry, generate anchor events, spawn privileged containers or mount external filesystems.
- Nested economic activity remains bound to the parent/root `spec_hash`; no nested minting or settlement mutation.
- Violation kills the offending tier/subtree, never contaminating upward.
- Recursive apps cannot update Merkle root, sign anchor batches or trigger CompromiseFlag.

### Recursive depth invariant
`MAX_DEPTH = 5`, enforced at build time.
Tier 6 is impossible/undefined and results in rejection/freeze semantics.

Purpose:
- bounded graph depth;
- bounded permission evaluation;
- bounded forensic reconstruction;
- bounded kill/economic cascades;
- predictable complexity ceiling.

Only a constitutional fork may change the locked recursion policy in this source.

## Layer 8 — Implementation Verification Law
- Reproducible build mandatory; source names Nix/locked toolchain.
- `build_hash` incorporates compiler, flags and normalized environment.
- UTC/path/locale normalization.
- Core detector must be verified against source/known vectors.
- Node boot uses TPM/HSM attestation in the design.
- Periodic runtime memory/state hash verification.
- Deploy sequence: Seal → verify signature → verify `build_hash` → deploy.
- Supply-chain defense: rebuild from source.
- Containers are digest-pinned.
- Spec ↔ binary correspondence is checked.
- CI compromise freezes the affected node.
- Verification failure leads to automatic FREEZE.

## Layer 9 — Runtime Determinism Lock
### Canonical mutation
- Single-thread Core execution.
- No shared mutable state.
- No parallel canonical mutation.
- Workers may perform I/O isolation or non-authoritative computation only.
- Canonical state has exactly one deterministic mutator/executor.

### Async/event ordering
- Async only through an explicit deterministic state machine.
- No unordered futures / implicit promise scheduling.
- Explicit FIFO event queue.
- Strict monotonic counter.
- No dynamic priority in canonical event ordering.

### Allocator/environment
- Fixed/pinned allocator; source gives jemalloc as an example.
- No system allocator fallback.
- Allocator version is included in `build_hash`.
- Environment normalized: TZ=UTC, Locale=C, fixed LANG, normalized paths, no runtime environment mutation.
- Environment hash is part of `build_hash`.

### Numeric law
- Floating point forbidden in Core.
- Fixed-point/integer math only.
- Locked branch specifies signed 128-bit integer canonical arithmetic.
- Overflow → immediate FREEZE; no wrap/saturation/silent truncation.

### Time/randomness
- Core may not read system time.
- Canonical time enters only through the approved TSA/batch authority.
- No RNG/entropy/time-seeded randomness in Core.
- Pre-anchored deterministic seed is only allowed in non-authoritative sandbox contexts.

### Architecture/scheduling
- Canonical target architecture explicitly pinned/listed.
- Endianness and compiler target triple locked.
- Core cannot depend on OS scheduler timing, sleeps or time slices.
- State transitions are event-driven.

### State verification
Periodic canonical-state hash divergence → AUTO FREEZE.

### Determinism invariant
Same Spec + Canon + event stream + build/binary/environment must produce identical:
- state hash;
- anchor root;
- ledger result.

Divergence → AUTO FREEZE.

## Layer 10 — Crash & Recovery Law
### WAL-first mutation
Canonical mutation order:
1. serialize canonical event;
2. append to append-only WAL;
3. fsync;
4. mutate in-memory state;
5. ACK.

In-memory-first mutation, deferred disk flush and unproven durability are forbidden. fsync failure freezes.

### WAL format
Canonical binary encoding, fixed endianness/schema, length-prefixed entries, per-entry SHA-256. Entries include a monotonic counter, previous state hash, event hash, spec hash and signature-set hash. Corrupt valid history is never skipped.

### WAL segmentation
Fixed-size segments; segment naming links to previous segment root. No compaction/rewrite/prune without anchor confirmation.

### Snapshot law
Snapshot at fixed event/finalized-batch boundary. Snapshot contains full canonical state, Merkle root, build/spec hashes, allocator id and environment hash; snapshot hash is anchored.

Snapshot creation is freeze → serialize → hash → write → fsync → resume.

### Replay
Boot verifies binary/build/environment, loads latest valid snapshot, replays WAL strictly in order, recomputes state hash after each entry and compares final hash to anchored state. Any mismatch freezes.

### Partial/double-crash handling
- Incomplete final WAL entry may only be truncated under explicit checksum/length-invalid rules; truncation is logged.
- Snapshot uses two-phase commit: temp write + fsync → metadata commit flag + fsync → active rename.
- Crash during snapshot cannot silently promote an incomplete snapshot.

### Replay invariant
Replay cannot depend on time, memory address, thread order, inode order or filesystem directory iteration. Directory input is lexicographically ordered.

### Fork detection
Replayed state hash != anchored state hash → FROZEN + replay-divergence incident + mutation block. No auto-heal.

### Crash-loop behavior
Repeated replay crashes enter safe mode, block mutation and export a recovery package.

Final law: crash must never create history; replay must never invent state; if identical recovery cannot be proven, freeze.

## Layer 11 — Storage & I/O Non-determinism Containment
The source goes below application storage into device/kernel behavior.

### Device class
Preferred/allowed design: enterprise NVMe or SATA SSD with power-loss protection. Consumer/untrusted/opaque-cache storage is rejected. Device model and firmware are part of boot attestation.

### Write ordering
Critical writes use durability barriers such as O_DSYNC/fdatasync/fsync. Disabled barriers freeze.

### Cache/flush
Write cache must expose safe flush/FUA semantics. Unsafe hidden caching freezes.

### Filesystem
Locked source allows ext4 ordered mode and XFS with barriers; COW/overlay and async-journal paths are disallowed in this branch. Mount options are boot-hashed.

### Scheduler/kernel
I/O scheduler is pinned to an approved set; kernel version is pinned/hashed. Major drift freezes; lesser drift may degrade until verified.

### DMA/barrier
Critical ACK occurs only after syscall durability + compiler/CPU ordering barriers.

### Power-loss semantics
Partial WAL follows Layer 10 rules; uncommitted snapshots are discarded; segment rollover is verified by hash chain. Filesystem journal is not trusted as source of truth.

### RAID/storage topology
Mirroring (RAID1/10) is accepted in the source branch; parity RAID and opaque controller write-back caches are forbidden.

### Storage attestation hash
Includes device model, firmware, FS UUID/mount options, scheduler, kernel, CPU and microcode. Mismatch quarantines node.

### Error/replacement
Uncorrectable read errors freeze node/mark region degraded. Disk replacement requires full replay and state-hash equality before ACTIVE.

Storage invariant: storage must behave like an ordered append-only durability medium; inability to prove persistence halts execution.

## Layer 12 — Human & Operational Determinism
### Roles
Spec-bound role matrix:
Observer, Maintainer, Region Operator, Anchor Signer, Owner.
Privileges are Canon-defined/hash-anchored; no runtime privilege escalation.

### Override
No ad-hoc override. Only predefined Canon procedures such as freeze, emergency replace or constitutional fork. No generic `--force` semantics.

### Emergency grammar
Finite command vocabulary such as FREEZE_NODE, FREEZE_REGION, QUARANTINE_NODE, EMERGENCY_REPLACE, TERMINATE_APP, ARCHIVE_APP. Arbitrary shell mutation is forbidden.

### CLI/mutation
All operations require explicit target/spec hash/confirmation hash. Missing values reject.
Interactive production mutation is forbidden; mutations are signed/sealed operation bundles.

### Debug/SSH/config
No maintenance bypass or hidden debug mutation flags. Direct production shell mutation is forbidden/restricted to diagnostics. Configuration derives from sealed spec; drift freezes.

### Update
Freeze-first replacement: freeze node → replace binary → attest/verify → rejoin. No live partial patch.

### Two-person destructive actions
Dual signature required for region eviction, emergency anchor replacement, major upgrade and fork trigger.

### Operator audit
Operator actions produce signed, time-authorized, anchorable events. No private admin mutations.

### Incident response
Each incident class has a deterministic playbook, legal state transition and freeze boundary. Improvisational mutation is not allowed.

### Human invariant
Every state-changing human action must be finite, explicit, signed, anchored, replayable and auditable. If an operator action cannot be represented as a deterministic state transition, that action must not exist.
