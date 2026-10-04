import assert from "node:assert/strict";
import test from "node:test";
import { compileOperatorExperience, OxcContractError } from "../dist/index.js";

function baseInput() {
  return {
    core: {
      schemaVersion: "1.0",
      systemState: "READY",
      truthStatus: "VERIFIED",
      role: "OWNER",
      mode: "RUN",
      blockingReasons: [],
      actions: [
        {
          id: "inspect",
          label: "Inspect",
          kind: "INSPECT",
          backendAllowed: true,
          allowedRoles: ["OWNER", "OPERATOR", "AUDITOR", "VIEWER"],
          allowedSystemStates: ["READY", "RUNNING", "VERIFYING", "CONSENSUS", "STABLE", "FREEZE", "STOP"],
          requiresVerifiedTruth: false,
          risk: "LOW",
          reversibility: "REVERSIBLE",
          minimumFriction: "NONE",
          visibilityPolicy: "SHOW_DISABLED",
        },
        {
          id: "mutate",
          label: "Apply change",
          kind: "MUTATE",
          backendAllowed: true,
          allowedRoles: ["OWNER", "OPERATOR"],
          allowedSystemStates: ["READY", "STABLE"],
          requiresVerifiedTruth: true,
          risk: "HIGH",
          reversibility: "REVERSIBLE_WITH_COST",
          minimumFriction: "ACK",
          visibilityPolicy: "SHOW_DISABLED",
        },
        {
          id: "recover",
          label: "Recover",
          kind: "RECOVERY",
          backendAllowed: true,
          allowedRoles: ["OWNER"],
          allowedSystemStates: ["FREEZE"],
          requiresVerifiedTruth: false,
          risk: "HIGH",
          reversibility: "REVERSIBLE_WITH_COST",
          minimumFriction: "CONFIRM",
          visibilityPolicy: "HIDE_WHEN_DENIED",
        },
      ],
    },
    preferences: {
      detail: "BALANCED",
      density: "MEDIUM",
      language: "th-TH",
      motion: "REDUCED",
      friendlyTone: false,
    },
  };
}

function authorizationProjection(plan) {
  return plan.actions.map(({ id, state, reasons, friction }) => ({ id, state, reasons, friction }));
}

test("identical inputs produce structurally identical outputs", () => {
  const input = baseInput();
  const before = structuredClone(input);
  const first = compileOperatorExperience(input);
  const second = compileOperatorExperience(structuredClone(input));
  assert.deepEqual(first, second);
  assert.deepEqual(input, before, "compiler must not mutate caller input");
});

test("presentation preferences cannot change action authorization, reasons, or friction", () => {
  const compact = baseInput();
  compact.preferences = {
    detail: "COMPACT",
    density: "LOW",
    language: "en-US",
    motion: "STANDARD",
    friendlyTone: true,
  };

  const deep = baseInput();
  deep.preferences = {
    detail: "DEEP",
    density: "HIGH",
    language: "ja-JP",
    motion: "REDUCED",
    friendlyTone: false,
  };

  assert.deepEqual(
    authorizationProjection(compileOperatorExperience(compact)),
    authorizationProjection(compileOperatorExperience(deep)),
  );
});

test("FREEZE is mandatory, visible, diagnostic, and blocks ordinary mutation", () => {
  const input = baseInput();
  input.core.systemState = "FREEZE";
  input.core.truthStatus = "BLOCKED";
  input.core.blockingReasons = ["verification failed"];
  const plan = compileOperatorExperience(input);

  assert.equal(plan.truthBanner.severity, "BLOCKING");
  assert.equal(plan.truthBanner.code, "SYSTEM_FREEZE");
  assert(plan.mandatorySignals.includes("FREEZE_BANNER"));
  assert.equal(plan.disclosure, "DIAGNOSTIC");
  assert.equal(plan.actions.find((action) => action.id === "mutate")?.state, "DISABLED");
  assert.equal(plan.actions.find((action) => action.id === "recover")?.state, "ENABLED");
});

test("non-owner cannot gain recovery authority and hidden denial remains non-executable", () => {
  const input = baseInput();
  input.core.systemState = "FREEZE";
  input.core.role = "OPERATOR";
  const plan = compileOperatorExperience(input);
  const recovery = plan.actions.find((action) => action.id === "recover");

  assert.equal(recovery?.state, "HIDDEN");
  assert.deepEqual(recovery?.reasons, ["ROLE_DENIED"]);
  assert.equal(recovery?.friction, "NONE");
});

test("backend denial always fails closed", () => {
  const input = baseInput();
  input.core.actions[1].backendAllowed = false;
  const action = compileOperatorExperience(input).actions.find((entry) => entry.id === "mutate");
  assert.equal(action?.state, "DISABLED");
  assert(action?.reasons.includes("BACKEND_DENIED"));
});

test("VIEW mode cannot enable mutation even when backend and role permit it", () => {
  const input = baseInput();
  input.core.mode = "VIEW";
  const action = compileOperatorExperience(input).actions.find((entry) => entry.id === "mutate");
  assert.equal(action?.state, "DISABLED");
  assert(action?.reasons.includes("VIEW_MODE_READ_ONLY"));
});

