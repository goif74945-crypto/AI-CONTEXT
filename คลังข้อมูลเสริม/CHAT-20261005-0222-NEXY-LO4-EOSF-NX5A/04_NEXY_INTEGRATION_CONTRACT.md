# NEXY Compatibility / Future Integration Contract

**Status:** DESIGN ONLY / Lo4 proposal / no live integration performed.

## Authoritative NEXY anchors used
Read-only AI-CONTEXT source context establishes these relevant current design facts in `projects/NEXY.AI/deep/doc-c-vnext-build-spec.md`:
- agent pipeline: no automatic retry by default; critical timeout freezes;
- all mutating routes require an idempotency key unless explicitly exempt;
- routes declare auth/RBAC/retry/audit/error behavior;
- queue states are `QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED / EXPIRED`;
- idempotency suppresses duplicate execution;
- FREEZE cancels pending release jobs and STOP cancels all jobs;
- failed jobs are not automatically retried unless explicitly safe;
- stale queue entries expire and payload is validated at enqueue and consume.

EOSF does not replace those laws. It is a proposed proof/admission layer that could sit before or around mutating queue consumers.

## Adapter boundary
A future NEXY-owned adapter should map canonical NEXY structures into EOSF contracts:
- route + actor/project + authority/config epoch + canonical payload -> ISC;
- explicit route retry policy + bounded worker/fanout graph -> RAB;
- durable queue/resource lease generation -> LFCG fence;
- transactional state/outbox row -> OES record;
- canonical queue job graph + materialized-effect metadata -> CCC.

## Required authoritative replacements on promotion
The standalone package intentionally avoids importing NEXY internals. Promotion should replace local canonical helpers with NEXY canonical serialization, IDs, error envelopes, tracing and evidence structures where authoritative.

## Database/runtime obligations not implemented here
A real adapter must prove:
1. idempotency identity has a durable uniqueness constraint;
2. lease fence increment and holder transition are atomic and monotonic;
3. outbox PREPARED/COMMITTED persistence participates in the same required transaction boundary as canonical mutation state;
4. outbox emission uses provider-specific idempotency where available and durable post-send reconciliation where not;
5. cancellation state and compensation obligations are persisted crash-safely;
6. queue consumer revalidates payload and policy epoch;
7. audit/event/freeze incidents link request_id + trace_id + incident_id as required by NEXY observability law;
8. LAW/JUDGE/release policy remains authoritative over actual NEXY state transitions.

## Forbidden adapter behavior
- treating EOSF `READY` as Canon authorization by itself;
- retrying a failed mutation solely because the provider timed out;
- deriving a new idempotency key after an ambiguous external effect just to “try again”;
- accepting stale fencing tokens;
- marking a job cancelled while ignoring a materialized side effect;
- assuming local E2/E3 evidence is NEXY E3/E4/E5/E6 evidence.
