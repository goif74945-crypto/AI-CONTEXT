/**
 * NEXY AgentAdapter preflight mirror for TypeScript hosts.
 *
 * AI-PROPOSED standalone lab contract. This file is intentionally dependency-free
 * so it can be evaluated before any explicit integration into the NEXY.AI codebase.
 */

export type NexyMode = "fast" | "strict" | "audit";
export type HealthState = "HEALTHY" | "DEGRADED" | "UNHEALTHY";
export type SimulationEvent =
  | "result_valid"
  | "result_schema_invalid"
  | "timeout"
  | "provider_failure";

export interface AgentAdapterManifest {
  schema_version: "1.0";
  adapter: {
    id: string;
    provider: string;
    version: string;
    supported_modes: NexyMode[];
    deterministic_capable: boolean;
    critical: boolean;
    timeout_ms: number;
    context_capacity: number;
    operations: string[];
  };
  authority: {
    candidate_only: true;
    direct_release: false;
    direct_vault_write: false;
    mutates_core_state: false;
    automatic_retry: false;
  };
  security: {
    secret_delivery: "runtime_injection";
    persists_secrets: false;
  };
}

export interface ValidationIssue {
  code: string;
  path: string;
  classification: "SOURCE_FACT" | "PROPOSED_GUARD";
  message: string;
}

export interface ValidationResult {
  status: "PASS" | "FAIL";
  issues: ValidationIssue[];
  scope_statement: string;
}

export interface SimulationResult {
  status: "PASS" | "FAIL";
  action:
    | "CONTINUE_TO_CROSS_VERIFY"
    | "FREEZE"
    | "FREEZE_PRE_EXEC"
    | "EXCLUDE_AGENT_AND_CONTINUE";
  reason_code: string;
  limitation: string;
}

const supportedModes = new Set<NexyMode>(["fast", "strict", "audit"]);
const requiredOperations = new Set(["execute", "cancel", "healthcheck"]);
const idPattern = /^[a-z0-9][a-z0-9._-]{2,63}$/;
const semverPattern = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;

