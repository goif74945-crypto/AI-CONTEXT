# NEXY.AI — Capability Registry / Admission / Public Governance / Chaos Deep Context

## Status
SOURCE-DESIGN / FUTURE GOVERNANCE FABRIC unless promoted by current authoritative build spec. NOT VERIFIED RUNTIME.

## 1. G20 — Versioned Capability Registry
Capability Registry is designed as:
- global;
- versioned;
- append-only;
- fixed-quorum governed;
- immutable per node/version.

Existing nodes are never edited in place or deleted historically.

### Canonical CapabilityNode
Fields include:
- id;
- semantic version;
- type: runtime/storage/network/render/AI/economy/etc.;
- dependencies;
- forbidden-with list;
- max recursion depth;
- resource profile;
- permission scope;
- deterministic class.

Canonical ordering:
id → version → hash.
Node identity:
`NodeHash = SHA-256(canonical_struct)`

## 2. Registry mutation FSM
New capability node requires:
- ProposalSpec;
- security-audit hash;
- fixed quorum signatures;
- public anchor inclusion;
- version lock.

State:
`PROPOSED → REVIEWED → QUORUM_SIGNED → ANCHORED → ACTIVE`

No retroactive activation.

## 3. Node immutability / sunset
Once ACTIVE, node identity/version/dependencies/conflicts are immutable.
Upgrade = new version.
Old versions remain valid unless a governed sunset process applies.

Sunset in source requires:
- fixed quorum;
- fixed notice window;
- anchored notice;
- no forced mutation of existing SpecHash/universes.

## 4. Envelope validation
UniverseSpec may use ACTIVE nodes only and must include exact versions.
System validates:
- dependency closure;
- forbidden collisions;
- deterministic class;
- resource/permission boundaries.

Envelope:
`EnvelopeHash = Merkle(sorted NodeHash)`

Same registry snapshot + node set + envelope must produce same EnvelopeHash across region/replay/fork boundary.

## 5. Deterministic classes
Named classes:
- **STRICT** — eligible for authoritative/deterministic simulation core.
- **SANDBOXED** — confined to lower/nested tiers.
- **NONDET_RENDER** — may participate in rendering/presentation but cannot mutate sovereign state.

A new version may not silently “upgrade” itself into a more privileged deterministic class.

## 6. Escalation prevention
Capability nodes may not:
- depend on Kernel authority;
- grant override powers;
- mutate Registry at runtime;
- introduce adaptive authority/governance.

Registry is intentionally not self-modifying.

## 7. Registry fork law
Political/quorum deadlock or constitutional split must become an explicit fork:
- major version boundary;
- Canon hash reset;
- public divergence anchor.

No silent registry divergence.

# G21 — Hybrid Capability Admission

## 8. Two-gate model
A new CapabilityNode becomes ACTIVE only after both:
- Gate A: deterministic static verifier.
- Gate B: fixed-quorum human policy review.

Missing either = REJECT.
No fast-track/emergency bypass in the described law.

## 9. Gate A — Static verifier
Mandatory machine checks include:
- canonical schema/structure;
- dependency closure;
- forbidden collision;
- deterministic class;
- resource cap;
- syscall scope;
- no authority escalation;
- no registry mutation path;
- no dynamic code loading;
- no undeclared/hidden network capability.

VerificationReport binds node/dependency hashes, deterministic class, static-analysis digest and verifier version. Report hash is anchored. Verifier itself is version-pinned and governed.

## 10. Gate B — Human quorum review
Human review is explicitly **policy-risk evaluation**, not an arbitrary opinion layer.

Review dimensions:
- economic exploit surface;
- cross-domain escalation;
- recursion abuse;
- resource amplification;
- legal/political exposure;
- long-term maintenance burden.

Approval requires fixed regional quorum signatures, anchored review-summary hash and reviewer DID records.
Reviewer cannot rewrite node; only ACCEPT/REJECT.

## 11. STRICT capability hardening
STRICT class additionally requires:
- two independent static-verifier builds;
- cross-compiler hash match;
- no float;
- no nondeterministic syscalls;
- proof of simulation boundary.

STRICT capability cannot downgrade its class in a later version to bypass restrictions.

## 12. Rejection finality / version evolution
Rejected node:
- cannot resubmit identical hash;
- must change structure/version;
- rejection is anchored;
- no silent retry.

New versions:
- declare compatibility;
- may not silently widen permission scope;
- may not exceed parent resource envelope without governance.
Violation freezes/rejects.

ACTIVE event binds node hash, verification hash, quorum signatures, registry root and time bundle. Capability becomes selectable only after FINALIZED anchor.

# G22 — Rejection Reason Code System (RCS)

## 13. Goal
Governance rejection must be:
- deterministic;
- replayable;
- machine-parseable;
- not dependent on free-text “vibes”.

## 14. Canonical RejectionRecord
Binds:
- proposal hash;
- node hash;
- registry version;
- verifier digest;
- sorted reason codes;
- reviewer DIDs;
- quorum signatures;
- review-summary hash;
- registry root;
- time bundle.

Reason-code list cannot be empty and is immutable after anchor.

Same node hash resubmission is automatically rejected under a duplicate-hash code in source.

## 15. Reason taxonomy
Machine/static examples:
- dependency cycle;
- permission escalation;
- resource cap violation;
- deterministic-class violation;
- undeclared network;
- dynamic code loading;
- nondeterministic syscall;
- noncanonical schema;
- container digest mismatch;
- spec-hash drift.

Human/policy examples:
- economic exploit vector;
- recursion abuse;
- resource amplification;
- cross-domain escalation;
- legal/political exposure;
- maintenance unsustainability;
- backward-compat break;
- insufficient risk analysis.

