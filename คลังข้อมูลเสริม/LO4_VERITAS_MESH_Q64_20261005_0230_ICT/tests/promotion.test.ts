import test from "node:test";
import assert from "node:assert/strict";
import { UnitQ64 } from "../src/q64.ts";
import { decidePromotion, decisionToPortableJson } from "../src/promotion.ts";
import type { SignalFrame } from "../src/signals.ts";

const U = (n: bigint, d = 100n) => UnitQ64.fromFraction(n, d);
function strong(): SignalFrame {
  return {
    requirementClarity: U(99n), evidenceCoverage: U(99n), evidenceFreshness: U(99n), sourceDiversity: U(98n),
    contradictionPressure: U(1n), scopeDistance: U(1n), canonAlignment: U(100n), interfaceCompatibility: U(100n),
    regressionRisk: U(1n), failureObservability: U(99n), reversibility: U(99n), userValue: U(99n), safetyMargin: U(100n),
    deterministicReproducibility: U(100n), testCoverage: U(99n), uncertainty: U(1n), changeSurface: U(2n),
    agentDisagreement: U(1n), resourcePressure: U(10n), novelty: U(95n), rollbackReadiness: U(99n),
    dependencyStability: U(99n), provenanceCompleteness: U(100n), assumptionRatio: U(1n)
  };
}

test("strong Lo4 candidate becomes eligible only for review, never auto-promoted", () => {
  const d = decidePromotion(strong());
  assert.equal(d.status, "ELIGIBLE_FOR_PROMOTION_REVIEW");
  assert.equal(d.authority, "NON_CANONICAL_LO4_ONLY");
  assert.equal(d.canonicalPromotionPerformed, false);
  assert.deepEqual(d.failedMandatoryGates, []);
});

test("unsafe candidate is rejected", () => {
  const d = decidePromotion({ ...strong(), safetyMargin: UnitQ64.ZERO, evidenceCoverage: UnitQ64.ZERO, testCoverage: UnitQ64.ZERO });
  assert.equal(d.status, "REJECT");
  assert.ok(d.failedMandatoryGates.includes("safety-utility-balance"));
});

test("borderline candidate is quarantined rather than granted authority", () => {
  const mid = U(70n);
  const d = decidePromotion({
    ...strong(),
    requirementClarity: mid, evidenceCoverage: mid, evidenceFreshness: mid, canonAlignment: mid,
    interfaceCompatibility: U(80n), regressionRisk: U(30n), safetyMargin: mid, deterministicReproducibility: U(80n),
    testCoverage: mid, provenanceCompleteness: mid, reversibility: mid, rollbackReadiness: mid
  });
  assert.equal(d.status, "QUARANTINE");
  assert.equal(d.canonicalPromotionPerformed, false);
});

test("receipt is deterministic and portable raw Q64.64 JSON contains no float fields", () => {
  const a = decidePromotion(strong());
  const b = decidePromotion(strong());
  assert.equal(a.receiptSha256, b.receiptSha256);
  assert.match(a.receiptSha256, /^[0-9a-f]{64}$/);
  const portable = JSON.parse(decisionToPortableJson(a));
  assert.equal(typeof portable.overallRawQ64_64, "string");
  assert.equal(portable.canonicalPromotionPerformed, false);
});