function issue(
  code: string,
  path: string,
  classification: ValidationIssue["classification"],
  message: string,
): ValidationIssue {
  return { code, path, classification, message };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function validateAdapterManifest(input: unknown): ValidationResult {
  const issues: ValidationIssue[] = [];
  if (!isRecord(input)) {
    return {
      status: "FAIL",
      issues: [issue("LAB.SCHEMA_VERSION", "$", "PROPOSED_GUARD", "Manifest must be an object.")],
      scope_statement: scopeStatement,
    };
  }

  if (input.schema_version !== "1.0") {
    issues.push(issue("LAB.SCHEMA_VERSION", "$.schema_version", "PROPOSED_GUARD", "schema_version must equal '1.0'."));
  }

  const adapter = input.adapter;
  if (!isRecord(adapter)) {
    issues.push(issue("LAB.ADAPTER_OBJECT", "$.adapter", "PROPOSED_GUARD", "adapter must be an object."));
    return finalize(issues);
  }

  if (typeof adapter.id !== "string" || !idPattern.test(adapter.id)) {
    issues.push(issue("LAB.ADAPTER_ID", "$.adapter.id", "PROPOSED_GUARD", "Invalid adapter id."));
  }
  if (typeof adapter.provider !== "string" || adapter.provider.trim().length === 0) {
    issues.push(issue("LAB.PROVIDER", "$.adapter.provider", "PROPOSED_GUARD", "provider must be non-empty."));
  }
  if (typeof adapter.version !== "string" || !semverPattern.test(adapter.version)) {
    issues.push(issue("LAB.ADAPTER_VERSION", "$.adapter.version", "PROPOSED_GUARD", "version must be valid SemVer."));
  }

  if (!Array.isArray(adapter.supported_modes) || adapter.supported_modes.length === 0) {
    issues.push(issue("DOC-C.AGENT_SUPPORTED_MODES", "$.adapter.supported_modes", "SOURCE_FACT", "supported_modes must be non-empty."));
  } else {
    const modes = adapter.supported_modes;
    const modeSet = new Set(modes);
    if (modeSet.size !== modes.length) {
      issues.push(issue("LAB.DUPLICATE_MODE", "$.adapter.supported_modes", "PROPOSED_GUARD", "supported_modes must be unique."));
    }
    for (const mode of modes) {
      if (typeof mode !== "string" || !supportedModes.has(mode as NexyMode)) {
        issues.push(issue("DOC-C.AGENT_SUPPORTED_MODES", "$.adapter.supported_modes", "SOURCE_FACT", `Unsupported mode: ${String(mode)}.`));
      }
    }
  }

  if (typeof adapter.deterministic_capable !== "boolean") {
    issues.push(issue("DOC-C.DETERMINISTIC_CAPABILITY_DECLARED", "$.adapter.deterministic_capable", "SOURCE_FACT", "deterministic_capable must be boolean."));
  }
  if (typeof adapter.critical !== "boolean") {
    issues.push(issue("DOC-C.CRITICAL_FLAG_DECLARED", "$.adapter.critical", "SOURCE_FACT", "critical must be boolean."));
  }
  if (!Number.isInteger(adapter.timeout_ms) || (adapter.timeout_ms as number) < 10_000 || (adapter.timeout_ms as number) > 60_000) {
    issues.push(issue("DOC-C.AGENT_TIMEOUT_RANGE", "$.adapter.timeout_ms", "SOURCE_FACT", "timeout_ms must be an integer in [10000, 60000]."));
  } else if (adapter.critical === true && adapter.timeout_ms !== 30_000) {
    issues.push(issue("DOC-C.CRITICAL_AGENT_TIMEOUT", "$.adapter.timeout_ms", "SOURCE_FACT", "critical timeout must be 30000 ms."));
  }
  if (!Number.isInteger(adapter.context_capacity) || (adapter.context_capacity as number) <= 0) {
    issues.push(issue("DOC-C.CONTEXT_CAPACITY_DECLARED", "$.adapter.context_capacity", "SOURCE_FACT", "context_capacity must be positive."));
  }
  if (!Array.isArray(adapter.operations) || adapter.operations.some((op) => typeof op !== "string")) {
    issues.push(issue("DOC-C.AGENT_ADAPTER_OPERATIONS", "$.adapter.operations", "SOURCE_FACT", "operations must be a string array."));
  } else {
    const ops = new Set(adapter.operations);
    for (const required of requiredOperations) {
      if (!ops.has(required)) {
        issues.push(issue("DOC-C.AGENT_ADAPTER_OPERATIONS", "$.adapter.operations", "SOURCE_FACT", `Missing operation: ${required}.`));
      }
    }
  }

  const authority = input.authority;
  if (!isRecord(authority)) {
    issues.push(issue("LAB.AUTHORITY_OBJECT", "$.authority", "PROPOSED_GUARD", "authority must be an object."));
  } else {
    exact(authority.candidate_only, true, "NEXY.CORE.WORKER_NOT_AUTHORITY", "$.authority.candidate_only", issues);
    exact(authority.direct_release, false, "NEXY.CORE.NO_WORKER_RELEASE", "$.authority.direct_release", issues);
    exact(authority.direct_vault_write, false, "DOC-C.DEPENDENCY.SWARM_TO_VAULT_FORBIDDEN", "$.authority.direct_vault_write", issues);
    exact(authority.mutates_core_state, false, "NEXY.CORE.NO_WORKER_AUTHORITY_ESCALATION", "$.authority.mutates_core_state", issues);
    exact(authority.automatic_retry, false, "DOC-C.PIPELINE.NO_AUTOMATIC_RETRY", "$.authority.automatic_retry", issues);
  }

  const security = input.security;
  if (!isRecord(security)) {
    issues.push(issue("LAB.SECURITY_OBJECT", "$.security", "PROPOSED_GUARD", "security must be an object."));
  } else {
    if (security.secret_delivery !== "runtime_injection") {
      issues.push(issue("NEXY.SECURITY.SERVER_SIDE_RUNTIME_SECRETS", "$.security.secret_delivery", "SOURCE_FACT", "Secrets must use runtime_injection."));
    }
    exact(security.persists_secrets, false, "NEXY.SECURITY.NO_SECRET_PERSISTENCE", "$.security.persists_secrets", issues);
  }

  return finalize(issues);
}

export function simulateAdapterEvent(
  manifest: unknown,
  event: SimulationEvent,
  quorumPossibleAfterExclusion: boolean | null = null,
): SimulationResult {
  const validation = validateAdapterManifest(manifest);
  if (validation.status !== "PASS") {
    return result("FAIL", "FREEZE_PRE_EXEC", "ADAPTER_CONTRACT_INVALID");
  }

  const critical = (manifest as AgentAdapterManifest).adapter.critical;
  if (event === "result_valid") {
    return result("PASS", "CONTINUE_TO_CROSS_VERIFY", "CANDIDATE_RESULT_VALID");
  }
  if (event === "result_schema_invalid") {
    return result("PASS", "FREEZE", "AGENT_SCHEMA_INVALID");
  }
  if (event === "provider_failure") {
    return result("PASS", "FREEZE", "DEPENDENCY_FAILURE");
  }
  if (critical) {
    return result("PASS", "FREEZE", "AGENT_TIMEOUT_CRITICAL");
  }
  if (quorumPossibleAfterExclusion === true) {
    return result("PASS", "EXCLUDE_AGENT_AND_CONTINUE", "AGENT_TIMEOUT_NONCRITICAL_QUORUM_REMAINS");
  }
  if (quorumPossibleAfterExclusion === false) {
    return result("PASS", "FREEZE", "CONSENSUS_QUORUM_WOULD_FAIL");
  }
  return result("PASS", "FREEZE", "QUORUM_STATUS_UNKNOWN_ZERO_GUESS");
}

const scopeStatement = "Standalone preflight only; PASS is not proof of NEXY.AI runtime integration or deployment.";
const limitation = "Deterministic lab simulation only; not E3/E5 evidence from the real NEXY.AI runtime.";

function finalize(issues: ValidationIssue[]): ValidationResult {
  issues.sort((a, b) => `${a.code}\0${a.path}\0${a.message}`.localeCompare(`${b.code}\0${b.path}\0${b.message}`));
  return { status: issues.length === 0 ? "PASS" : "FAIL", issues, scope_statement: scopeStatement };
}

function exact(value: unknown, expected: boolean, code: string, path: string, issues: ValidationIssue[]): void {
  if (typeof value !== "boolean" || value !== expected) {
    issues.push(issue(code, path, "SOURCE_FACT", `${path.split(".").at(-1)} must be ${String(expected)}.`));
  }
}

function result(status: "PASS" | "FAIL", action: SimulationResult["action"], reason_code: string): SimulationResult {
  return { status, action, reason_code, limitation };
}
