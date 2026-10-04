import test from "node:test";
import assert from "node:assert/strict";
import { Q64_SCALE, UnitQ64 } from "../src/q64.ts";
import { CONCEPT_IDS, evaluateAll, evaluateConcept } from "../src/models.ts";
import type { SignalFrame, SignalName } from "../src/signals.ts";

const U = (n: bigint, d = 100n) => UnitQ64.fromFraction(n, d);

function healthyFrame(): SignalFrame {
  return {
    requirementClarity: U(99n), evidenceCoverage: U(98n), evidenceFreshness: U(97n), sourceDiversity: U(95n),
    contradictionPressure: U(2n), scopeDistance: U(1n), canonAlignment: U(99n), interfaceCompatibility: U(99n),
    regressionRisk: U(2n), failureObservability: U(98n), reversibility: U(97n), userValue: U(96n), safetyMargin: U(99n),
    deterministicReproducibility: U(100n), testCoverage: U(98n), uncertainty: U(2n), changeSurface: U(5n),
    agentDisagreement: U(3n), resourcePressure: U(10n), novelty: U(90n), rollbackReadiness: U(98n),
    dependencyStability: U(97n), provenanceCompleteness: U(99n), assumptionRatio: U(1n)
  };
}

function nextRaw(state: bigint): bigint {
  return (state * 6364136223846793005n + 1442695040888963407n) & ((1n << 64n) - 1n);
}

test("all 20 Lo4 concepts are present exactly once", () => {
  assert.equal(CONCEPT_IDS.length, 20);
  assert.equal(new Set(CONCEPT_IDS).size, 20);
});

test("all concept scores stay inside UnitQ64 for 2000 deterministic stress frames", () => {
  const names = Object.keys(healthyFrame()) as SignalName[];
  let state = 0x4e455859n;
  for (let i = 0; i < 2000; i++) {
    const frame = {} as SignalFrame;
    for (const key of names) {
      state = nextRaw(state);
      frame[key] = UnitQ64.fromRaw(state % (Q64_SCALE + 1n));
    }
    const scores = evaluateAll(frame);
    for (const id of CONCEPT_IDS) {
      assert.ok(scores[id].raw >= 0n, `${id} below zero`);
      assert.ok(scores[id].raw <= Q64_SCALE, `${id} above one`);
    }
  }
});

test("evidence reliability is monotonic in evidence coverage", () => {
  const low = healthyFrame();
  const high = { ...low, evidenceCoverage: UnitQ64.ONE };
  const lowScore = evaluateConcept("evidence-reliability", low);
  const highScore = evaluateConcept("evidence-reliability", high);
  assert.ok(highScore.raw >= lowScore.raw);
});

test("regression containment improves as regression risk decreases", () => {
  const highRisk = { ...healthyFrame(), regressionRisk: U(90n) };
  const lowRisk = { ...healthyFrame(), regressionRisk: U(10n) };
  assert.ok(evaluateConcept("regression-containment", lowRisk).raw > evaluateConcept("regression-containment", highRisk).raw);
});

test("scope integrity collapses under extreme scope distance and change surface", () => {
  const bad = { ...healthyFrame(), scopeDistance: UnitQ64.ONE, changeSurface: UnitQ64.ONE, requirementClarity: UnitQ64.ZERO };
  assert.equal(evaluateConcept("scope-integrity", bad).raw, 0n);
});

test("safety utility balance respects the weaker side", () => {
  const unsafe = { ...healthyFrame(), safetyMargin: UnitQ64.ZERO, userValue: UnitQ64.ONE };
  assert.equal(evaluateConcept("safety-utility-balance", unsafe).raw, 0n);
});
