import test from "node:test";
import assert from "node:assert/strict";
import { Q64 as Q } from "./shared/q64.ts";
import { chooseModel } from "./01_model-route-stabilizer/CODE.ts";
import { rankContext } from "./02_context-salience-field/CODE.ts";
import { allocateBudget } from "./03_compute-budget-allocator/CODE.ts";
import { evaluateBackpressure } from "./04_backpressure-governor/CODE.ts";
import { limitPreferenceUpdate } from "./05_personalization-drift-limiter/CODE.ts";
import { requireSafety } from "./06_safety-margin-envelope/CODE.ts";
import { optionValue } from "./07_mutation-option-valuator/CODE.ts";
import { rankRecovery } from "./08_recovery-path-planner/CODE.ts";
import { promotionGate } from "./09_lo4-promotion-gate/CODE.ts";
import { resolveConsensus } from "./10_consensus-weight-resolver/CODE.ts";
import { freshnessDiscount } from "./11_freshness-discount-engine/CODE.ts";
import { PrivacyBudgetGovernor } from "./12_privacy-budget-governor/CODE.ts";
import { accrueCredit, chooseRunnable } from "./13_fair-queue-credit-scheduler/CODE.ts";
import { choosePrecision } from "./14_latency-precision-governor/CODE.ts";
import { rankMemory } from "./15_memory-retention-ranker/CODE.ts";
import { rankTools } from "./16_tool-call-governor/CODE.ts";
import { severity } from "./17_incident-severity-aggregator/CODE.ts";
import { rankPrefetch } from "./18_predictive-prefetch-ranker/CODE.ts";
import { allocateDuty } from "./19_swarm-duty-allocator/CODE.ts";
import { filterIntent } from "./20_intent-stability-filter/CODE.ts";

