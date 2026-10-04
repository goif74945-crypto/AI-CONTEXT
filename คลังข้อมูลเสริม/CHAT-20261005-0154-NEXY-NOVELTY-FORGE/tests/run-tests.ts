import {
  computeOutcomeCredits,
  evaluateCrossModalConsistency,
  evaluateSemanticEntropy,
  mineObservedContracts,
  scheduleVerification,
  ContractError,
} from "../src/index.js";

let passed = 0;
let failed = 0;

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}

function equal<T>(actual: T, expected: T, message: string): void {
  if (actual !== expected) throw new Error(`${message}: expected ${String(expected)}, got ${String(actual)}`);
}

function approx(actual: number, expected: number, tolerance = 1e-9): void {
  if (Math.abs(actual - expected) > tolerance) throw new Error(`expected ${expected}, got ${actual}`);
}

function test(name: string, fn: () => void): void {
  try {
    fn();
    passed += 1;
    console.log(`PASS ${name}`);
  } catch (error) {
    failed += 1;
    console.error(`FAIL ${name}: ${error instanceof Error ? error.stack ?? error.message : String(error)}`);
  }
}

function expectContractError(fn: () => void): void {
  let threw = false;
  try {
    fn();
  } catch (error) {
    threw = error instanceof ContractError;
  }
  assert(threw, "expected ContractError");
}

test("cross-modal exact agreement passes", () => {
  const report = evaluateCrossModalConsistency([
    { artifactId: "spec", modality: "text", subject: "Auth", predicate: "ttl", object: "300s", critical: true },
    { artifactId: "config", modality: "config", subject: " auth ", predicate: "TTL", object: "300s", critical: true },
  ], { freezeOnCriticalConflict: true, minimumModalitiesForCrossCheck: 2 });
  equal(report.decision, "PASS", "decision");
  equal(report.crossCheckedKeys, 1, "cross-checked keys");
});

test("cross-modal critical contradiction freezes", () => {
  const report = evaluateCrossModalConsistency([
    { artifactId: "spec", modality: "text", subject: "Auth", predicate: "ttl", object: "300s", critical: true },
    { artifactId: "runtime", modality: "runtime", subject: "Auth", predicate: "ttl", object: "900s", critical: true },
  ], { freezeOnCriticalConflict: true, minimumModalitiesForCrossCheck: 2 });
  equal(report.decision, "FREEZE", "decision");
  equal(report.conflicts.length, 1, "conflict count");
});

test("cross-modal polarity contradiction is detected", () => {
  const report = evaluateCrossModalConsistency([
    { artifactId: "a", modality: "api", subject: "release", predicate: "authorized", object: "true", polarity: "affirm" },
    { artifactId: "b", modality: "test", subject: "release", predicate: "authorized", object: "true", polarity: "deny" },
  ], { freezeOnCriticalConflict: true, minimumModalitiesForCrossCheck: 2 });
  equal(report.decision, "REVIEW", "decision");
});

test("outcome credit satisfies symmetry", () => {
  const report = computeOutcomeCredits({
    actionIds: ["A", "B"],
    coalitionValues: { "": 0, "A": 1, "B": 1, "A|B": 2 },
  });
  approx(report.credits[0]!.contribution, 1);
  approx(report.credits[1]!.contribution, 1);
  approx(report.efficiencyResidual, 0);
});

test("outcome credit identifies dummy action", () => {
  const report = computeOutcomeCredits({
    actionIds: ["A", "B"],
    coalitionValues: { "": 0, "A": 3, "B": 0, "A|B": 3 },
  });
  const byId = Object.fromEntries(report.credits.map((item) => [item.actionId, item.contribution]));
  approx(byId["A"]!, 3);
  approx(byId["B"]!, 0);
});

test("outcome credit blocks incomplete counterfactual table", () => {
  expectContractError(() => computeOutcomeCredits({
    actionIds: ["A", "B"],
    coalitionValues: { "": 0, "A": 1, "B": 1 },
  }));
});

