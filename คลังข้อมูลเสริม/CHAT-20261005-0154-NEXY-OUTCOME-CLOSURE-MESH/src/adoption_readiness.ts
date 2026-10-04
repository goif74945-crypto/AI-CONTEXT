import { compareText, fingerprint64, hasDuplicates, isNonBlank, sortedUnique, type CanonicalValue } from "./canonical.js";
import type { ProgressAggregate } from "./progress_truth.js";

export type CompatibilityStatus = "PASS" | "FAIL" | "UNKNOWN";

export interface AdoptionDossier {
  readonly proposalId: string;
  readonly collisionScan: {
    readonly checked: boolean;
    readonly unresolvedOverlapIds: readonly string[];
  };
  readonly compatibility: readonly {
    readonly id: string;
    readonly status: CompatibilityStatus;
  }[];
  readonly evidenceClassesPresent: readonly string[];
  readonly requiredEvidenceClasses: readonly string[];
  readonly rollback: {
    readonly defined: boolean;
    readonly verified: boolean;
  };
  readonly protectedScopeMutation: boolean;
  readonly outcomeStatus: "CLOSED" | "OPEN" | "FREEZE";
  readonly progressStatus: ProgressAggregate;
  readonly benefitStatus: "BENEFICIAL" | "REJECT" | "INCONCLUSIVE" | "FREEZE";
}

export interface AdoptionReadinessResult {
  readonly status: "READY_FOR_HUMAN_REVIEW" | "HOLD" | "FREEZE";
  readonly automaticApproval: false;
  readonly reasons: readonly string[];
  readonly missingEvidenceClasses: readonly string[];
  readonly fingerprint: string;
}

export function evaluateAdoptionReadiness(dossier: AdoptionDossier): AdoptionReadinessResult {
  const reasons: string[] = [];
  const validationReasons: string[] = [];
  if (!isNonBlank(dossier.proposalId)) validationReasons.push("BLANK_PROPOSAL_ID");
  const compatibilityIds = dossier.compatibility.map((item) => item.id);
  if (compatibilityIds.some((id) => !isNonBlank(id))) validationReasons.push("BLANK_COMPATIBILITY_ID");
  if (hasDuplicates(compatibilityIds)) validationReasons.push("DUPLICATE_COMPATIBILITY_ID");
  if (dossier.compatibility.some((item) => item.status !== "PASS" && item.status !== "FAIL" && item.status !== "UNKNOWN")) {
    validationReasons.push("INVALID_COMPATIBILITY_STATUS");
  }
  if (dossier.requiredEvidenceClasses.some((id) => !isNonBlank(id)) || dossier.evidenceClassesPresent.some((id) => !isNonBlank(id))) {
    validationReasons.push("BLANK_EVIDENCE_CLASS");
  }
  if (hasDuplicates(dossier.requiredEvidenceClasses) || hasDuplicates(dossier.evidenceClassesPresent)) {
    validationReasons.push("DUPLICATE_EVIDENCE_CLASS");
  }

  const requiredEvidence = sortedUnique(dossier.requiredEvidenceClasses);
  const presentEvidence = new Set(dossier.evidenceClassesPresent);
  const missingEvidenceClasses = requiredEvidence.filter((evidenceClass) => !presentEvidence.has(evidenceClass));
  const unresolvedOverlapIds = sortedUnique(dossier.collisionScan.unresolvedOverlapIds);
  const compatibility = [...dossier.compatibility].sort((a, b) => compareText(a.id, b.id));

  if (dossier.protectedScopeMutation) reasons.push("PROTECTED_SCOPE_MUTATION");
  if (!dossier.collisionScan.checked) reasons.push("COLLISION_SCAN_NOT_RUN");
  if (unresolvedOverlapIds.length > 0) reasons.push("UNRESOLVED_OVERLAP");
  if (compatibility.some((item) => item.status === "FAIL")) reasons.push("COMPATIBILITY_FAILURE");
  if (compatibility.some((item) => item.status === "UNKNOWN")) reasons.push("COMPATIBILITY_UNKNOWN");
  if (missingEvidenceClasses.length > 0) reasons.push("MISSING_REQUIRED_EVIDENCE");
  if (!dossier.rollback.defined) reasons.push("ROLLBACK_NOT_DEFINED");
  else if (!dossier.rollback.verified) reasons.push("ROLLBACK_NOT_VERIFIED");
  if (dossier.outcomeStatus !== "CLOSED") reasons.push(`OUTCOME_${dossier.outcomeStatus}`);
  if (dossier.progressStatus !== "COMPLETE") reasons.push(`PROGRESS_${dossier.progressStatus}`);
  if (dossier.benefitStatus !== "BENEFICIAL") reasons.push(`BENEFIT_${dossier.benefitStatus}`);
  reasons.push(...validationReasons);

  const freezeReasons = new Set([
    "PROTECTED_SCOPE_MUTATION",
    "COMPATIBILITY_FAILURE",
    "OUTCOME_FREEZE",
    "PROGRESS_FREEZE",
    "BENEFIT_FREEZE",
    ...validationReasons,
  ]);
  const sortedReasons = sortedUnique(reasons);
  const status: AdoptionReadinessResult["status"] = sortedReasons.some((reason) => freezeReasons.has(reason))
    ? "FREEZE"
    : sortedReasons.length > 0
      ? "HOLD"
      : "READY_FOR_HUMAN_REVIEW";

  const identity: CanonicalValue = {
    proposalId: dossier.proposalId,
    collisionScan: { checked: dossier.collisionScan.checked, unresolvedOverlapIds },
    compatibility: compatibility.map((item) => ({ id: item.id, status: item.status })),
    evidenceClassesPresent: sortedUnique(dossier.evidenceClassesPresent),
    requiredEvidenceClasses: requiredEvidence,
    rollback: { defined: dossier.rollback.defined, verified: dossier.rollback.verified },
    protectedScopeMutation: dossier.protectedScopeMutation,
    outcomeStatus: dossier.outcomeStatus,
    progressStatus: dossier.progressStatus,
    benefitStatus: dossier.benefitStatus,
    status,
    reasons: sortedReasons,
    missingEvidenceClasses,
    automaticApproval: false,
  };

  return {
    status,
    automaticApproval: false,
    reasons: sortedReasons,
    missingEvidenceClasses,
    fingerprint: fingerprint64(identity),
  };
}
