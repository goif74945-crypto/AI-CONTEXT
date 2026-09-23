# WORKFLOW — LONG-CONTEXT INGESTION

## Goal
Process sources larger than one model context without losing coverage, authority, contradictions or resumability.

## Core method
`INVENTORY → PARTITION → READ CHUNK → ANALYZE → NORMALIZE → CHECKPOINT → COVERAGE MAP → NEXT CHUNK`

## 1. Inventory
Record:
- source identity/version;
- size/pages/sections;
- table of contents/headings if available;
- expected domains.

## 2. Partition
Split by semantic domain/section, not arbitrary token size where possible.

## 3. Per-chunk extraction
Capture:
- facts;
- requirements;
- laws/invariants;
- entities/modules;
- contracts;
- state machines;
- numbers/defaults;
- conflicts;
- deprecations;
- evidence boundaries.

## 4. Immediate checkpoint
Write normalized durable context after each meaningful domain.
Do not wait until the whole source is loaded.

## 5. Coverage map
Track:
- processed ranges;
- target context file;
- unresolved ranges;
- duplicate/repeated material;
- authority/evolution notes.

## 6. Contradiction map
Never silently merge:
- old/new defaults;
- vision/build spec;
- source/runtime;
- mutually exclusive rules.

## 7. Completion
Only mark source-ingestion complete when:
- every major domain has a destination;
- gaps are explicit;
- contradictions are preserved;
- index/navigation exists;
- another AI can resume from coverage map.

## 8. Atomic-count warning
Do not infer “number of systems” from top-level headings until ontology/dedup rules define what counts as an atomic entity.