test("verification scheduler preserves mandatory evidence first", () => {
  const plan = scheduleVerification([
    {
      claimId: "release-auth",
      riskWeight: 10,
      failureImpact: 10,
      priorUncertainty: 1,
      mustVerify: true,
      options: [
        { optionId: "E6", costUnits: 4, expectedUncertaintyAfter: 0.1, satisfiesRequiredClass: true },
      ],
    },
    {
      claimId: "copy-tone",
      riskWeight: 1,
      failureImpact: 1,
      priorUncertainty: 0.8,
      mustVerify: false,
      options: [
        { optionId: "review", costUnits: 2, expectedUncertaintyAfter: 0.2, satisfiesRequiredClass: true },
      ],
    },
  ], 4);
  equal(plan.status, "PASS", "status");
  equal(plan.selected.length, 1, "selected count");
  equal(plan.selected[0]!.claimId, "release-auth", "mandatory selected");
});

test("verification scheduler blocks impossible mandatory class", () => {
  const plan = scheduleVerification([
    {
      claimId: "runtime-recovery",
      riskWeight: 5,
      failureImpact: 5,
      priorUncertainty: 1,
      mustVerify: true,
      options: [
        { optionId: "static-only", costUnits: 1, expectedUncertaintyAfter: 0.5, satisfiesRequiredClass: false },
      ],
    },
  ], 10);
  equal(plan.status, "BLOCKED", "status");
  equal(plan.uncoveredMandatoryClaims[0], "runtime-recovery", "uncovered claim");
});

test("verification scheduler chooses globally higher value plan", () => {
  const plan = scheduleVerification([
    {
      claimId: "A", riskWeight: 10, failureImpact: 1, priorUncertainty: 1, mustVerify: false,
      options: [{ optionId: "deep", costUnits: 3, expectedUncertaintyAfter: 0.1, satisfiesRequiredClass: true }],
    },
    {
      claimId: "B", riskWeight: 6, failureImpact: 1, priorUncertainty: 1, mustVerify: false,
      options: [{ optionId: "test", costUnits: 2, expectedUncertaintyAfter: 0, satisfiesRequiredClass: true }],
    },
    {
      claimId: "C", riskWeight: 6, failureImpact: 1, priorUncertainty: 1, mustVerify: false,
      options: [{ optionId: "test", costUnits: 2, expectedUncertaintyAfter: 0, satisfiesRequiredClass: true }],
    },
  ], 4);
  equal(plan.selected.length, 2, "selected count");
  assert(plan.selected.some((item) => item.claimId === "B"), "B selected");
  assert(plan.selected.some((item) => item.claimId === "C"), "C selected");
});

test("semantic entropy passes stable proposals", () => {
  const report = evaluateSemanticEntropy([
    { workerId: "w1", decisions: { route: "A", action: "freeze" } },
    { workerId: "w2", decisions: { route: "A", action: "freeze" } },
  ], { reviewThreshold: 0.3, freezeThreshold: 0.8, criticalDimensions: ["action"], minimumCoverage: 1 });
  equal(report.decision, "PASS", "decision");
  approx(report.aggregateEntropy, 0);
});

test("semantic entropy freezes critical split", () => {
  const report = evaluateSemanticEntropy([
    { workerId: "w1", decisions: { action: "execute" } },
    { workerId: "w2", decisions: { action: "freeze" } },
  ], { reviewThreshold: 0.2, freezeThreshold: 0.8, criticalDimensions: ["action"], minimumCoverage: 1 });
  equal(report.decision, "FREEZE", "decision");
  approx(report.dimensions[0]!.normalizedEntropy, 1);
});

test("semantic entropy reviews low coverage", () => {
  const report = evaluateSemanticEntropy([
    { workerId: "w1", decisions: { route: "A" } },
    { workerId: "w2", decisions: { route: null } },
  ], { reviewThreshold: 0.5, freezeThreshold: 0.9, criticalDimensions: [], minimumCoverage: 0.75 });
  equal(report.decision, "REVIEW", "decision");
});

test("contract miner preserves observed markers as non-authority", () => {
  const report = mineObservedContracts({
    "tests/auth.test.ts": '// @nexy-observed-contract {"requirementId":"REQ-AUTH-001","behavior":"rejects expired OTAC","evidenceClass":"E2"}',
  }, ["REQ-AUTH-001", "REQ-AUTH-002"]);
  equal(report.observations[0]!.authority, "OBSERVED_NON_AUTHORITY", "authority");
  equal(report.expectedRequirementStatus["REQ-AUTH-001"], "NOT_VERIFIED", "observed is not pass");
  equal(report.expectedRequirementStatus["REQ-AUTH-002"], "UNKNOWN", "missing remains unknown");
});

