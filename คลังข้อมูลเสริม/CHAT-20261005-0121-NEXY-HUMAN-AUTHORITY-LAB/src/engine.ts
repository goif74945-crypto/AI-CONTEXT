import { sha256Canonical } from "./canonical.js";
import type {
  AcceptanceEvaluation,
  ActionDecision,
  ActionKind,
  ActionRequest,
  CriterionResult,
  DisclosurePlan,
  IntentContract,
  PresentationEvaluation,
  Role,
  Scenario,
  ScenarioEvaluation,
  SystemState,
  TraceEvaluation,
  TraceEvent,
} from "./types.js";

const OWNER_ONLY = new Set<ActionKind>(["CONFIG", "RECOVER", "MUTATE_IRREVERSIBLE"]);
const HUMAN_MUTATORS = new Set<Role>(["OWNER", "OPERATOR"]);

function isNonEmpty(value: string): boolean {
  return value.trim().length > 0;
}

function matchesScope(pattern: string, target: string): boolean {
  if (pattern === target) return true;
  if (pattern.endsWith(":*")) return target.startsWith(pattern.slice(0, -1));
  return false;
}

function scopeMatchesAny(patterns: readonly string[], target: string): boolean {
  return patterns.some((pattern) => matchesScope(pattern, target));
}

function roleAllows(role: Role, action: ActionRequest): boolean {
  if (action.required_role) return role === action.required_role || role === "SYSTEM";
  if (OWNER_ONLY.has(action.kind)) return role === "OWNER" || role === "SYSTEM";
  if (action.kind === "SUBMIT_DIRECTIVE" || action.kind === "MUTATE_REVERSIBLE" || action.kind === "EXTERNAL_IO") {
    return HUMAN_MUTATORS.has(role) || role === "SYSTEM";
  }
  if (action.kind === "EXPORT") return role === "OWNER" || role === "OPERATOR" || role === "AUDITOR" || role === "SYSTEM";
  return true;
}

function validateContract(contract: IntentContract): string[] {
  const issues: string[] = [];
  if (contract.schema_version !== "1.0") issues.push("UNSUPPORTED_SCHEMA_VERSION");
  if (!isNonEmpty(contract.id)) issues.push("CONTRACT_ID_REQUIRED");
  if (!isNonEmpty(contract.objective)) issues.push("OBJECTIVE_REQUIRED");
  if (!isNonEmpty(contract.actor.id)) issues.push("ACTOR_ID_REQUIRED");
  if (contract.constraints.allowed_scope.length === 0) issues.push("ALLOWED_SCOPE_REQUIRED");
  if (!Number.isInteger(contract.constraints.max_interruptions) || contract.constraints.max_interruptions < 0) {
    issues.push("INVALID_INTERRUPTION_BUDGET");
  }

  const outcomeIds = new Set<string>();
  for (const outcome of contract.required_outcomes) {
    if (!isNonEmpty(outcome.id) || !isNonEmpty(outcome.statement)) issues.push("INVALID_OUTCOME");
    if (outcomeIds.has(outcome.id)) issues.push("DUPLICATE_OUTCOME_ID");
    outcomeIds.add(outcome.id);
  }

  const fieldNames = new Set<string>();
  for (const field of contract.material_fields) {
    if (!isNonEmpty(field.name) || !isNonEmpty(field.prompt)) issues.push("INVALID_MATERIAL_FIELD");
    if (fieldNames.has(field.name)) issues.push("DUPLICATE_MATERIAL_FIELD");
    fieldNames.add(field.name);
  }

  return [...new Set(issues)].sort();
}

function makeDecision(
  status: ActionDecision["status"],
  reasonCodes: string[],
  questions: string[],
  contract: IntentContract,
  action: ActionRequest,
): ActionDecision {
  return {
    status,
    reason_codes: [...new Set(reasonCodes)].sort(),
    questions,
    contract_hash: sha256Canonical(contract),
    action_hash: sha256Canonical(action),
  };
}

function isObjectiveAligned(contract: IntentContract, action: ActionRequest): boolean {
  if (action.kind === "READ" || action.kind === "EXPORT") return true;
  const requiredIds = new Set(contract.required_outcomes.filter((item) => item.required).map((item) => item.id));
  if (requiredIds.size === 0) return action.supports_outcomes.length > 0;
  return action.supports_outcomes.some((id) => requiredIds.has(id));
}

