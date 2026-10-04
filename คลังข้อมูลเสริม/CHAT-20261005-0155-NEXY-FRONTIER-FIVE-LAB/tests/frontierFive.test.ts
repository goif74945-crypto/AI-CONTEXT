import assert from "node:assert/strict";
import test from "node:test";
import {
  analyzeFrontierFive,
  cacheKey,
  canonicalJson,
  compareFingerprints,
  fingerprintRun,
  mineInvariants,
  minimizeFailure,
  ProvenanceAwareCache,
  selectMinimalEvidence,
  stableDigest,
  type CacheContext,
} from "../src/frontierFive.js";

// ===== core.test.ts =====

test("canonicalJson is invariant to object key order", () => {
  const a = { z: 1, a: { y: true, x: "v" } } as const;
  const b = { a: { x: "v", y: true }, z: 1 } as const;
  assert.equal(canonicalJson(a), canonicalJson(b));
  assert.equal(stableDigest(a), stableDigest(b));
});

test("canonicalJson rejects non-finite numbers", () => {
  assert.throws(() => canonicalJson({ x: Number.NaN }), /Non-finite/);
});

// ===== provenanceCache.test.ts =====

function context(overrides: Partial<CacheContext> = {}): CacheContext {
  return {
    namespace: "nexy.test",
    operation: "plan",
    input: { goal: "x" },
    authorityEpoch: "law-7",
    policyDigest: "policy-a",
    dependencyVersions: { spec: "sha-1", tool: "v2" },
    ...overrides,
  };
}

test("cache key is stable across dependency insertion order", () => {
  assert.equal(
    cacheKey(context({ dependencyVersions: { a: "1", b: "2" } })),
    cacheKey(context({ dependencyVersions: { b: "2", a: "1" } })),
  );
});

test("cache returns hit only for same evidence class and fresh record", () => {
  const cache = new ProvenanceAwareCache<{ ok: boolean }>();
  const ctx = context();
  cache.put({
    key: cacheKey(ctx),
    context: ctx,
    value: { ok: true },
    evidenceClass: "E2",
    createdAtMs: 100,
    expiresAtMs: 200,
  });

  assert.equal(cache.lookup(ctx, "E2", 150).status, "HIT");
  assert.deepEqual(cache.lookup(ctx, "E3", 150), { status: "MISS", reason: "EVIDENCE_CLASS_MISMATCH" });
  assert.deepEqual(cache.lookup(ctx, "E2", 201), { status: "MISS", reason: "STALE_TIME" });
});

test("provenance drift cannot alias the prior cache entry", () => {
  const cache = new ProvenanceAwareCache<{ ok: boolean }>();
  const original = context();
  cache.put({
    key: cacheKey(original),
    context: original,
    value: { ok: true },
    evidenceClass: "E2",
    createdAtMs: 100,
    expiresAtMs: 200,
  });

  assert.deepEqual(
    cache.lookup(context({ dependencyVersions: { spec: "sha-2", tool: "v2" } }), "E2", 150),
    { status: "MISS", reason: "DEPENDENCY_DRIFT" },
  );
});

test("authority and policy drift are diagnosed explicitly", () => {
  const cache = new ProvenanceAwareCache<{ ok: boolean }>();
  const original = context();
  cache.put({
    key: cacheKey(original),
    context: original,
    value: { ok: true },
    evidenceClass: "E2",
    createdAtMs: 100,
    expiresAtMs: 200,
  });
  assert.deepEqual(cache.lookup(context({ authorityEpoch: "law-8" }), "E2", 150), { status: "MISS", reason: "AUTHORITY_DRIFT" });
  assert.deepEqual(cache.lookup(context({ policyDigest: "policy-b" }), "E2", 150), { status: "MISS", reason: "POLICY_DRIFT" });
});

test("put rejects forged key", () => {
  const cache = new ProvenanceAwareCache<{ ok: boolean }>();
  assert.throws(
    () => cache.put({
      key: "forged",
      context: context(),
      value: { ok: true },
      evidenceClass: "E2",
      createdAtMs: 0,
      expiresAtMs: 1,
    }),
    /does not match/,
  );
});

// ===== determinismFingerprint.test.ts =====

