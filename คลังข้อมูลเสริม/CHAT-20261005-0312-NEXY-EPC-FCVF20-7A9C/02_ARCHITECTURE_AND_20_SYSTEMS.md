# FCVF-20 Architecture and System Design

## Design objective

The ordinary EPC question is "what should we keep, cut, defer, or prepare for promotion?" FCVF asks a different question: **can the mechanism answering that question violate its own constitution?** This separation prevents a high proposal score from laundering a protocol violation into authority.

The architecture is deliberately pure and immutable. `CourtState + Event + Constitution -> TransitionResult`. The strict constitution is fixed for production-reference tests; configurable flags exist only so regression tests can intentionally weaken individual laws and verify that the invariant layer catches the weakening.

## State domains

A court state contains a durable `CHAT_ID`, candidate identity/path, exact source/repository pins, work status, immutable evidence set, vote history, append-only vote revisions, DEFER count, non-destructive disposition, and three protected-authority indicators (`promoted`, `external_core_mutations`, `canon_overrides`). Strict transitions never permit the three protected indicators to change from their safe values.

Quantitative protocol metrics use a `Q64` value whose raw carrier is restricted to the signed i128 domain. All constructors and arithmetic paths reject binary floats. Overflow and division by zero fail closed with explicit exceptions rather than wrapping.

## Exactly 20 systems

| ID | System | Executable obligation |
|---|---|---|
| CSM | Constitutional State Model | State counters and domains remain valid. |
| LVBA | Lifetime Vote Budget Automaton | KEEP <= 1 and CUT <= 1 for a CHAT_ID. |
| MEL | Monotone Evidence Lattice | Evidence is deduplicated, canonical and never erased by accepted transitions. |
| VIA | Verdict Immutability Automaton | Vote IDs remain unique; revisions attach to existing votes without rewriting them. |
| WNCT | WIP Non-Cut Theorem Checker | Every reachable CUT vote has `READY` status before voting. |
| ANIC | Authority Non-Interference Checker | External Core mutation count remains zero. |
| CNOP | Canon Non-Override Property Checker | Canon override count remains zero. |
| PNCG | Promotion Non-Causality Gate | Court state can never become automatically promoted. |
| NDCS | Non-Destructive CUT Semantics Checker | CUT disposition is only ARCHIVED, REJECTED, or SUPERSEDED. |
| EPCC | Evidence Provenance Closure Checker | Votes carry spec/code/AI-CONTEXT/test locators and exact source/commit pins. |
| SDWL | Semantic Duplicate Witness Law | Duplicate evidence requires both a concrete target and semantic witness. |
| DPEC | Deterministic Permutation Equivalence Checker | Reordering an equivalent evidence set leaves the canonical state hash unchanged. |
| CRS | Canonical Receipt Serializer | Court states/receipts serialize deterministically; float input is forbidden. |
| QMDC | Q64.64 Metric Domain Checker | Every quantitative vote field is Q64 within signed i128 bounds. |
| MEFP | Missing-Evidence Freeze Property | KEEP/CUT cannot exist without all four critical evidence classes. |
| MCR | Minimal Counterexample Reducer | Violating traces are shrunk deterministically to a 1-minimal witness. |
| BSSEE | Bounded State-Space Exhaustion Engine | Reachable states are enumerated to a configured depth and every child is checked. |
| COR | Constitutional Obligation Registry | The verifier registry is exactly 20 unique, callable, named obligations. |
| CRD | Constitutional Regression Differential | Weak constitutions are compared against strict law and must expose unsafe reachable states. |
| PWCV | Promotion Witness Contract Validator | Review-readiness may exist only while all hard non-authority invariants remain true; it never promotes. |

## Safety properties

The principal safety invariant is a conjunction of non-escalation and vote-integrity conditions. No reachable strict state may contain a second KEEP or CUT, an auto-promotion flag, a Core mutation, a Canon override, a destructive CUT, a WIP CUT, a vote without provenance closure, or an invalid semantic duplicate witness.

Blocked authority attacks are **state identity transitions**: the returned state is the same immutable object and has the same canonical hash. This is stronger than merely returning an error while accidentally changing a side field.

## Temporal/lifetime properties

Vote rights are lifetime properties, not request-local validation. The current vote history is the authority for rights consumption. DEFER increments only its own counter. Vote revisions append lineage but do not replace the base `VoteRecord`. Evidence grows monotonically because the model exposes attachment/union but no removal transition.

## Determinism

State-space iteration, evidence collections, locators, dependency/duplicate collections and JSON object keys are explicitly sorted. Canonical hashes are SHA-256 over UTF-8 canonical JSON. No randomness, wall-clock reads, network reads or filesystem iteration order participate in a court decision. Timestamps are supplied evidence fields and validated rather than generated inside the engine.

## Bounded proof semantics

`BSSEE` is intentionally described as **bounded exhaustive verification**, not an unbounded mathematical proof. For a finite event alphabet and depth `D`, it enumerates every newly reachable canonical state through depth `D`, evaluates all 20 obligations on every transition result, and produces a stable digest of the reached state set. Claims beyond that explored model remain outside the proof boundary.
