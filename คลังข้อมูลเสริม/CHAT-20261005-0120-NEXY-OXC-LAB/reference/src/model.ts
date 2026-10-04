export const SYSTEM_STATES = [
  "INIT",
  "READY",
  "RUNNING",
  "VERIFYING",
  "CONSENSUS",
  "STABLE",
  "FREEZE",
  "STOP",
] as const;
export type SystemState = (typeof SYSTEM_STATES)[number];

export const TRUTH_STATUSES = [
  "VERIFIED",
  "PARTIAL",
  "UNKNOWN",
  "CONFLICT",
  "NOT_VERIFIED",
  "BLOCKED",
] as const;
export type TruthStatus = (typeof TRUTH_STATUSES)[number];

export const ROLES = ["OWNER", "OPERATOR", "AUDITOR", "VIEWER"] as const;
export type Role = (typeof ROLES)[number];

export const MODES = ["VIEW", "RUN", "FORGE"] as const;
export type Mode = (typeof MODES)[number];

export const ACTION_KINDS = ["READ", "INSPECT", "EXPORT", "MUTATE", "RECOVERY"] as const;
export type ActionKind = (typeof ACTION_KINDS)[number];

export const RISKS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"] as const;
export type Risk = (typeof RISKS)[number];

export const REVERSIBILITY = ["REVERSIBLE", "REVERSIBLE_WITH_COST", "IRREVERSIBLE"] as const;
export type Reversibility = (typeof REVERSIBILITY)[number];

export const FRICTION_LEVELS = ["NONE", "ACK", "CONFIRM", "DOUBLE_CONFIRM"] as const;
export type FrictionLevel = (typeof FRICTION_LEVELS)[number];

export const VISIBILITY_POLICIES = ["SHOW_DISABLED", "HIDE_WHEN_DENIED"] as const;
export type VisibilityPolicy = (typeof VISIBILITY_POLICIES)[number];

export const DETAIL_PREFERENCES = ["COMPACT", "BALANCED", "DEEP"] as const;
export type DetailPreference = (typeof DETAIL_PREFERENCES)[number];

export const DENSITIES = ["LOW", "MEDIUM", "HIGH"] as const;
export type Density = (typeof DENSITIES)[number];

export const MOTION_PREFERENCES = ["REDUCED", "STANDARD"] as const;
export type MotionPreference = (typeof MOTION_PREFERENCES)[number];

export const ACTION_PLAN_STATES = ["ENABLED", "DISABLED", "HIDDEN"] as const;
export type ActionPlanState = (typeof ACTION_PLAN_STATES)[number];

export const DISCLOSURE_LEVELS = ["MINIMAL", "STANDARD", "DIAGNOSTIC"] as const;
export type DisclosureLevel = (typeof DISCLOSURE_LEVELS)[number];

export type BannerSeverity = "OK" | "INFO" | "WARNING" | "BLOCKING";

export interface ActionDescriptor {
  readonly id: string;
  readonly label: string;
  readonly kind: ActionKind;
  readonly backendAllowed: boolean;
  readonly allowedRoles: readonly Role[];
  readonly allowedSystemStates: readonly SystemState[];
  readonly requiresVerifiedTruth: boolean;
  readonly risk: Risk;
  readonly reversibility: Reversibility;
  readonly minimumFriction: FrictionLevel;
  readonly visibilityPolicy: VisibilityPolicy;
}

export interface CoreSnapshot {
  readonly schemaVersion: "1.0";
  readonly systemState: SystemState;
  readonly truthStatus: TruthStatus;
  readonly role: Role;
  readonly mode: Mode;
  readonly blockingReasons: readonly string[];
  readonly actions: readonly ActionDescriptor[];
}

export interface PreferenceEnvelope {
  readonly detail: DetailPreference;
  readonly density: Density;
  readonly language: string;
  readonly motion: MotionPreference;
  readonly friendlyTone: boolean;
}

export interface CompileInput {
  readonly core: CoreSnapshot;
  readonly preferences: PreferenceEnvelope;
}

export interface TruthBanner {
  readonly severity: BannerSeverity;
  readonly code: string;
  readonly title: string;
  readonly reasons: readonly string[];
}

export interface PlannedAction {
  readonly id: string;
  readonly label: string;
  readonly kind: ActionKind;
  readonly state: ActionPlanState;
  readonly reasons: readonly string[];
  readonly friction: FrictionLevel;
}

export interface SurfacePlan {
  readonly schemaVersion: "1.0";
  readonly systemPulse: SystemState;
  readonly truthStatus: TruthStatus;
  readonly truthBanner: TruthBanner;
  readonly disclosure: DisclosureLevel;
  readonly mandatorySignals: readonly string[];
  readonly actions: readonly PlannedAction[];
  readonly presentation: Readonly<{
    detail: DetailPreference;
    density: Density;
    language: string;
    motion: MotionPreference;
    friendlyTone: boolean;
  }>;
  readonly invariants: readonly string[];
}