test("contract miner reports conflicting duplicate observations", () => {
  const report = mineObservedContracts({
    "tests/a.ts": '// @nexy-observed-contract {"requirementId":"REQ-1","behavior":"returns A","evidenceClass":"E2"}',
    "tests/b.ts": '// @nexy-observed-contract {"requirementId":"REQ-1","behavior":"returns B","evidenceClass":"E2"}',
  }, ["REQ-1"]);
  equal(report.expectedRequirementStatus["REQ-1"], "CONFLICT", "status");
  equal(report.duplicateConflicts.length, 1, "conflict count");
});

test("contract miner quarantines malformed markers", () => {
  const report = mineObservedContracts({
    "bad.ts": '// @nexy-observed-contract {oops}',
  }, []);
  equal(report.malformedMarkers.length, 1, "malformed count");
  equal(report.observations.length, 0, "observation count");
});

test("cross-modal report is invariant to input ordering", () => {
  const input = [
    { artifactId: "z", modality: "runtime" as const, subject: "S", predicate: "P", object: "B", critical: true },
    { artifactId: "a", modality: "text" as const, subject: "S", predicate: "P", object: "A", critical: true },
  ];
  const policy = { freezeOnCriticalConflict: true, minimumModalitiesForCrossCheck: 2 };
  const one = JSON.stringify(evaluateCrossModalConsistency(input, policy));
  const two = JSON.stringify(evaluateCrossModalConsistency([...input].reverse(), policy));
  equal(one, two, "stable report");
});

test("outcome credits are invariant to action ordering", () => {
  const coalitionValues = { "": 0, "A": 1, "B": 2, "A|B": 4 };
  const one = JSON.stringify(computeOutcomeCredits({ actionIds: ["A", "B"], coalitionValues }));
  const two = JSON.stringify(computeOutcomeCredits({ actionIds: ["B", "A"], coalitionValues }));
  equal(one, two, "stable credits");
});

test("verification scheduler is invariant to claim ordering", () => {
  const claims = [
    {
      claimId: "A", riskWeight: 2, failureImpact: 3, priorUncertainty: 1, mustVerify: false,
      options: [{ optionId: "x", costUnits: 2, expectedUncertaintyAfter: 0, satisfiesRequiredClass: true }],
    },
    {
      claimId: "B", riskWeight: 3, failureImpact: 2, priorUncertainty: 1, mustVerify: false,
      options: [{ optionId: "y", costUnits: 2, expectedUncertaintyAfter: 0, satisfiesRequiredClass: true }],
    },
  ];
  const one = JSON.stringify(scheduleVerification(claims, 2));
  const two = JSON.stringify(scheduleVerification([...claims].reverse(), 2));
  equal(one, two, "stable schedule");
});

test("semantic entropy is invariant to worker ordering", () => {
  const proposals = [
    { workerId: "b", decisions: { route: "B", action: "freeze" } },
    { workerId: "a", decisions: { route: "A", action: "freeze" } },
  ];
  const policy = { reviewThreshold: 0.2, freezeThreshold: 0.9, criticalDimensions: ["action"], minimumCoverage: 1 };
  const one = JSON.stringify(evaluateSemanticEntropy(proposals, policy));
  const two = JSON.stringify(evaluateSemanticEntropy([...proposals].reverse(), policy));
  equal(one, two, "stable entropy report");
});

test("contract mining is invariant to file map insertion order", () => {
  const markerA = '// @nexy-observed-contract {"requirementId":"REQ-A","behavior":"A","evidenceClass":"E2"}';
  const markerB = '// @nexy-observed-contract {"requirementId":"REQ-B","behavior":"B","evidenceClass":"E3"}';
  const one = JSON.stringify(mineObservedContracts({ "z.ts": markerB, "a.ts": markerA }, ["REQ-A", "REQ-B"]));
  const two = JSON.stringify(mineObservedContracts({ "a.ts": markerA, "z.ts": markerB }, ["REQ-A", "REQ-B"]));
  equal(one, two, "stable mining report");
});


