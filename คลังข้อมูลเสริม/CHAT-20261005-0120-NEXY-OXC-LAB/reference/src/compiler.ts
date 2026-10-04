import {
  ACTION_KINDS,
  DETAIL_PREFERENCES,
  DENSITIES,
  FRICTION_LEVELS,
  MODES,
  MOTION_PREFERENCES,
  REVERSIBILITY,
  RISKS,
  ROLES,
  SYSTEM_STATES,
  TRUTH_STATUSES,
  VISIBILITY_POLICIES,
  type ActionDescriptor,
  type CompileInput,
  type DisclosureLevel,
  type FrictionLevel,
  type PlannedAction,
  type PreferenceEnvelope,
  type SurfacePlan,
  type TruthBanner,
} from "./model.js";

export class OxcContractError extends Error {
  readonly code = "INVALID_INPUT" as const;

  constructor(message: string) {
    super(message);
    this.name = "OxcContractError";
  }
}

const FRICTION_RANK: Readonly<Record<FrictionLevel, number>> = Object.freeze({
  NONE: 0,
  ACK: 1,
  CONFIRM: 2,
  DOUBLE_CONFIRM: 3,
});

const FRICTION_BY_RANK = ["NONE", "ACK", "CONFIRM", "DOUBLE_CONFIRM"] as const;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isEnumValue<const T extends readonly string[]>(values: T, value: unknown): value is T[number] {
  return typeof value === "string" && (values as readonly string[]).includes(value);
}

function requireNonEmptyString(value: unknown, path: string): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new OxcContractError(`${path} must be a non-empty string`);
  }
  return value;
}

function requireBoolean(value: unknown, path: string): boolean {
  if (typeof value !== "boolean") {
    throw new OxcContractError(`${path} must be boolean`);
  }
  return value;
}

function requireStringArray(value: unknown, path: string): readonly string[] {
  if (!Array.isArray(value)) {
    throw new OxcContractError(`${path} must be an array`);
  }
  return value.map((entry, index) => requireNonEmptyString(entry, `${path}[${index}]`));
}

function requireEnumArray<const T extends readonly string[]>(
  value: unknown,
  values: T,
  path: string,
  allowEmpty = false,
): readonly T[number][] {
  if (!Array.isArray(value) || (!allowEmpty && value.length === 0)) {
    throw new OxcContractError(`${path} must be ${allowEmpty ? "an" : "a non-empty"} array`);
  }

  const result = value.map((entry, index) => {
    if (!isEnumValue(values, entry)) {
      throw new OxcContractError(`${path}[${index}] contains an unsupported value`);
    }
    return entry;
  });

  if (new Set(result).size !== result.length) {
    throw new OxcContractError(`${path} must not contain duplicates`);
  }

  return result;
}

function normalizeAction(value: unknown, index: number): ActionDescriptor {
  const path = `core.actions[${index}]`;
  if (!isRecord(value)) {
    throw new OxcContractError(`${path} must be an object`);
  }

  const kind = value.kind;
  const risk = value.risk;
  const reversibility = value.reversibility;
  const minimumFriction = value.minimumFriction;
  const visibilityPolicy = value.visibilityPolicy;

  if (!isEnumValue(ACTION_KINDS, kind)) throw new OxcContractError(`${path}.kind is unsupported`);
  if (!isEnumValue(RISKS, risk)) throw new OxcContractError(`${path}.risk is unsupported`);
  if (!isEnumValue(REVERSIBILITY, reversibility)) {
    throw new OxcContractError(`${path}.reversibility is unsupported`);
  }
  if (!isEnumValue(FRICTION_LEVELS, minimumFriction)) {
    throw new OxcContractError(`${path}.minimumFriction is unsupported`);
  }
  if (!isEnumValue(VISIBILITY_POLICIES, visibilityPolicy)) {
    throw new OxcContractError(`${path}.visibilityPolicy is unsupported`);
  }

  return Object.freeze({
    id: requireNonEmptyString(value.id, `${path}.id`),
    label: requireNonEmptyString(value.label, `${path}.label`),
    kind,
    backendAllowed: requireBoolean(value.backendAllowed, `${path}.backendAllowed`),
    allowedRoles: requireEnumArray(value.allowedRoles, ROLES, `${path}.allowedRoles`),
    allowedSystemStates: requireEnumArray(value.allowedSystemStates, SYSTEM_STATES, `${path}.allowedSystemStates`),
    requiresVerifiedTruth: requireBoolean(value.requiresVerifiedTruth, `${path}.requiresVerifiedTruth`),
    risk,
    reversibility,
    minimumFriction,
    visibilityPolicy,
  });
}

