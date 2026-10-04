export type VerificationStatus =
  | "PASS"
  | "FAIL"
  | "PARTIAL"
  | "BLOCKED"
  | "NOT_VERIFIED"
  | "UNKNOWN"
  | "CONFLICT";

export type Decision = "PASS" | "REVIEW" | "FREEZE";

export interface VersionedEnvelope<T> {
  protocol: "nexy.aux.reference.v1";
  system: string;
  inputHash?: string;
  payload: T;
}

export interface Diagnostic {
  code: string;
  message: string;
  path?: string;
}

export class ContractError extends Error {
  readonly diagnostics: readonly Diagnostic[];

  constructor(message: string, diagnostics: readonly Diagnostic[] = []) {
    super(message);
    this.name = "ContractError";
    this.diagnostics = diagnostics;
  }
}
