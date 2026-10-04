import { compareText, fingerprint64, hasDuplicates, isNonBlank, sortedUnique, type CanonicalValue } from "./canonical.js";

export type PredicateStatus = "SATISFIED" | "VIOLATED" | "UNKNOWN";

export interface OutcomeContract {
  readonly id: string;
  readonly required: readonly string[];
  readonly forbidden: readonly string[];
  readonly minEvidencePerRequired: number;
}

export interface OutcomeObservation {
  readonly predicateId: string;
  readonly status: PredicateStatus;
  readonly evidenceIds: readonly string[];
}

export interface OutcomeClosureResult {
  readonly status: "CLOSED" | "OPEN" | "FREEZE";
  readonly openRequired: readonly string[];
  readonly violatedRequired: readonly string[];
  readonly evidenceDeficits: readonly string[];
  readonly unresolvedForbidden: readonly string[];
  readonly triggeredForbidden: readonly string[];
  readonly reasons: readonly string[];
  readonly fingerprint: string;
}

interface NormalizedObservation {
  readonly predicateId: string;
  readonly status: PredicateStatus;
  readonly evidenceIds: readonly string[];
}

function normalizeObservations(observations: readonly OutcomeObservation[]): NormalizedObservation[] {
  return observations
    .map((observation) => ({
      predicateId: observation.predicateId,
      status: observation.status,
      evidenceIds: sortedUnique(observation.evidenceIds),
    }))
    .sort((a, b) => compareText(a.predicateId, b.predicateId));
}

export function evaluateOutcomeClosure(
  contract: OutcomeContract,
  observations: readonly OutcomeObservation[],
): OutcomeClosureResult {
  const required = sortedUnique(contract.required);
  const forbidden = sortedUnique(contract.forbidden);
  const normalizedObservations = normalizeObservations(observations);
  const validationReasons: string[] = [];

  if (!isNonBlank(contract.id)) validationReasons.push("BLANK_CONTRACT_ID");
  if (!Number.isInteger(contract.minEvidencePerRequired) || contract.minEvidencePerRequired < 1) {
    validationReasons.push("INVALID_MIN_EVIDENCE");
  }
  if (contract.required.some((id) => !isNonBlank(id)) || contract.forbidden.some((id) => !isNonBlank(id))) {
    validationReasons.push("BLANK_PREDICATE_ID");
  }
  if (hasDuplicates(contract.required) || hasDuplicates(contract.forbidden)) {
    validationReasons.push("DUPLICATE_CONTRACT_PREDICATE");
  }
  const overlap = required.filter((id) => forbidden.includes(id));
  if (overlap.length > 0) validationReasons.push("REQUIRED_FORBIDDEN_OVERLAP");

  const observedIds = normalizedObservations.map((observation) => observation.predicateId);
  if (hasDuplicates(observedIds)) validationReasons.push("DUPLICATE_OBSERVATION");
  if (normalizedObservations.some((observation) => !isNonBlank(observation.predicateId))) {
    validationReasons.push("BLANK_OBSERVATION_ID");
  }
  if (normalizedObservations.some((observation) => observation.evidenceIds.some((id) => !isNonBlank(id)))) {
    validationReasons.push("BLANK_EVIDENCE_ID");
  }
  const contractIds = new Set([...required, ...forbidden]);
  if (normalizedObservations.some((observation) => !contractIds.has(observation.predicateId))) {
    validationReasons.push("UNKNOWN_OBSERVED_PREDICATE");
  }

  const observationById = new Map<string, NormalizedObservation>();
  for (const observation of normalizedObservations) {
    if (!observationById.has(observation.predicateId)) observationById.set(observation.predicateId, observation);
  }

  const openRequired: string[] = [];
  const violatedRequired: string[] = [];
  const evidenceDeficits: string[] = [];
  for (const id of required) {
    const observation = observationById.get(id);
    if (observation === undefined || observation.status === "UNKNOWN") {
      openRequired.push(id);
      continue;
    }
    if (observation.status === "VIOLATED") {
      violatedRequired.push(id);
      continue;
    }
    if (observation.evidenceIds.length < contract.minEvidencePerRequired) evidenceDeficits.push(id);
  }

  const unresolvedForbidden: string[] = [];
  const triggeredForbidden: string[] = [];
  for (const id of forbidden) {
    const observation = observationById.get(id);
    if (observation === undefined || observation.status === "UNKNOWN") {
      unresolvedForbidden.push(id);
      continue;
    }
    if (observation.status === "SATISFIED") {
      triggeredForbidden.push(id);
      continue;
    }
    if (observation.evidenceIds.length === 0) unresolvedForbidden.push(id);
  }

  const reasons = sortedUnique([
    ...validationReasons,
    ...openRequired.map((id) => `REQUIRED_UNKNOWN:${id}`),
    ...violatedRequired.map((id) => `REQUIRED_VIOLATED:${id}`),
    ...evidenceDeficits.map((id) => `EVIDENCE_DEFICIT:${id}`),
    ...unresolvedForbidden.map((id) => `FORBIDDEN_UNRESOLVED:${id}`),
    ...triggeredForbidden.map((id) => `FORBIDDEN_TRIGGERED:${id}`),
  ]);

  const status: OutcomeClosureResult["status"] =
    validationReasons.length > 0 || triggeredForbidden.length > 0
      ? "FREEZE"
      : openRequired.length > 0 || violatedRequired.length > 0 || evidenceDeficits.length > 0 || unresolvedForbidden.length > 0
        ? "OPEN"
        : "CLOSED";

  const identity: CanonicalValue = {
    contract: {
      id: contract.id,
      required,
      forbidden,
      minEvidencePerRequired: contract.minEvidencePerRequired,
    },
    observations: normalizedObservations.map((observation) => ({
      predicateId: observation.predicateId,
      status: observation.status,
      evidenceIds: [...observation.evidenceIds],
    })),
    result: {
      status,
      openRequired: [...openRequired].sort(compareText),
      violatedRequired: [...violatedRequired].sort(compareText),
      evidenceDeficits: [...evidenceDeficits].sort(compareText),
      unresolvedForbidden: [...unresolvedForbidden].sort(compareText),
      triggeredForbidden: [...triggeredForbidden].sort(compareText),
      reasons,
    },
  };

  return {
    status,
    openRequired: [...openRequired].sort(compareText),
    violatedRequired: [...violatedRequired].sort(compareText),
    evidenceDeficits: [...evidenceDeficits].sort(compareText),
    unresolvedForbidden: [...unresolvedForbidden].sort(compareText),
    triggeredForbidden: [...triggeredForbidden].sort(compareText),
    reasons,
    fingerprint: fingerprint64(identity),
  };
}
