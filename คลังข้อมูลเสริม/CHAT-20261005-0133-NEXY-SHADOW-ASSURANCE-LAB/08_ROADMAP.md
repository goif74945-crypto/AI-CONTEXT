# Roadmap

**AI-PROPOSED continuation roadmap.** This is deliberately larger than the current prototype and is not a claim of background work.

## Phase 1 — Prototype hardening
Version the record schema; add strict JSON schema validation; add redaction policy; add signed report manifest; add corrupted/truncated JSONL tests; benchmark 100k/1M cases.

## Phase 2 — Semantic adapters
Define adapters for decision records, provider outputs, policy snapshots and incident replay. Prove adapter equivalence before allowing cross-version comparisons.

## Phase 3 — Mutation assurance
Build automatic authority/evidence/freeze mutation operators. The assurance system itself must fail when its protections are intentionally weakened.

## Phase 4 — Differential corpus selection
Rank cases by changed dependency closure, prior incidents, freeze boundary proximity, action irreversibility and user-law sensitivity. Do not reduce the baseline denominator silently.

## Phase 5 — Governed rebaseline
Create a human-authorized workflow for intentional policy/action changes: proposal -> authority review -> new baseline -> shadow replay -> evidence -> explicit promotion decision.

## Phase 6 — Operational shadow mode
Only after isolation and privacy proof, feed real normalized decision metadata into the comparator with strict no-execution credentials. Define timeouts, partial corpus behavior and report retention.

## Phase 7 — NEXY adoption decision
Map the tool against exact current NEXY requirements at that future revision. Adopt only the pieces that survive authority, security, performance and evidence gates.
