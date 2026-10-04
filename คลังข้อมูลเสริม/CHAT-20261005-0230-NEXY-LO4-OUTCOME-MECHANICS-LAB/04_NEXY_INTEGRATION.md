# Future NEXY Integration Contract — Proposal Only

Intended flow:
NEXY normalized context -> validated Q64 input DTO -> selected Outcome Mechanics engine(s) -> NexyLo4Envelope -> NEXY LAW/JUDGE validation -> reject/quarantine/promote only by explicit governed process.

Before any real integration:
1. map engine inputs to authoritative NEXY sources;
2. define Zod/equivalent boundary schemas;
3. select canonical wire form for Q64 decimal strings or raw signed integers;
4. run exact-head NEXY TypeScript 6 compile and unit/integration tests;
5. run module-boundary and deterministic checks;
6. establish performance budgets;
7. revalidate against current Canon and promotion policy;
8. obtain explicit authorization before any NEXY.AI repository mutation.

Forbidden: automatic Canon promotion, hidden preference learning, direct side effects, silent JS-number coercion into Q64, or replacement of LAW/JUDGE/Safety authority.