function actionPermittedInState(state: SystemState, action: ActionRequest, recoverable: boolean | undefined): string | null {
  if (state === "STOP") return "SYSTEM_STOP";
  if (state === "FREEZE") {
    if (action.kind !== "RECOVER") return "SYSTEM_FROZEN";
    if (!recoverable) return "RECOVERY_NOT_ALLOWED";
  }
  return null;
}

function materialQuestions(contract: IntentContract): string[] {
  const prompts = contract.material_fields.filter((field) => !field.present).map((field) => field.prompt.trim());
  if (prompts.length === 0) return [];
  return [`Required before execution: ${prompts.join(" | ")}`];
}

export function evaluateAction(scenario: Scenario): ActionDecision {
  const { contract, action, context, consent } = scenario;
  const contractIssues = validateContract(contract);
  if (contractIssues.length > 0) return makeDecision("FREEZE", contractIssues, [], contract, action);

  const stateBlock = actionPermittedInState(context.system_state, action, context.recoverable);
  if (stateBlock) return makeDecision("FREEZE", [stateBlock], [], contract, action);

  if (!roleAllows(contract.actor.role, action)) {
    return makeDecision("FREEZE", ["PERMISSION_DENIED"], [], contract, action);
  }

  if (scopeMatchesAny(contract.constraints.protected_scope, action.target_scope)) {
    return makeDecision("FREEZE", ["PROTECTED_SCOPE"], [], contract, action);
  }

  if (!scopeMatchesAny(contract.constraints.allowed_scope, action.target_scope)) {
    return makeDecision("FREEZE", ["OUT_OF_SCOPE"], [], contract, action);
  }

  if (action.external && !contract.constraints.allow_external) {
    return makeDecision("FREEZE", ["EXTERNAL_IO_NOT_AUTHORIZED"], [], contract, action);
  }

  if (!isObjectiveAligned(contract, action)) {
    return makeDecision("FREEZE", ["OBJECTIVE_DRIFT"], [], contract, action);
  }

  const questions = materialQuestions(contract);
  if (questions.length > 0) {
    if (context.interruptions_used >= contract.constraints.max_interruptions) {
      return makeDecision("FREEZE", ["MATERIAL_UNKNOWN_INTERRUPTION_BUDGET_EXHAUSTED"], [], contract, action);
    }
    return makeDecision("ASK", ["MATERIAL_INFORMATION_REQUIRED"], questions, contract, action);
  }

  if (action.reversibility === "IRREVERSIBLE" || action.kind === "MUTATE_IRREVERSIBLE") {
    if (!consent) {
      if (context.interruptions_used >= contract.constraints.max_interruptions) {
        return makeDecision("FREEZE", ["IRREVERSIBLE_CONSENT_MISSING"], [], contract, action);
      }
      return makeDecision("ASK", ["IRREVERSIBLE_CONSENT_REQUIRED"], ["Explicit OWNER consent is required for this exact irreversible action."], contract, action);
    }

    const expectedContractHash = sha256Canonical(contract);
    const expectedActionHash = sha256Canonical(action);
    const consentIssues: string[] = [];
    if (!consent.explicit) consentIssues.push("CONSENT_NOT_EXPLICIT");
    if (consent.granted_by_role !== "OWNER" && consent.granted_by_role !== "SYSTEM") consentIssues.push("CONSENT_AUTHORITY_INVALID");
    if (consent.contract_hash !== expectedContractHash) consentIssues.push("CONSENT_CONTRACT_MISMATCH");
    if (consent.action_hash !== expectedActionHash) consentIssues.push("CONSENT_ACTION_MISMATCH");
    if (consentIssues.length > 0) return makeDecision("FREEZE", consentIssues, [], contract, action);
  }

  return makeDecision("ALLOW", ["CONTRACT_CONFORMANT"], [], contract, action);
}