test("all 20 systems compose in one deterministic local control flow",()=>{
  const bp=evaluateBackpressure({queue:Q.parse("0.20"),errors:Q.parse("0.05"),latency:Q.parse("0.15")});
  assert.equal(bp.level,"NORMAL");
  const precision=choosePrecision(Q.parse("0.9"),Q.parse("0.1"),bp.pressure,Q.parse("0.8"));
  assert.notEqual(precision.tier,"FAST");
  const w={quality:Q.fromInt(4n),latency:Q.fromInt(2n),cost:Q.fromInt(2n),safety:Q.fromInt(5n),stability:Q.fromInt(3n)};
  const model=chooseModel([
    {id:"alpha",quality:Q.parse("0.94"),latency:Q.parse("0.20"),cost:Q.parse("0.25"),safety:Q.parse("0.98"),stability:Q.parse("0.95")},
    {id:"beta",quality:Q.parse("0.91"),latency:Q.parse("0.15"),cost:Q.parse("0.20"),safety:Q.parse("0.96"),stability:Q.parse("0.90")}
  ],w,Q.parse("0.95"));
  assert.ok(model.id==="alpha"||model.id==="beta");
  const ctx=rankContext([
    {id:"canon",relevance:Q.parse("0.9"),authority:Q.one(),freshness:Q.parse("0.9"),userPriority:Q.parse("0.9"),contaminationRisk:Q.zero()},
    {id:"rumor",relevance:Q.one(),authority:Q.parse("0.2"),freshness:Q.one(),userPriority:Q.parse("0.2"),contaminationRisk:Q.parse("0.8")}
  ]);
  assert.equal(ctx[0].id,"canon");
  const budget=allocateBudget(Q.fromInt(100n),[{id:"reason",weight:Q.fromInt(3n),floor:Q.fromInt(20n)},{id:"verify",weight:Q.fromInt(2n),floor:Q.fromInt(20n)}]);
  assert.equal(Q.sum(budget.map(x=>x.amount)).raw,Q.fromInt(100n).raw);
  const pref=limitPreferenceUpdate(Q.parse("0.4"),Q.parse("0.9"),Q.parse("0.1"));
  assert.equal(pref.toDecimal(1),"0.5");
  const safe=requireSafety({likelihood:Q.parse("0.1"),impact:Q.parse("0.2"),containment:Q.one(),reversibility:Q.one()},Q.parse("0.8"));
  assert.ok(safe.compare(Q.parse("0.8"))>=0);
  const mutation=optionValue({id:"m",utility:Q.parse("0.9"),reversibility:Q.one(),blastRadius:Q.parse("0.1"),rollbackCost:Q.parse("0.1"),evidence:Q.parse("0.95")});
  assert.ok(mutation.compare(Q.parse("0.8"))>0);
  const recovery=rankRecovery([{id:"r",restoreProbability:Q.parse("0.95"),timeCost:Q.parse("0.2"),sideEffectRisk:Q.parse("0.1"),evidence:Q.parse("0.9"),reversibility:Q.one()}]);
  assert.equal(recovery[0].id,"r");
  const promo=promotionGate({evidence:Q.parse("0.95"),determinism:Q.one(),security:Q.parse("0.98"),regression:Q.parse("0.99"),integration:Q.parse("0.95")});
  assert.equal(promo.status,"ELIGIBLE_FOR_FORMAL_PROMOTION_REVIEW");
  const consensus=resolveConsensus([{agentId:"a",verdict:1,trust:Q.one(),reliability:Q.parse("0.95")},{agentId:"b",verdict:1,trust:Q.parse("0.9"),reliability:Q.parse("0.9")},{agentId:"c",verdict:-1,trust:Q.parse("0.2"),reliability:Q.parse("0.5")}],Q.parse("0.2"));
  assert.equal(consensus.decision,1);
  const fresh=freshnessDiscount(Q.one(),Q.fromInt(1n),Q.fromInt(4n));
  assert.ok(fresh.compare(Q.parse("0.7"))>0);
  const privacy=new PrivacyBudgetGovernor(Q.one());
  assert.equal(privacy.tryConsume(Q.parse("0.2")),true);
  let actor=accrueCredit({id:"u",credit:Q.zero(),cost:Q.parse("0.5")},Q.one(),Q.fromInt(2n));
  assert.equal(chooseRunnable([actor]).id,"u");
  const mem=rankMemory([{id:"keep",futureUtility:Q.one(),authority:Q.one(),uniqueness:Q.parse("0.9"),freshness:Q.parse("0.9"),privacyCost:Q.parse("0.1")}]);
  assert.equal(mem[0].id,"keep");
  const tool=rankTools([{id:"read",expectedUtility:Q.one(),confidence:Q.one(),latencyCost:Q.parse("0.1"),moneyCost:Q.zero(),mutationRisk:Q.zero()}]);
  assert.equal(tool[0].id,"read");
  assert.equal(severity({impact:Q.parse("0.2"),reach:Q.parse("0.1"),exploitability:Q.parse("0.1"),irreversibility:Q.parse("0.1"),spread:Q.parse("0.1")}).level,"S1");
  assert.equal(rankPrefetch([{id:"p",probability:Q.parse("0.9"),utility:Q.one(),sizeCost:Q.parse("0.1"),freshness:Q.one(),wasteRisk:Q.parse("0.1")}])[0].id,"p");
  const duties=allocateDuty([{id:"a",capacity:Q.one(),fitness:Q.one(),trust:Q.one(),load:Q.parse("0.2"),reserve:Q.one()},{id:"b",capacity:Q.parse("0.8"),fitness:Q.parse("0.8"),trust:Q.parse("0.9"),load:Q.parse("0.3"),reserve:Q.parse("0.8")}]);
  assert.equal(Q.sum(duties.map(x=>x.share)).raw,Q.one().raw);
  const intent=filterIntent({confidence:Q.parse("0.9"),stability:Q.parse("0.9"),direction:1},{confidence:Q.parse("0.95"),stability:Q.parse("0.9"),direction:1},Q.parse("0.6"));
  assert.equal(intent.acceptCurrent,true);
});
