export type Role = "OWNER" | "OPERATOR" | "AUDITOR" | "SYSTEM";
export type Mode = "VIEW" | "RUN" | "FORGE";
export type SystemState =
  | "INIT"
  | "READY"
  | "RUNNING"
  | "VERIFYING"
  | "CONSENSUS"
  | "STABLE"
  | "FREEZE"
  | "STOP";

export type ActionKind =
  | "READ"
  | "SUBMIT_DIRECTIVE"
  | "MUTATE_REVERSIBLE"
  | "MUTATE_IRREVERSIBLE"
  | "EXTERNAL_IO"
  | "CONFIG"
  | "RECOVER"
  | "EXPORT";

export type RiskTier = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type Reversibility = "READ_ONLY" | "REVERSIBLE" | "IRREVERSIBLE";
export type EvidenceStatus = "PASS" | "FAIL" | "NOT_VERIFIED";

export interface AcceptanceCriterion {
  id: string;
  statement: string;
  required: boolean;
}

export interface MaterialField {
  name: string;
  present: boolean;
  prompt: string;
}

export interface IntentContract {
  schema_version: "1.0";
  id: string;
  objective: string;
  mode: Mode;
  actor: {
    id: string;
    role: Role;
    declared_expertise?: "NEW" | "STANDARD" | "ADVANCED";
  };
  constraints: {
    allowed_scope: string[];
    protected_scope: string[];
    allow_external: boolean;
    max_interruptions: number;
  };
  required_outcomes: AcceptanceCriterion[];
  material_fields: MaterialField[];
}

export interface ActionRequest {
  id: string;
  kind: ActionKind;
  target_scope: string;
  risk: RiskTier;
  reversibility: Reversibility;
  supports_outcomes: string[];
  external: boolean;
  required_role?: Role;
}

export interface ConsentBinding {
  contract_hash: string;
  action_hash: string;
  granted_by_role: Role;
  explicit: boolean;
}

export interface PresentationState {
  freeze_visible: boolean;
  reported_success: boolean;
  visible_controls: string[];
}

export interface EvaluationContext {
  system_state: SystemState;
  recoverable?: boolean;
  interruptions_used: number;
}

export interface Scenario {
  id: string;
  contract: IntentContract;
  action: ActionRequest;
  context: EvaluationContext;
  consent?: ConsentBinding;
  presentation?: PresentationState;
}

export type DecisionStatus = "ALLOW" | "ASK" | "FREEZE";

export interface ActionDecision {
  status: DecisionStatus;
  reason_codes: string[];
  questions: string[];
  contract_hash: string;
  action_hash: string;
}

export interface PresentationEvaluation {
  status: EvidenceStatus;
  violations: string[];
}

export interface DisclosurePlan {
  panels: string[];
  controls: string[];
  mandatory_notices: string[];
}

export interface CriterionResult {
  id: string;
  status: EvidenceStatus;
  evidence_refs: string[];
}

export interface AcceptanceEvaluation {
  status: EvidenceStatus;
  missing_required: string[];
  failed_required: string[];
  evidence_missing: string[];
}

export interface TraceEvent {
  seq: number;
  kind:
    | "ASK_USER"
    | "ACTION_PROPOSED"
    | "ACTION_EXECUTED"
    | "FREEZE_SHOWN"
    | "SUCCESS_SHOWN"
    | "RESULT_SHOWN";
  material_blocker?: string;
}

export interface TraceEvaluation {
  status: EvidenceStatus;
  violations: string[];
  interruption_count: number;
}

export interface ScenarioEvaluation {
  scenario_id: string;
  decision: ActionDecision;
  presentation: PresentationEvaluation | null;
}
