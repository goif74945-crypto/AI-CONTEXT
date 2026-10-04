# Twenty Lo4 Concepts — Q64 Operations Research Portfolio

> Status: AI_PROPOSED / NON_CANON / ADVISORY ONLY.

This portfolio intentionally focuses on deterministic operations research and execution planning. It is not a proof/trust/authority/counterfactual lab and does not replace NEXY::JUDGE, User Law, or existing verification gates.

| ID | Engine | Core question | Primary user value |
|---|---|---|---|
| OR20-01 | PARETO64 | Which candidates are not dominated across declared objectives? | Removes strictly worse choices without hiding tradeoffs. |
| OR20-02 | LEXI64 | Which candidate wins under an explicit immutable criterion order? | Predictable priority behavior without weighted-sum surprises. |
| OR20-03 | REGRET64 | Which action minimizes worst-case regret across scenarios? | Better choices under bounded uncertainty without pretending probabilities are known. |
| OR20-04 | PACK64 | Which bounded subset maximizes verified value within hard cost? | Higher value under explicit budgets. |
| OR20-05 | BOTTLENECK64 | Which assignment minimizes the maximum normalized worker load? | Prevents one agent/tool from becoming the hidden bottleneck. |
| OR20-06 | FAIR64 | How should divisible capacity be allocated by explicit weights and caps? | Stable, auditable fair sharing. |
| OR20-07 | DEADLINE64 | Can the declared work graph meet its deadline envelope? | Early detection of impossible schedules. |
| OR20-08 | CRITICAL64 | Which dependency chain determines minimum completion time? | Focuses optimization on actual blockers. |
| OR20-09 | SLACK64 | Where should spare schedule capacity be reserved? | Makes resilience intentional rather than accidental. |
| OR20-10 | INVERSION64 | Is lower-priority work blocking higher-priority work? | Prevents bad queue/lock ordering from sabotaging priorities. |
| OR20-11 | MATCH64 | Can agents/tasks be matched stably from explicit preferences? | Reduces churn in multi-agent assignment. |
| OR20-12 | DIVERSIFY64 | Does a selected strategy set exceed concentration limits? | Avoids betting everything on one correlated approach. |
| OR20-13 | BATCH64 | Which contiguous work grouping minimizes setup + processing cost? | Cuts repeated tool/context setup overhead. |
| OR20-14 | SWITCH64 | Is improvement large enough to justify switching strategy after friction? | Stops oscillation and thrash. |
| OR20-15 | STOPLOSS64 | Has marginal verified gain fallen below the declared continuation floor? | Stops wasting work when returns collapse. |
| OR20-16 | SLICE64 | Which independent result slices can be released without waiting for the entire mission? | Delivers safe partial value earlier. |
| OR20-17 | HANDOFF64 | Does a work package contain enough state/evidence/dependency closure for another executor? | Makes long work resumable instead of personality-dependent. |
| OR20-18 | OPTION64 | Is an irreversible action consuming more future-option reserve than authorized? | Preserves reversibility until commitment is justified. |
| OR20-19 | OPPCOST64 | Does admitting this task displace a more valuable feasible task? | Makes queue admission reflect real tradeoffs. |
| OR20-20 | PORTFOLIO64 | Which bounded strategy portfolio maximizes worst-case utility under concentration caps? | Selects robust mixes instead of fragile single-strategy bets. |

All tie-breaking is canonical. Quantitative values use signed Q64.64. Any future NEXY adapter must be read-only/advisory until separately promoted and verified.
