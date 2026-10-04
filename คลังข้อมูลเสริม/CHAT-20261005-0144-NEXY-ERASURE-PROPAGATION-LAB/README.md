# NEXY Provenance-Aware Erasure & Tombstone Lab

Classification: EXPERIMENTAL / AI-PROPOSED CONCEPT / ADVISORY REFERENCE IMPLEMENTATION ONLY

Local chat/work reference: CHAT-20261005-0144-NEXY-ERASURE-PROPAGATION-LAB
Platform immutable ChatGPT conversation ID: UNKNOWN / NOT EXPOSED BY AVAILABLE TOOLING.

## Objective

Provide a deterministic, fail-closed reference protocol for privacy-aware deletion propagation that can be integrated with NEXY.AI in the future without mutating the NEXY.AI repository in this work.

The protocol separates four things humans routinely collapse into the word delete:

1. revoke user-facing access,
2. physically destroy exclusively-owned content,
3. remove or rebuild derived projections,
4. preserve immutable audit provenance through non-secret tombstones.

## Why this exists

The NEXY snapshot inspected read-only at commit 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43 already exposes soft-delete metadata, an artifact hard-delete marker, storage lifecycle state, immutable Revision/Commit records, and append-only audit history. A naive cascade delete would conflict with those invariants.

This lab therefore plans erasure over an explicit provenance graph and emits evidence obligations instead of pretending one database DELETE proves global erasure.

## Core properties

- deterministic plan hash and action IDs
- explicit READY / PARTIAL_HOLD / PENDING_EXTERNAL / FREEZE states
- executionAuthorized is false for every frozen plan
- legal/retention holds block destructive actions without hiding erasure intent
- cross-owner exclusive data never mutates automatically
- shared derivatives are rebuilt without the erased source when provenance is complete
- immutable audit history receives an append-only tombstone action
- external exports require an external erasure receipt
- missing targets, dangling edges, cycles, incomplete shared provenance, immutable mutation attempts and unknown external adapters fail closed
- receipt verification is bound to planHash, actionId, nodeId and evidenceHash

## Scope lock

IN SCOPE:
- standalone TypeScript reference implementation
- compatibility analysis against a read-only NEXY snapshot
- deterministic erasure planning
- receipt verification
- executable critical tests and broader local regression evidence
- security/privacy failure-mode documentation

OUT OF SCOPE:
- any modification to a repository whose name contains NEXY.AI
- production migration
- object-store deletion
- cache/index adapter implementation
- legal advice or assertion of regulatory compliance
- claim that NEXY.AI already implements this protocol

## Verification snapshot

Fresh local verification before persistence:
- npm test: 36 tests, 36 pass, 0 fail
- npm run typecheck: exit 0 with strict TypeScript configuration
- npm run test:coverage: all files 99.90% line, 93.98% branch, 99.01% functions
- planner.ts: 99.70% line, 90.83% branch, 100% functions
- persisted critical test suite: 12/12 pass

See DESIGN.md, INTEGRATION.md, REQUIREMENT_LEDGER.md, STATE.md and evidence/EVIDENCE.md.
