# LICPL Architecture — Lo4 Innovation Containment

**Status:** AI-PROPOSED / ADVISORY / NON-CANON  
**Work code:** `CHAT-20261005-0222-NEXY-LO4-INNOVATION-CONTAINMENT-LAB`

## Design target

Lo4 is allowed to invent aggressively, but it must remain structurally unable to convert local intelligence, local tests, popularity, or self-generated evidence into NEXY authority.

The reference architecture therefore separates:

`INVENT -> PROVE LOCALLY -> PACKAGE EVIDENCE -> ELIGIBLE FOR HUMAN REVIEW`

from:

`AUTHORIZED PROMOTION -> CURRENT SPEC MAPPING -> NEXY INTEGRATION -> RUNTIME/DEPLOYMENT EVIDENCE -> GOVERNED ADOPTION`

The first sequence is implemented by this lab. The second sequence is intentionally absent.

## Invariants

1. AI workers are evidence producers, not authority.
2. No module may silently raise certainty, privilege, or promotion stage.
3. No automatic edge exists from Lo4 to Canon/Law/Judge/production.
4. Critical ambiguity or structural defect fails closed.
5. Equal canonical inputs produce equal identities in the tested reference path.
6. Experimental mutation must have a complete rollback/compensation model.
7. Supported historical contracts remain explicit obligations.
8. Human/operator surface complexity is an engineering budget, not something innovation may expand without limit.
9. Evidence floors are external invariants; a proposal may not lower its own bar.
10. NEXY integration remains NOT_VERIFIED until separately authorized and tested.

## Concept 1 — Authority Taint Flow Analyzer (ATFA)

ATFA models influence as a directed graph.

Nodes declare a trust class. Authority sinks declare required independently verified gate classes. For every path from an AI/untrusted source to an authority sink, ATFA proves that every required verified class appears on the path.

A node merely named “verifier” is insufficient; it must hold the required VERIFIED trust class. Cycles, missing sink requirements, state-budget exhaustion, and a discovered bypass return `FREEZE` with a witness.

Purpose: turn “AI cannot bypass authority” from policy prose into a graph-verifiable property.

## Concept 2 — Rollback Algebra Verifier (RAV)

RAV treats reversibility as a pre-execution proof obligation.

A forward experimental mutation must have exactly one explicit compensation. Compensation definitions are not counted as ordinary forward work. Dependency order is checked in both execution and rollback directions. An irreversible Lo4 mutation is rejected rather than accepted because its author labels the operation “safe”.

Purpose: prevent experimental innovation from creating one-way state damage while claiming a rollback that has never been structurally proven.

## Concept 3 — Compatibility Time Machine (CTM)

CTM compares a candidate interface contract against supported historical request/response contracts and stored behavior witnesses.

Request compatibility rejects newly required fields, removal of previously accepted fields, and narrowed enum domains. Response compatibility preserves prior required fields and rejects incompatible enum expansion where the old contract forbids it.

Behavior drift can be explicitly declared, but declaration alone is not authority. A nonempty external `authorization_ref` is required. Self-authorization is invalid.

Purpose: make backward compatibility executable rather than a semantic-version promise.

## Concept 4 — Operator Complexity Budget Compiler (OCBC)

OCBC compiles the user/operator control flow into a bounded directed graph with explicit limits:
- maximum visible actions per state;
- maximum decision depth;
- maximum confirmations per legal path;
- maximum exposed states.

It also rejects:
- destructive actions without confirmation;
- cycles where the flow contract forbids them;
- dead-end critical states;
- unreachable exposed states;
- budget overflow.

This is an engineering control-surface budget, not a scientific claim about human cognition or proof that a user will prefer the interface.

Purpose: preserve the NEXY “small surface / large backbone” direction even when backend capability grows.

## Concept 5 — Innovation Genome Protocol (IGP)

IGP packages a proposal, local proof state, limitations, protected scope, module decisions, and artifact hashes into a deterministic review packet.

Legal stages are:

`IDEA -> SPECIFIED -> PROTOTYPED -> VERIFIED_LOCAL -> EVIDENCE_PACKED -> ELIGIBLE_FOR_HUMAN_REVIEW`

There is intentionally no:
- CANON
- ADOPTED
- DEPLOYED
- PRODUCTION

The authority ceiling is `ADVISORY_ONLY`.

Promotion readiness requires all four assurance modules to PASS, valid lowercase SHA-256 artifact identities, explicit limitations, protected NEXY.AI scope, and fixed evidence floors E1/E2/E3_LOCAL. A genome cannot lower those floors to manufacture eligibility.

Purpose: make Lo4 maximally inventive but constitutionally weak.

## Composition

```text
Lo4 candidate
  |
  +--> ATFA: authority influence path safe?
  |
  +--> RAV: full reverse/compensation algebra?
  |
  +--> CTM: historical contract/behavior obligations preserved?
  |
  +--> OCBC: operator surface remains bounded and safe?
  |
  '--> IGP: deterministic evidence packet
              |
              '--> ELIGIBLE_FOR_HUMAN_REVIEW
                         |
                         X  no implemented promotion edge
                         |
                    NEXY authority
```

## Implementation constraints

The standalone reference implementation is dependency-free Python 3.11+.

The tested core path forbids:
- wall-clock reads;
- RNG;
- network access;
- subprocess execution;
- environment reads for authority decisions;
- dynamic eval/exec/compile/open/input/import tricks in core modules;
- floating-point literals in the assurance core.

Canonical JSON and SHA-256 are used for stable artifact identity.

## Evidence boundary

The design and implementation prove behavior only for this isolated reference package at the captured bytes. They do not authorize or prove NEXY runtime integration. Any future adoption must start from the then-current authoritative NEXY requirements and fresh evidence.