function normalizePreferences(value: unknown): PreferenceEnvelope {
  if (!isRecord(value)) throw new OxcContractError("preferences must be an object");

  if (!isEnumValue(DETAIL_PREFERENCES, value.detail)) {
    throw new OxcContractError("preferences.detail is unsupported");
  }
  if (!isEnumValue(DENSITIES, value.density)) {
    throw new OxcContractError("preferences.density is unsupported");
  }
  if (!isEnumValue(MOTION_PREFERENCES, value.motion)) {
    throw new OxcContractError("preferences.motion is unsupported");
  }

  return Object.freeze({
    detail: value.detail,
    density: value.density,
    language: requireNonEmptyString(value.language, "preferences.language"),
    motion: value.motion,
    friendlyTone: requireBoolean(value.friendlyTone, "preferences.friendlyTone"),
  });
}

function normalizeInput(value: unknown): CompileInput {
  if (!isRecord(value)) throw new OxcContractError("input must be an object");
  if (!isRecord(value.core)) throw new OxcContractError("core must be an object");

  const core = value.core;
  if (core.schemaVersion !== "1.0") throw new OxcContractError("core.schemaVersion must equal 1.0");
  if (!isEnumValue(SYSTEM_STATES, core.systemState)) {
    throw new OxcContractError("core.systemState is unsupported");
  }
  if (!isEnumValue(TRUTH_STATUSES, core.truthStatus)) {
    throw new OxcContractError("core.truthStatus is unsupported");
  }
  if (!isEnumValue(ROLES, core.role)) throw new OxcContractError("core.role is unsupported");
  if (!isEnumValue(MODES, core.mode)) throw new OxcContractError("core.mode is unsupported");
  if (!Array.isArray(core.actions)) throw new OxcContractError("core.actions must be an array");

  const actions = core.actions.map(normalizeAction);
  const ids = actions.map((action) => action.id);
  if (new Set(ids).size !== ids.length) {
    throw new OxcContractError("core.actions contains duplicate action ids");
  }

  return Object.freeze({
    core: Object.freeze({
      schemaVersion: "1.0" as const,
      systemState: core.systemState,
      truthStatus: core.truthStatus,
      role: core.role,
      mode: core.mode,
      blockingReasons: Object.freeze([...requireStringArray(core.blockingReasons, "core.blockingReasons")]),
      actions: Object.freeze(actions),
    }),
    preferences: normalizePreferences(value.preferences),
  });
}

function maximumFriction(...levels: readonly FrictionLevel[]): FrictionLevel {
  const rank = Math.max(...levels.map((level) => FRICTION_RANK[level]));
  const selected = FRICTION_BY_RANK[rank];
  if (selected === undefined) throw new Error("internal friction rank invariant violated");
  return selected;
}

function riskFriction(action: ActionDescriptor): FrictionLevel {
  const risk: FrictionLevel =
    action.risk === "LOW" ? "NONE" : action.risk === "MEDIUM" ? "ACK" : action.risk === "HIGH" ? "CONFIRM" : "DOUBLE_CONFIRM";

  const reversibility: FrictionLevel =
    action.reversibility === "REVERSIBLE"
      ? "NONE"
      : action.reversibility === "REVERSIBLE_WITH_COST"
        ? "CONFIRM"
        : "DOUBLE_CONFIRM";

  const kindFloor: FrictionLevel = action.kind === "RECOVERY" ? "CONFIRM" : "NONE";
  return maximumFriction(action.minimumFriction, risk, reversibility, kindFloor);
}

function planAction(input: CompileInput, action: ActionDescriptor): PlannedAction {
  const reasons: string[] = [];
  const { core } = input;

  if (!action.backendAllowed) reasons.push("BACKEND_DENIED");
  if (!action.allowedRoles.includes(core.role)) reasons.push("ROLE_DENIED");
  if (!action.allowedSystemStates.includes(core.systemState)) reasons.push("STATE_DENIED");
  if (core.mode === "VIEW" && (action.kind === "MUTATE" || action.kind === "RECOVERY")) {
    reasons.push("VIEW_MODE_READ_ONLY");
  }
  if (core.systemState === "STOP" && (action.kind === "MUTATE" || action.kind === "RECOVERY")) {
    reasons.push("SYSTEM_STOPPED");
  }
  if (core.systemState === "FREEZE" && action.kind === "MUTATE") {
    reasons.push("SYSTEM_FROZEN");
  }
  if (action.requiresVerifiedTruth && core.truthStatus !== "VERIFIED") {
    reasons.push("VERIFIED_TRUTH_REQUIRED");
  }

  const denied = reasons.length > 0;
  const state = denied
    ? action.visibilityPolicy === "HIDE_WHEN_DENIED"
      ? "HIDDEN"
      : "DISABLED"
    : "ENABLED";

  return Object.freeze({
    id: action.id,
    label: action.label,
    kind: action.kind,
    state,
    reasons: Object.freeze(reasons),
    friction: state === "ENABLED" ? riskFriction(action) : "NONE",
  });
}

