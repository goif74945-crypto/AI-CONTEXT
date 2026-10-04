import { performance } from "node:perf_hooks";
import { UnitQ64 } from "./src/q64.ts";
import { decidePromotion } from "./src/promotion.ts";
import type { SignalFrame } from "./src/signals.ts";

const U = (n: bigint, d = 100n) => UnitQ64.fromFraction(n, d);
const frame: SignalFrame = {
  requirementClarity: U(99n), evidenceCoverage: U(99n), evidenceFreshness: U(99n), sourceDiversity: U(98n),
  contradictionPressure: U(1n), scopeDistance: U(1n), canonAlignment: U(100n), interfaceCompatibility: U(100n),
  regressionRisk: U(1n), failureObservability: U(99n), reversibility: U(99n), userValue: U(99n), safetyMargin: U(100n),
  deterministicReproducibility: U(100n), testCoverage: U(99n), uncertainty: U(1n), changeSurface: U(2n),
  agentDisagreement: U(1n), resourcePressure: U(10n), novelty: U(95n), rollbackReadiness: U(99n),
  dependencyStability: U(99n), provenanceCompleteness: U(100n), assumptionRatio: U(1n)
};
const runs = 10000;
const start = performance.now();
let digest = "";
for (let i = 0; i < runs; i++) digest = decidePromotion(frame).receiptSha256;
const elapsedMs = performance.now() - start;
console.log(JSON.stringify({ runs, elapsedMs: Number(elapsedMs.toFixed(3)), decisionsPerSecond: Number((runs / (elapsedMs / 1000)).toFixed(2)), finalDigest: digest }));