test("verification scheduler blocks when mandatory cost exceeds budget", () => {
  const plan = scheduleVerification([
    {
      claimId: "deployment-proof",
      riskWeight: 10,
      failureImpact: 10,
      priorUncertainty: 1,
      mustVerify: true,
      options: [{ optionId: "E6", costUnits: 5, expectedUncertaintyAfter: 0, satisfiesRequiredClass: true }],
    },
  ], 4);
  equal(plan.status, "BLOCKED", "status");
  equal(plan.totalCostUnits, 5, "mandatory cost remains explicit");
});

test("semantic entropy rejects inverted thresholds", () => {
  expectContractError(() => evaluateSemanticEntropy([
    { workerId: "w1", decisions: { action: "a" } },
    { workerId: "w2", decisions: { action: "a" } },
  ], { reviewThreshold: 0.9, freezeThreshold: 0.2, criticalDimensions: ["action"], minimumCoverage: 1 }));
});

test("contract miner quarantines invalid evidence class", () => {
  const report = mineObservedContracts({
    "bad-evidence.ts": '// @nexy-observed-contract {"requirementId":"REQ-X","behavior":"x","evidenceClass":"E9"}',
  }, ["REQ-X"]);
  equal(report.malformedMarkers.length, 1, "malformed marker count");
  equal(report.expectedRequirementStatus["REQ-X"], "UNKNOWN", "invalid marker cannot establish observation");
});

test("cross-modal coverage gap is explicit rather than pass-by-silence", () => {
  const report = evaluateCrossModalConsistency([
    { artifactId: "spec-only", modality: "text", subject: "release", predicate: "authorized", object: "false", critical: true },
  ], { freezeOnCriticalConflict: true, minimumModalitiesForCrossCheck: 2 });
  equal(report.decision, "PASS", "no contradiction exists");
  equal(report.crossCheckedKeys, 0, "no cross-check exists");
  equal(report.diagnostics[0]!.code, "NO_CROSS_MODAL_COVERAGE", "coverage deficit must be surfaced");
});

test("outcome credit conserves asymmetric total delta", () => {
  const report = computeOutcomeCredits({
    actionIds: ["A", "B", "C"],
    coalitionValues: {
      "": 1,
      "A": 3,
      "B": 2,
      "C": 1.5,
      "A|B": 6,
      "A|C": 4,
      "B|C": 2.5,
      "A|B|C": 8,
    },
  });
  approx(report.credits.reduce((sum, item) => sum + item.contribution, 0), report.totalDelta, 1e-9);
  approx(report.efficiencyResidual, 0, 1e-9);
});

test("observed-contract output composes with verification scheduling without authority promotion", () => {
  const mined = mineObservedContracts({
    "tests/runtime.ts": '// @nexy-observed-contract {"requirementId":"REQ-RUNTIME","behavior":"recovery test exists","evidenceClass":"E2"}',
  }, ["REQ-RUNTIME", "REQ-DEPLOY"]);
  equal(mined.expectedRequirementStatus["REQ-RUNTIME"], "NOT_VERIFIED", "marker is not PASS");
  equal(mined.expectedRequirementStatus["REQ-DEPLOY"], "UNKNOWN", "missing remains UNKNOWN");
  const claims = Object.entries(mined.expectedRequirementStatus).map(([claimId, status]) => ({
    claimId,
    riskWeight: status === "UNKNOWN" ? 10 : 5,
    failureImpact: 10,
    priorUncertainty: status === "UNKNOWN" ? 1 : 0.7,
    mustVerify: claimId === "REQ-DEPLOY",
    options: [{
      optionId: claimId === "REQ-DEPLOY" ? "E6" : "E3",
      costUnits: claimId === "REQ-DEPLOY" ? 3 : 2,
      expectedUncertaintyAfter: 0.1,
      satisfiesRequiredClass: true,
    }],
  }));
  const plan = scheduleVerification(claims, 3);
  equal(plan.status, "PASS", "plan status");
  equal(plan.selected[0]!.claimId, "REQ-DEPLOY", "mandatory unknown deployment claim is scheduled first");
});

console.log(`SUMMARY passed=${passed} failed=${failed}`);
if (failed > 0) {
  throw new Error(`${failed} test(s) failed`);
}
