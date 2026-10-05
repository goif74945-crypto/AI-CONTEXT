# E-V16RC13-STATIC-CLOSURE-PINNED-WORLD-P0-F0D72593

ESCALATION_ID: E-V16RC13-STATIC-CLOSURE-PINNED-WORLD-P0-F0D72593
TARGET_AUTHORITY_KEY: b11e0417b2731cdb032af51b723d555b1e06f275426ee85276f4254191d4cc93
CURRENT_CONSTITUTION: NEXY::EQUAL-PEER-FENCED-ATOMIC-DYNAMIC-SCALE-ENGINEERING-CONSTITUTION-V16-RC1.3
CURRENT_PHASE: PHASE_1_STATIC_CONTROL_REPAIR
PUBLISHER_CHAT_ID: C-SOL-20261005-0936-0800-V16RC13-LAWID-3E906E53
PUBLISHER_MEMBERSHIP_ID: PRE-bdf83c3a2ea67f90e815aa6dc0735136
STATUS: USER_AUTHORITY_REQUIRED
PRODUCT_MUTATION: NONE
TARGET_INTEGRATION: NONE

## Canonical blocker

Finding:
NEXY-BUILD-CONTROL/FINDINGS/FINDING-V16RC13-CLOSURE-PINNED-WORLD-MEMBERSHIP-RACE-F0D72593.json

Independent reproduction:
NEXY-BUILD-CONTROL/V16/PREACTIVATION/REVIEWS/d5/REVIEW-C-SOL-20261005-0924-0800-V16RC13-C01D48AF-F0D72593.json

The finding is OPEN / P0 and the independent review verdict is CONFIRMED_P0.
Clause [184] therefore prevents PHASE_1 -> PHASE_2 because STATIC_PROTOCOL_P0 == 0 is not true.

## Failure mechanism

The active law permits post-barrier joins under [197].
Closure pins MEMBERSHIP_ROOT_HASH and DRAIN_MANIFEST_ROOT_HASH under [200]-[209], but it does not establish an immutable membership cutoff for the swept closure universe.
A post-pin membership write can therefore change the current-epoch membership set without changing MISSION_FENCE_STATE.STATE_VERSION.
The COMPLETE preconditions in [214] do not explicitly require the current membership/drain roots to equal the pinned roots, while [215] CASes only Mission Fence STATE_VERSION.
A COMPLETE CAS can therefore succeed against a stale membership/drain universe.

## Why this requires user authority

Repair changes Constitution semantics and terminal-success invariants.
Under the active authority order, an engineering peer may diagnose and propose the repair but must not silently rewrite the active Constitution or declare the P0 resolved.
A superseding explicit law change, or authoritative proof that disproves the counterexample, is required.

## Minimal repair contract for the superseding law

1. At distributed-closure entry, atomically freeze the closure membership universe by either:
   - rotating MEMBERSHIP_EPOCH and binding the pre-rotation epoch as CLOSURE_MEMBERSHIP_EPOCH; or
   - establishing an immutable CLOSURE_MEMBERSHIP_CUTOFF_GENERATION.

2. After that freeze, no record that belongs to the pinned closure universe may be created or mutated. Post-barrier joins allowed by the successor of [197] must enter a distinct audit-only epoch/generation and must be excluded from MEMBERSHIP_ROOT_HASH and DRAIN_MANIFEST_ROOT_HASH for that closure generation.

3. Persist the exact pinned closure tuple in authoritative fence state. At minimum it must bind every closure-relevant item already required by [209], including:
   TARGET HEAD/TREE,
   mission generation,
   law hash,
   Spec hash,
   source root,
   active-build root,
   deployment root,
   resource graph,
   shard universe,
   membership root,
   drain root,
   dependency root,
   test-environment hash,
   control-P0 root,
   engineering epoch,
   closure generation.

4. COMPLETE must require a fresh recomputation/readback proving exact equality of the entire current closure tuple to the pinned tuple immediately before the expected-version CAS. Any mismatch must REOPEN rather than COMPLETE.

5. The COMPLETE CAS must bind both the expected Mission Fence STATE_VERSION and the exact pinned closure tuple identity. No sharded membership/drain mutation for the frozen closure universe may race between the final tuple validation and COMPLETE authority transition.

6. Preserve fail-closed behavior. This repair does not authorize product mutation, target integration, legacy drain advancement, activation, or closure while other Phase-1 blockers remain.

## Current fence observed before escalation

BOOTSTRAP_FENCE_STATE: BLOCKED
BOOTSTRAP_FENCE_STATE_VERSION: 6
WORK_ADMISSION_GATE: READ_ONLY_PREACTIVATION
MUTATION_GATE: CLOSED
INTEGRATION_GATE: CLOSED
LEGACY_DRAIN_STATUS: NOT_AUTHORIZED_TO_ADVANCE_UNTIL_PHASE_1_GATE_PASSES

## Stop condition

Do not advance to PHASE_2 on the basis of V16-RC1.3 while this static protocol P0 remains OPEN.
Resume normal automatic phase advancement only after an authorized superseding law is durably pinned/activated or authoritative evidence closes/supersedes the P0, and the complete Phase-1 gate is recomputed to zero.
