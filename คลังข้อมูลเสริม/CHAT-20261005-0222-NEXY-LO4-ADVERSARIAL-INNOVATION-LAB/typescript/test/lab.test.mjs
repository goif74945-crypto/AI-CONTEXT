import test from "node:test";
import assert from "node:assert/strict";
import {
  analyzeContractDrift,
  EvidenceValue,
  evaluateAbstention,
  evaluateConstraints,
  InfluenceGraph,
} from "../dist/index.js";

test("AURORA passes safe calibrated behavior", () => {
  const report = evaluateAbstention([
    { caseId: "a", answerable: true, action: "ANSWER", correct: true, confidence: 0.99 },
    { caseId: "b", answerable: false, action: "ABSTAIN" },
  ], {
    wrongAnswerCost: 4,
    unanswerableAnswerCost: 8,
    needlessAbstainCost: 1,
    maxUnsafeAnswerRate: 0,
    minReliabilityScore: 0.99,
    maxBrierScore: 0.12,
  });
  assert.equal(report.status, "PASS");
});

test("MARGIN separates fragile pass from robust release", () => {
  const fragile = evaluateConstraints([{ name: "risk", actual: 0.099, operator: "<=", limit: 0.1, scale: 1, requiredMargin: 0.01 }]);
  assert.equal(fragile.releaseStatus, "REVERIFY");
  const robust = evaluateConstraints([{ name: "risk", actual: 0.01, operator: "<=", limit: 0.1, scale: 1, requiredMargin: 0.05 }]);
  assert.equal(robust.releaseStatus, "RELEASE");
});

test("UPA preserves contradiction and blocks release", () => {
  const merged = new EvidenceValue("TRUE", ["a"]).knowledgeJoin(new EvidenceValue("FALSE", ["b"]));
  assert.equal(merged.state, "CONFLICT");
  assert.equal(merged.releaseable, false);
});

test("TRACEWEIGHT detects dominance", () => {
  const graph = new InfluenceGraph([
    { nodeId: "a", parents: {}, isAgentSource: true, verified: true },
    { nodeId: "b", parents: {}, isAgentSource: true, verified: true },
    { nodeId: "final", parents: { a: 9, b: 1 } },
  ]);
  const report = graph.analyze("final");
  assert.equal(report.status, "FREEZE");
  assert.ok(report.reasons.includes("single_source_dominance"));
});

test("CONTRACT-DRIFT blocks silent scope expansion", () => {
  const before = {
    authorizedScope: ["read"], successInvariants: ["safe"], forbiddenActions: ["write-nexy"], assumptions: [], requiredEvidence: ["e2"],
  };
  const after = { ...before, authorizedScope: ["read", "deploy"] };
  const report = analyzeContractDrift(before, after);
  assert.equal(report.status, "FREEZE");
});

test("UPA De Morgan holds for all four states", () => {
  const states = ["TRUE", "FALSE", "UNKNOWN", "CONFLICT"];
  for (const a of states) for (const b of states) {
    const left = new EvidenceValue(a).and(new EvidenceValue(b)).negate().state;
    const right = new EvidenceValue(a).negate().or(new EvidenceValue(b).negate()).state;
    assert.equal(left, right);
  }
});
