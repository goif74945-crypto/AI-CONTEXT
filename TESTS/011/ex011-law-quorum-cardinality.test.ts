import { describe, expect, it } from "vitest";
import { isReleaseCandidate, prereleaseGate } from "../../packages/law/prerelease.js";
import { VNEXT_DEFAULTS } from "../../packages/api/vnext-config.js";

const valid = {
  confidence: 0.99,
  deterministicMatchScore: 0.99,
  quorumCount: 2,
  evidenceCount: 2,
  candidateHash: "b".repeat(64),
  agentIds: ["agent-01", "agent-02"],
};

describe("EX011 LAW quorum agent cardinality fail closed", () => {
  it("rejects quorum >=2 claimed from only one distinct agent", () => {
    const impossible = { ...valid, agentIds: ["agent-01"] };
    expect(isReleaseCandidate(impossible)).toBe(false);
    const outcome = prereleaseGate(impossible);
    expect(outcome).toEqual({
      passed: false,
      reasons: ["SCHEMA_VIOLATION"],
      threshold_snapshot: { ...VNEXT_DEFAULTS.release },
    });
  });
  it("rejects quorum count exceeding supplied unique agent identities", () => {
    const impossible = { ...valid, quorumCount: 10 };
    expect(isReleaseCandidate(impossible)).toBe(false);
    expect(prereleaseGate(impossible).passed).toBe(false);
  });
  it("retains canonical exact-quorum passing case", () => {
    expect(isReleaseCandidate(valid)).toBe(true);
    expect(prereleaseGate(valid)).toEqual({
      passed: true, reasons: [], threshold_snapshot: { ...VNEXT_DEFAULTS.release },
    });
  });
  it("retains current independently reported quorum threshold rejection", () => {
    const low = { ...valid, quorumCount: 1 };
    expect(isReleaseCandidate(low)).toBe(true);
    const outcome = prereleaseGate(low);
    expect(outcome.passed).toBe(false);
    expect(outcome.reasons).toContain("CONSENSUS_FAILED");
  });
  it("continues rejecting duplicate agent identities", () => {
    expect(isReleaseCandidate({ ...valid, agentIds: ["agent-01", "agent-01"] })).toBe(false);
  });
});