const base = {
  input: { a: 1, b: 2 },
  state: { mode: "READY" },
  policy: { law: 7 },
  output: { result: "ok" },
  effects: [{ kind: "log", id: 1 }],
} as const;

test("fingerprint ignores object key insertion order but preserves effect order", () => {
  const first = fingerprintRun(base);
  const reordered = fingerprintRun({ ...base, input: { b: 2, a: 1 } });
  assert.deepEqual(compareFingerprints(first, reordered), { deterministic: true, changedDimensions: [] });

  const changedEffects = fingerprintRun({ ...base, effects: [{ id: 1, kind: "log" }, { kind: "log", id: 2 }] });
  assert.deepEqual(compareFingerprints(first, changedEffects), { deterministic: false, changedDimensions: ["effects"] });
});

test("fingerprint localizes output drift", () => {
  const first = fingerprintRun(base);
  const changed = fingerprintRun({ ...base, output: { result: "different" } });
  assert.deepEqual(compareFingerprints(first, changed).changedDimensions, ["output"]);
});

// ===== failureMinimizer.test.ts =====

test("minimizer finds a 1-minimal reproducer", () => {
  const steps = ["load", "auth", "transform", "race-a", "race-b", "save", "notify"];
  const result = minimizeFailure(steps, (candidate) => candidate.includes("race-a") && candidate.includes("race-b"));
  assert.deepEqual([...result.minimal].sort(), ["race-a", "race-b"]);
  assert.equal(result.oneMinimal, true);
  assert.ok(result.evaluations > 0);
});

test("minimizer rejects a non-failing initial candidate", () => {
  assert.throws(() => minimizeFailure(["a", "b"], () => false), /does not reproduce/);
});

test("minimizer enforces evaluation budget", () => {
  assert.throws(
    () => minimizeFailure(["a", "b", "c", "d"], (candidate) => candidate.length >= 2, { maxEvaluations: 1 }),
    /exceeded/,
  );
});

test("minimizer preserves duplicate positions instead of deleting by value identity", () => {
  const steps = ["dup", "trigger", "dup", "guard"];
  const result = minimizeFailure(steps, (candidate) => candidate.includes("trigger") && candidate.length >= 2);
  assert.equal(result.minimal.includes("trigger"), true);
  assert.equal(result.minimal.length, 2);
  assert.equal(result.oneMinimal, true);
});

// ===== invariantMiner.test.ts =====

const traces = [
  { state: "READY", latency: 10, nested: { version: 1 } },
  { state: "READY", latency: 20, nested: { version: 1 } },
  { state: "READY", latency: 15, nested: { version: 1 } },
] as const;

test("miner produces advisory proposals with support and ranges", () => {
  const proposals = mineInvariants(traces);
  assert.ok(proposals.length > 0);
  assert.ok(proposals.every((proposal) => proposal.status === "PROPOSAL"));
  assert.ok(proposals.some((proposal) => proposal.kind === "CONSTANT" && proposal.path === "$/state"));
  assert.ok(proposals.some((proposal) => proposal.kind === "NUMERIC_RANGE" && proposal.path === "$/latency"));
});

test("miner does not infer from insufficient samples", () => {
  assert.deepEqual(mineInvariants([{ x: 1 }, { x: 1 }]), []);
});

test("miner distinguishes missing path from required path", () => {
  const proposals = mineInvariants([{ x: 1 }, { x: 2 }, { y: 3 }]);
  assert.equal(proposals.some((proposal) => proposal.kind === "REQUIRED_PATH" && proposal.path === "$/x"), false);
});

test("miner does not depend on localeCompare for path traversal", () => {
  const original = String.prototype.localeCompare;
  Object.defineProperty(String.prototype, "localeCompare", {
    configurable: true,
    writable: true,
    value: () => { throw new Error("localeCompare must not be used"); },
  });
  try {
    const proposals = mineInvariants([{ z: 1, a: 2 }, { z: 1, a: 3 }, { z: 1, a: 4 }]);
    assert.ok(proposals.some((proposal) => proposal.path === "$/z"));
  } finally {
    Object.defineProperty(String.prototype, "localeCompare", {
      configurable: true,
      writable: true,
      value: original,
    });
  }
});

// ===== evidenceSelector.test.ts =====

