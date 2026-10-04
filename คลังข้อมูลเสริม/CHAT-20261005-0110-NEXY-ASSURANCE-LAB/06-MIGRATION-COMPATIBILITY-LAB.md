# Migration & Compatibility Lab
Goal: permit future implementation evolution without silently weakening existing law.

Dimensions: FSM, evidence schema, law/constraint, replay, API/wire, durable ledger, release policy, operator/recovery.

Change classes: C0 projection-only; C1 additive compatible; C2 gated semantic extension; C3 authoritative migration; C4 breaking law change requiring explicit authority.

Migration proof packet: before/after schema+hashes; deterministic transform; invariants; golden fixtures; rollback policy if allowed; partial-failure behavior; interrupted migration recovery; replay accepted cases; replay frozen/rejected cases; proof no forbidden state becomes accepted.

Critical invariant: migration must not turn UNKNOWN, REJECTED, or FREEZE historical cases into ACCEPTED because information was dropped/defaulted.

Where semantics differ distinguish MISSING, explicit zero/false, UNKNOWN, LEGACY_NOT_REPRESENTABLE. Convenience defaults can convert data loss into false certainty.

During dual-read, compare readers and expose divergence. Silent preference hides incompatibility.

Completion requires golden replay, negative replay, interrupted migration, and post-migration exact-state verification.
