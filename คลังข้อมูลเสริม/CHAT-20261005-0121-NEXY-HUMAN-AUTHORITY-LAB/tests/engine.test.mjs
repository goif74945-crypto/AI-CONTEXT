import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import {
  computeDisclosure,
  evaluateAcceptance,
  evaluateAction,
  evaluateScenario,
  evaluateTrace,
} from "../dist/src/engine.js";
import { sha256Canonical } from "../dist/src/canonical.js";

function baseContract(testCase = {}) {
  const missing = new Set(testCase.missing_fields ?? []);
  return {
    schema_version: "1.0",
    id: `contract:${testCase.id ?? "base"}`,
    objective: "Produce the requested artifact without authority or scope drift.",
    mode: testCase.mode ?? "RUN",
    actor: {
      id: "operator:test",
      role: testCase.role ?? "OWNER",
      declared_expertise: "ADVANCED",
    },
    constraints: {
      allowed_scope: testCase.allowed_scope ?? ["artifact:*", "task:*", "audit:*", "external:*", "config:*", "system:*"],
      protected_scope: testCase.protected_scope ?? [],
      allow_external: testCase.allow_external ?? true,
      max_interruptions: testCase.max_interruptions ?? 2,
    },
    required_outcomes: [{ id: "O1", statement: "Requested outcome exists and is verified.", required: true }],
    material_fields: [
      { name: "destination", present: !missing.has("destination"), prompt: "Provide destination." },
      { name: "format", present: !missing.has("format"), prompt: "Provide output format." },
    ],
  };
}

function scenarioFromCase(testCase) {
  const contract = baseContract(testCase);
  return {
    id: testCase.id,
    contract,
    action: { id: `action:${testCase.id}`, ...testCase.action },
    context: {
      system_state: testCase.state,
      recoverable: testCase.recoverable,
      interruptions_used: testCase.interruptions_used ?? 0,
    },
    presentation: testCase.presentation,
  };
}

const fixtureCases = JSON.parse(await readFile(new URL("../fixtures/scenario-cases.json", import.meta.url), "utf8"));

for (const testCase of fixtureCases) {
  test(`fixture: ${testCase.id}`, () => {
    const result = evaluateScenario(scenarioFromCase(testCase));
    assert.equal(result.decision.status, testCase.expected_status);
    assert.ok(result.decision.reason_codes.includes(testCase.expected_reason));
    if (testCase.expected_question_count !== undefined) {
      assert.equal(result.decision.questions.length, testCase.expected_question_count);
    }
    if (testCase.expected_presentation !== undefined) {
      assert.equal(result.presentation?.status, testCase.expected_presentation);
      assert.ok(result.presentation?.violations.includes(testCase.expected_presentation_violation));
    }
  });
}

test("canonical hashing is independent of object key insertion order", () => {
  const a = { z: 1, nested: { b: 2, a: 3 }, list: [3, 2, 1] };
  const b = { list: [3, 2, 1], nested: { a: 3, b: 2 }, z: 1 };
  assert.equal(sha256Canonical(a), sha256Canonical(b));
});

test("irreversible action is allowed only with exact explicit OWNER-bound consent", () => {
  const contract = baseContract({ id: "consent-pass", role: "OWNER", mode: "FORGE" });
  const action = {
    id: "action:irreversible",
    kind: "MUTATE_IRREVERSIBLE",
    target_scope: "artifact:alpha",
    risk: "CRITICAL",
    reversibility: "IRREVERSIBLE",
    supports_outcomes: ["O1"],
    external: false,
  };
  const scenario = {
    id: "consent-pass",
    contract,
    action,
    context: { system_state: "READY", interruptions_used: 0 },
    consent: {
      contract_hash: sha256Canonical(contract),
      action_hash: sha256Canonical(action),
      granted_by_role: "OWNER",
      explicit: true,
    },
  };
  assert.equal(evaluateAction(scenario).status, "ALLOW");
});

test("stale or mismatched irreversible consent freezes", () => {
  const contract = baseContract({ id: "consent-mismatch", role: "OWNER", mode: "FORGE" });
  const action = {
    id: "action:irreversible",
    kind: "MUTATE_IRREVERSIBLE",
    target_scope: "artifact:alpha",
    risk: "CRITICAL",
    reversibility: "IRREVERSIBLE",
    supports_outcomes: ["O1"],
    external: false,
  };
  const decision = evaluateAction({
    id: "consent-mismatch",
    contract,
    action,
    context: { system_state: "READY", interruptions_used: 0 },
    consent: {
      contract_hash: "0".repeat(64),
      action_hash: sha256Canonical(action),
      granted_by_role: "OWNER",
      explicit: true,
    },
  });
  assert.equal(decision.status, "FREEZE");
  assert.ok(decision.reason_codes.includes("CONSENT_CONTRACT_MISMATCH"));
});

test("acceptance requires every required PASS to carry evidence", () => {
  const contract = baseContract({ id: "acceptance" });
  const verified = evaluateAcceptance(contract, [{ id: "O1", status: "PASS", evidence_refs: ["E2:test:1"] }]);
  assert.equal(verified.status, "PASS");

  const noEvidence = evaluateAcceptance(contract, [{ id: "O1", status: "PASS", evidence_refs: [] }]);
  assert.equal(noEvidence.status, "NOT_VERIFIED");
  assert.deepEqual(noEvidence.evidence_missing, ["O1"]);

  const failed = evaluateAcceptance(contract, [{ id: "O1", status: "FAIL", evidence_refs: ["E2:test:2"] }]);
  assert.equal(failed.status, "FAIL");
});

test("disclosure never hides freeze from OWNER and does not expose owner controls to AUDITOR", () => {
  const ownerPlan = computeDisclosure(baseContract({ id: "owner", role: "OWNER" }), "FREEZE");
  assert.ok(ownerPlan.mandatory_notices.includes("FREEZE_BANNER"));
  assert.ok(ownerPlan.controls.includes("RECOVER"));

  const auditorPlan = computeDisclosure(baseContract({ id: "auditor", role: "AUDITOR", mode: "VIEW" }), "READY");
  assert.ok(auditorPlan.panels.includes("AUDIT"));
  assert.ok(!auditorPlan.controls.includes("CONFIG"));
  assert.ok(!auditorPlan.controls.includes("RECOVER"));
});

test("trace evaluator detects unnecessary, repeated, and over-budget interruptions", () => {
  const trace = evaluateTrace(
    [
      { seq: 1, kind: "ASK_USER" },
      { seq: 2, kind: "ASK_USER", material_blocker: "target" },
      { seq: 3, kind: "ASK_USER", material_blocker: "target" },
    ],
    2,
  );
  assert.equal(trace.status, "FAIL");
  assert.ok(trace.violations.includes("UNNECESSARY_INTERRUPTION:1"));
  assert.ok(trace.violations.includes("REPEATED_INTERRUPTION:3"));
  assert.ok(trace.violations.includes("INTERRUPTION_BUDGET_EXCEEDED"));
});

test("trace evaluator rejects success presentation after freeze presentation", () => {
  const trace = evaluateTrace(
    [
      { seq: 1, kind: "FREEZE_SHOWN" },
      { seq: 2, kind: "SUCCESS_SHOWN" },
    ],
    1,
  );
  assert.equal(trace.status, "FAIL");
  assert.ok(trace.violations.includes("SUCCESS_AFTER_FREEZE:2"));
});