const obligations = [
  { id: "schema", requiredClass: "E1" },
  { id: "unit", requiredClass: "E2" },
  { id: "integration", requiredClass: "E3" },
] as const;

test("selector finds exact minimum-cost proof set and respects evidence class", () => {
  const selection = selectMinimalEvidence(obligations, [
    { id: "lint", cost: 1, proves: [{ obligationId: "schema", evidenceClass: "E1" }] },
    { id: "unit-fast", cost: 2, proves: [{ obligationId: "unit", evidenceClass: "E2" }] },
    { id: "integration", cost: 5, proves: [
      { obligationId: "integration", evidenceClass: "E3" },
      { obligationId: "unit", evidenceClass: "E2" },
    ] },
    { id: "bundle", cost: 20, proves: [
      { obligationId: "schema", evidenceClass: "E1" },
      { obligationId: "unit", evidenceClass: "E2" },
      { obligationId: "integration", evidenceClass: "E3" },
    ] },
  ]);

  assert.deepEqual(selection.selectedIds, ["integration", "lint"]);
  assert.equal(selection.totalCost, 6);
});

test("selector does not treat higher evidence class as automatic substitution", () => {
  assert.throws(
    () => selectMinimalEvidence([{ id: "type-safety", requiredClass: "E1" }], [
      { id: "e2-only", cost: 1, proves: [{ obligationId: "type-safety", evidenceClass: "E2" }] },
    ]),
    /No evidence plan/,
  );
});

test("selector keeps mandatory candidate even if redundant", () => {
  const selection = selectMinimalEvidence([{ id: "u", requiredClass: "E2" }], [
    { id: "mandatory-audit", cost: 3, mandatory: true, proves: [] },
    { id: "unit", cost: 1, proves: [{ obligationId: "u", evidenceClass: "E2" }] },
  ]);
  assert.deepEqual(selection.selectedIds, ["mandatory-audit", "unit"]);
  assert.equal(selection.totalCost, 4);
});

test("selector chooses deterministic lexical tie-break for equal-cost exact plans", () => {
  const selection = selectMinimalEvidence([{ id: "x", requiredClass: "E2" }], [
    { id: "z-proof", cost: 1, proves: [{ obligationId: "x", evidenceClass: "E2" }] },
    { id: "a-proof", cost: 1, proves: [{ obligationId: "x", evidenceClass: "E2" }] },
  ]);
  assert.deepEqual(selection.selectedIds, ["a-proof"]);
});

// ===== integration.test.ts =====

test("five prototypes compose into one advisory report without claiming authority", () => {
  const report = analyzeFrontierFive({
    cacheContext: {
      namespace: "nexy.plan",
      operation: "compile",
      input: { request: "safe action" },
      authorityEpoch: "doc-b@7",
      policyDigest: "policy@abc",
      dependencyVersions: { spec: "doc-c@123" },
    },
    run: {
      input: { request: "safe action" },
      state: { mode: "READY" },
      policy: { userLaw: "allow" },
      output: { decision: "VERIFY" },
      effects: [],
    },
    traces: [
      { phase: "verify", retries: 0 },
      { phase: "verify", retries: 1 },
      { phase: "verify", retries: 0 },
    ],
    obligations: [
      { id: "parser", requiredClass: "E1" },
      { id: "behavior", requiredClass: "E2" },
    ],
    candidates: [
      { id: "typecheck", cost: 1, proves: [{ obligationId: "parser", evidenceClass: "E1" }] },
      { id: "unit", cost: 2, proves: [{ obligationId: "behavior", evidenceClass: "E2" }] },
    ],
    failingSteps: ["prepare", "race-a", "race-b", "cleanup"],
    reproducesFailure: (steps) => steps.includes("race-a") && steps.includes("race-b"),
  });

  assert.equal(report.advisoryOnly, true);
  assert.equal(report.cacheKey.length, 64);
  assert.equal(report.fingerprint.aggregate.length, 64);
  assert.deepEqual(report.evidencePlan.selectedIds, ["typecheck", "unit"]);
  assert.deepEqual([...report.minimizedFailure.minimal].sort(), ["race-a", "race-b"]);
  assert.ok(report.invariantProposals.some((proposal) => proposal.path === "$/phase"));
});