Important: free-text cannot itself be the authoritative reason; only governed reason codes are.

## 16. Governance replay
Given proposal source + registry snapshot + verifier/RCS versions, an external auditor should reproduce:
- static gate result;
- violated deterministic rule;
- applied human reason codes.

Replay mismatch freezes Registry.

## 17. Anti-drift rule
Invalid review conditions include:
- missing reason code;
- inactive/unknown reason code;
- missing reviewer signature;
- verifier-digest mismatch.

Registry becomes frozen until governance state is corrected.

## 18. RCS versioning
Reason-code registry is append-only.
Codes cannot be redefined or removed; they may be deprecated.
New codes require governed quorum + anchor.

Thus governance vocabulary itself becomes a constitutional artifact.

# G23 — Public Registry View

## 19. Transparency boundary
Internal RegistryData is not identical to public RegistryView.

Public must be able to:
- verify governance;
- replay admission logic;
- validate signatures;
- audit rejection history.

Public must not be able to:
- map infrastructure topology;
- fingerprint operational reviewer behavior;
- infer region layout;
- infer security posture;
- obtain exploit PoC details.

Principle: **Transparency ≠ raw dump.**

## 20. Public snapshot
PublicRegistrySnapshot includes:
- registry version;
- registry root hash;
- public capability node metadata;
- proposal/rejection/admission events;
- RCS/verifier versions;
- canonical timestamp bundle.

Ordering is explicit and deterministic.

## 21. Public capability fields
Exposed:
- id/version/type;
- deterministic class;
- dependencies/conflicts;
- max depth;
- abstracted resource profile;
- node hash.

Not exposed:
- internal static-analysis artifacts;
- private test vectors;
- infrastructure validation notes;
- reviewer commentary.

## 22. Public rejection event
Exposes:
- proposal/node hashes;
- registry version;
- reason codes;
- hashed reviewer identities;
- quorum signature set;
- review-summary hash;
- event hash.

Does not expose exploit proof/raw stress logs/internal security narrative.

## 23. Reviewer identity / topology opacity
Reviewer identity is public-key/DID based and hash-exposed without personal/region metadata.

Public view must not disclose region ids, quorum voting order, signature-timing offsets, node IP/ASN/cloud provider or other infrastructure map.

Only proof of signature validity/quorum is public.

## 24. Replay property
External auditor using public snapshot + verifier/RCS version should reconstruct:
- root hash;
- EnvelopeHash;
- dependency closure;
- rejection logic.

Failure to reproduce governance invalidates the claimed state.

## 25. Public mirroring
Design calls for hosted public view + IPFS mirror + minimal chain root commitment.
This is not meant to turn the whole registry into an unconstrained blockchain system.

# G25 — Adversarial Chaos Simulation / Self-Testing

## 26. Chaos model
Chaos runs in an isolated deterministic fork:
`ChaosUniverse = deterministic fork(current registry snapshot)`

It shares Spec/capability graph/economic constants/simulation engine, but uses a distinct namespace and cannot settle real CSU or mutate production state.

Chaos identity:
`ChaosUniverseHash = SHA-256(base_registry_root + chaos_config)`

## 27. Attack Vector Library
Append-only deterministic scenarios include examples such as:
- revenue velocity spike;
- recursive yield-loop attempt;
- circular cross-app settlement;
- shard divergence injection;
- double-transfer attempt;
- packet reorder burst;
- region partition;
- capability escalation;
- governance replay mismatch;
- massive AI feedback oscillation;
- liquidity shock flood;
- cartel concentration.

Each AttackScenario has:
- id;
- vector class;
- deterministic seed;
- parameter set;
- expected invariant set.

Sorted/hash-bound/append-only.

## 28. Deterministic chaos execution
Chaos must:
- use deterministic engine;
- use fixed seed;
- use fixed tick count;
- produce ChaosResultHash;
- avoid random fuzz/adaptive mutation.

Same scenario + same registry snapshot → identical ChaosResultHash across region/hardware/replay.

## 29. Chaos invariants
Tests include:
- ledger boundedness;
- no double credit;
- no state divergence;
- no recursion overflow;
- velocity caps;
- no governance bypass;
- no cross-shard duplication;
- no unbounded settlement acceleration.

Failure produces anchored CHAOS_FAILURE_EVENT.

## 30. Failure policy
If ChaosUniverse breaks an invariant:
- freeze capability admission/registry class affected;
- identify invariant class;
- require constitutional repair/fork path;
- publicly anchor failure hash;
- no silent/quiet patch.

Failure is treated as a constitutional event.

## 31. Scheduling
Chaos runs on:
- every major registry update;
- every STRICT capability addition;
- economic-rule proposals;
- fixed periodic schedule.

Not adaptive/event-triggered in the source branch.

## 32. Worst-case escalation tests
Simulation should exercise maxima such as:
- recursion depth;
- velocity limit attempts;
- shard transfer rate;
- AI agent density;
- cross-app graph depth.

Survival inside bounded invariants = pass.
Otherwise constitutional weakness is surfaced.

## 33. Isolation / public report
Chaos cannot:
- mutate real CSU ledger;
- anchor production shard state;
- modify registry.

It is epistemic testing, not production authority.

Public report may expose scenario id, tested invariants, pass/fail and result hash, but must hide weaponizable exploit detail and infrastructure timing.

## 34. Final property
The intended capability governance stack is **self-adversarial and publicly replayable**:
- it tests itself before deployment/governance promotion;
- it surfaces failure rather than silently repairing;
- it preserves deterministic evidence and policy history.