test("verified-truth requirement blocks action under UNKNOWN truth", () => {
  const input = baseInput();
  input.core.truthStatus = "UNKNOWN";
  const action = compileOperatorExperience(input).actions.find((entry) => entry.id === "mutate");
  assert.equal(action?.state, "DISABLED");
  assert(action?.reasons.includes("VERIFIED_TRUTH_REQUIRED"));
});

test("critical irreversible action requires double confirmation", () => {
  const input = baseInput();
  input.core.actions.push({
    id: "destroy",
    label: "Destroy",
    kind: "MUTATE",
    backendAllowed: true,
    allowedRoles: ["OWNER"],
    allowedSystemStates: ["READY"],
    requiresVerifiedTruth: true,
    risk: "CRITICAL",
    reversibility: "IRREVERSIBLE",
    minimumFriction: "NONE",
    visibilityPolicy: "SHOW_DISABLED",
  });
  const plan = compileOperatorExperience(input);
  const action = plan.actions.find((entry) => entry.id === "destroy");
  assert.equal(action?.state, "ENABLED");
  assert.equal(action?.friction, "DOUBLE_CONFIRM");
  assert.equal(plan.disclosure, "DIAGNOSTIC");
});

test("STOP fails closed for mutation and recovery", () => {
  const input = baseInput();
  input.core.systemState = "STOP";
  input.core.actions[2].allowedSystemStates = ["STOP"];
  const plan = compileOperatorExperience(input);
  const mutation = plan.actions.find((entry) => entry.id === "mutate");
  const recovery = plan.actions.find((entry) => entry.id === "recover");
  assert.equal(mutation?.state, "DISABLED");
  assert.equal(recovery?.state, "HIDDEN");
  assert(recovery?.reasons.includes("SYSTEM_STOPPED"));
});

test("duplicate action ids are rejected at the contract boundary", () => {
  const input = baseInput();
  input.core.actions.push(structuredClone(input.core.actions[0]));
  assert.throws(() => compileOperatorExperience(input), OxcContractError);
});

test("unsupported role fails closed rather than being inferred", () => {
  const input = baseInput();
  input.core.role = "SUPERADMIN";
  assert.throws(() => compileOperatorExperience(input), /core\.role is unsupported/);
});

test("empty allowedSystemStates is rejected", () => {
  const input = baseInput();
  input.core.actions[0].allowedSystemStates = [];
  assert.throws(() => compileOperatorExperience(input), /allowedSystemStates must be a non-empty array/);
});

test("unknown friction values are rejected", () => {
  const input = baseInput();
  input.core.actions[0].minimumFriction = "TRIPLE_CONFIRM";
  assert.throws(() => compileOperatorExperience(input), /minimumFriction is unsupported/);
});

test("exhaustive policy matrix never promotes a backend-denied mutation", () => {
  const roles = ["OWNER", "OPERATOR", "AUDITOR", "VIEWER"];
  const modes = ["VIEW", "RUN", "FORGE"];
  const states = ["INIT", "READY", "RUNNING", "VERIFYING", "CONSENSUS", "STABLE", "FREEZE", "STOP"];
  const truths = ["VERIFIED", "PARTIAL", "UNKNOWN", "CONFLICT", "NOT_VERIFIED", "BLOCKED"];
  let cases = 0;

  for (const role of roles) {
    for (const mode of modes) {
      for (const systemState of states) {
        for (const truthStatus of truths) {
          const input = baseInput();
          input.core.role = role;
          input.core.mode = mode;
          input.core.systemState = systemState;
          input.core.truthStatus = truthStatus;
          input.core.actions[1].backendAllowed = false;
          input.core.actions[1].allowedRoles = roles;
          input.core.actions[1].allowedSystemStates = states;
          input.core.actions[1].requiresVerifiedTruth = false;
          const action = compileOperatorExperience(input).actions.find((entry) => entry.id === "mutate");
          assert.notEqual(action?.state, "ENABLED");
          assert(action?.reasons.includes("BACKEND_DENIED"));
          cases += 1;
        }
      }
    }
  }

  assert.equal(cases, 576);
});

test("all presentation preference combinations preserve authorization projection", () => {
  const details = ["COMPACT", "BALANCED", "DEEP"];
  const densities = ["LOW", "MEDIUM", "HIGH"];
  const motions = ["REDUCED", "STANDARD"];
  const tones = [false, true];
  const baseline = authorizationProjection(compileOperatorExperience(baseInput()));
  let cases = 0;

  for (const detail of details) {
    for (const density of densities) {
      for (const motion of motions) {
        for (const friendlyTone of tones) {
          const input = baseInput();
          input.preferences = { detail, density, language: "th-TH", motion, friendlyTone };
          assert.deepEqual(authorizationProjection(compileOperatorExperience(input)), baseline);
          cases += 1;
        }
      }
    }
  }

  assert.equal(cases, 36);
});