export function computeDisclosure(contract: IntentContract, state: SystemState): DisclosurePlan {
  const panels = new Set<string>(["STATUS", "TASK"]);
  const controls = new Set<string>();
  const notices = new Set<string>();

  if (contract.mode === "VIEW") panels.add("RESULT");
  if (contract.mode === "RUN") panels.add("PIPELINE");
  if (contract.mode === "FORGE") panels.add("ARTIFACT_BUILDER");

  if (contract.actor.role === "AUDITOR" || contract.actor.role === "OWNER") panels.add("AUDIT");
  if (contract.actor.role === "OWNER") panels.add("OWNER_CONTROL");

  if (state === "FREEZE") {
    panels.add("INCIDENT");
    notices.add("FREEZE_BANNER");
    if (contract.actor.role === "OWNER") controls.add("RECOVER");
  } else if (state !== "STOP") {
    if ((contract.actor.role === "OWNER" || contract.actor.role === "OPERATOR") && contract.mode === "RUN") controls.add("SUBMIT_DIRECTIVE");
    if ((contract.actor.role === "OWNER" || contract.actor.role === "OPERATOR") && contract.mode === "FORGE") controls.add("BUILD_ARTIFACT");
  }

  if (contract.actor.role === "OWNER" && state !== "STOP") controls.add("CONFIG");
  if (contract.actor.role === "OWNER" || contract.actor.role === "OPERATOR" || contract.actor.role === "AUDITOR") controls.add("EXPORT");
  if (state === "STOP") notices.add("STOP_BANNER");

  return {
    panels: [...panels].sort(),
    controls: [...controls].sort(),
    mandatory_notices: [...notices].sort(),
  };
}

export function evaluatePresentation(scenario: Scenario, decision: ActionDecision): PresentationEvaluation | null {
  if (!scenario.presentation) return null;
  const violations: string[] = [];
  const presentation = scenario.presentation;
  const disclosure = computeDisclosure(scenario.contract, scenario.context.system_state);

  if (scenario.context.system_state === "FREEZE" && !presentation.freeze_visible) violations.push("FREEZE_MASKED");
  if (decision.status !== "ALLOW" && presentation.reported_success) violations.push("FALSE_SUCCESS");

  const allowedControls = new Set(disclosure.controls);
  for (const control of presentation.visible_controls) {
    if (!allowedControls.has(control)) violations.push(`UNAUTHORIZED_CONTROL_VISIBLE:${control}`);
  }

  return {
    status: violations.length === 0 ? "PASS" : "FAIL",
    violations: violations.sort(),
  };
}

export function evaluateAcceptance(contract: IntentContract, results: CriterionResult[]): AcceptanceEvaluation {
  const byId = new Map(results.map((item) => [item.id, item]));
  const missingRequired: string[] = [];
  const failedRequired: string[] = [];
  const evidenceMissing: string[] = [];

  for (const criterion of contract.required_outcomes) {
    if (!criterion.required) continue;
    const result = byId.get(criterion.id);
    if (!result || result.status === "NOT_VERIFIED") {
      missingRequired.push(criterion.id);
      continue;
    }
    if (result.status === "FAIL") failedRequired.push(criterion.id);
    if (result.status === "PASS" && result.evidence_refs.length === 0) evidenceMissing.push(criterion.id);
  }

  let status: AcceptanceEvaluation["status"] = "PASS";
  if (failedRequired.length > 0) status = "FAIL";
  else if (missingRequired.length > 0 || evidenceMissing.length > 0) status = "NOT_VERIFIED";

  return {
    status,
    missing_required: missingRequired.sort(),
    failed_required: failedRequired.sort(),
    evidence_missing: evidenceMissing.sort(),
  };
}

export function evaluateTrace(events: TraceEvent[], maxInterruptions: number): TraceEvaluation {
  const sorted = [...events].sort((a, b) => a.seq - b.seq);
  const violations: string[] = [];
  let interruptionCount = 0;
  let previousAskBlocker: string | undefined;
  let freezeShown = false;

  for (const event of sorted) {
    if (event.kind === "ASK_USER") {
      interruptionCount += 1;
      if (!event.material_blocker) violations.push(`UNNECESSARY_INTERRUPTION:${event.seq}`);
      if (event.material_blocker && event.material_blocker === previousAskBlocker) violations.push(`REPEATED_INTERRUPTION:${event.seq}`);
      previousAskBlocker = event.material_blocker;
    }
    if (event.kind === "FREEZE_SHOWN") freezeShown = true;
    if (event.kind === "SUCCESS_SHOWN" && freezeShown) violations.push(`SUCCESS_AFTER_FREEZE:${event.seq}`);
  }

  if (interruptionCount > maxInterruptions) violations.push("INTERRUPTION_BUDGET_EXCEEDED");
  return {
    status: violations.length === 0 ? "PASS" : "FAIL",
    violations: violations.sort(),
    interruption_count: interruptionCount,
  };
}

export function evaluateScenario(scenario: Scenario): ScenarioEvaluation {
  const decision = evaluateAction(scenario);
  return {
    scenario_id: scenario.id,
    decision,
    presentation: evaluatePresentation(scenario, decision),
  };
}
