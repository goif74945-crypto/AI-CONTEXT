# Lo4 Promotion Gate

All five systems remain `Lo4_AI_PROPOSAL_ONLY / NON_CANON`.

A future promotion must not occur merely because this standalone reference implementation passes tests.

## Required gates before any NEXY Canon/build promotion
1. **Authority:** explicit user/spec authorization for promotion and NEXY repository mutation.
2. **Collision refresh:** compare against then-current NEXY and AI-CONTEXT work.
3. **Contract mapping:** map every EOSF input/output to canonical NEXY schemas, error envelopes, state machines and evidence classes.
4. **Data-layer proof:** transactional idempotency registry/outbox/fence persistence implemented with uniqueness/CAS constraints.
5. **Provider proof:** ambiguous timeout, duplicate request, provider idempotency and reconciliation cases tested against supported providers.
6. **Queue proof:** BullMQ/Redis or current queue implementation tested for crash/restart/stale-job/fencing/cancellation scenarios.
7. **Security review:** auth/RBAC/CSRF/audit interactions tested; no EOSF output bypasses LAW/JUDGE.
8. **E3 integration:** real NEXY module integration tests.
9. **E4 E2E:** API -> queue -> worker -> storage/outbox -> audit/freeze path.
10. **E5 runtime:** exact candidate build runtime evidence.
11. **E6 deployment:** production-shaped environment and rollback evidence.

## Promotion must freeze if
- any critical effect identity dimension is missing;
- a provider cannot disambiguate timeout outcomes and no safe reconciliation exists;
- fencing cannot be enforced at the actual commit point;
- cancellation can leave an untracked materialized effect;
- compensation semantics are assumed rather than evidenced;
- the proposed adapter changes NEXY authority ordering.