function truthBanner(input: CompileInput): TruthBanner {
  const { systemState, truthStatus, blockingReasons } = input.core;
  const reasons = Object.freeze([...blockingReasons]);

  if (systemState === "FREEZE") {
    return Object.freeze({ severity: "BLOCKING", code: "SYSTEM_FREEZE", title: "System frozen", reasons });
  }
  if (systemState === "STOP") {
    return Object.freeze({ severity: "BLOCKING", code: "SYSTEM_STOP", title: "System stopped", reasons });
  }
  if (truthStatus === "CONFLICT") {
    return Object.freeze({ severity: "BLOCKING", code: "TRUTH_CONFLICT", title: "Authoritative truth conflict", reasons });
  }
  if (truthStatus === "BLOCKED") {
    return Object.freeze({ severity: "BLOCKING", code: "TRUTH_BLOCKED", title: "Truth path blocked", reasons });
  }
  if (truthStatus === "UNKNOWN") {
    return Object.freeze({ severity: "WARNING", code: "TRUTH_UNKNOWN", title: "Truth not established", reasons });
  }
  if (truthStatus === "NOT_VERIFIED") {
    return Object.freeze({ severity: "WARNING", code: "TRUTH_NOT_VERIFIED", title: "Verification missing", reasons });
  }
  if (truthStatus === "PARTIAL") {
    return Object.freeze({ severity: "INFO", code: "TRUTH_PARTIAL", title: "Truth partially established", reasons });
  }
  return Object.freeze({ severity: "OK", code: "TRUTH_VERIFIED", title: "Truth verified", reasons });
}

function disclosureLevel(input: CompileInput, actions: readonly PlannedAction[]): DisclosureLevel {
  const preferred: DisclosureLevel =
    input.preferences.detail === "COMPACT"
      ? "MINIMAL"
      : input.preferences.detail === "BALANCED"
        ? "STANDARD"
        : "DIAGNOSTIC";

  const mustDiagnose =
    input.core.systemState === "FREEZE" ||
    input.core.systemState === "STOP" ||
    input.core.truthStatus === "CONFLICT" ||
    input.core.truthStatus === "BLOCKED" ||
    actions.some((action) => action.state === "ENABLED" && action.friction === "DOUBLE_CONFIRM");

  if (mustDiagnose) return "DIAGNOSTIC";
  if (input.core.truthStatus === "UNKNOWN" || input.core.truthStatus === "NOT_VERIFIED") {
    return preferred === "MINIMAL" ? "STANDARD" : preferred;
  }
  return preferred;
}

function mandatorySignals(input: CompileInput): readonly string[] {
  const signals = ["SYSTEM_STATE", "TRUTH_STATUS"];
  if (input.core.blockingReasons.length > 0) signals.push("BLOCKING_REASONS");
  if (input.core.systemState === "FREEZE") signals.push("FREEZE_BANNER");
  if (input.core.systemState === "STOP") signals.push("STOP_BANNER");
  return Object.freeze(signals);
}

/**
 * Compile a deterministic presentation plan from authoritative state.
 *
 * Security/authority boundary: this function can only narrow or explain action availability.
 * It cannot make a backend-denied, role-denied, state-denied, mode-denied, or truth-denied action executable.
 */
export function compileOperatorExperience(value: unknown): SurfacePlan {
  const input = normalizeInput(value);
  const actions = Object.freeze(input.core.actions.map((action) => planAction(input, action)));

  return Object.freeze({
    schemaVersion: "1.0" as const,
    systemPulse: input.core.systemState,
    truthStatus: input.core.truthStatus,
    truthBanner: truthBanner(input),
    disclosure: disclosureLevel(input, actions),
    mandatorySignals: mandatorySignals(input),
    actions,
    presentation: Object.freeze({ ...input.preferences }),
    invariants: Object.freeze([
      "PRESENTATION_CANNOT_CHANGE_TRUTH",
      "PRESENTATION_CANNOT_GRANT_AUTHORITY",
      "BACKEND_DENIAL_FAILS_CLOSED",
      "FREEZE_AND_STOP_ARE_MANDATORY_SIGNALS",
      "PREFERENCES_ARE_PRESENTATION_ONLY",
      "IDENTICAL_INPUTS_PRODUCE_IDENTICAL_OUTPUTS",
    ]),
  });
}
