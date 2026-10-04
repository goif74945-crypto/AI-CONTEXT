import { compareText, fingerprint64, hasDuplicates, isNonBlank, sortedUnique, type CanonicalValue } from "./canonical.js";

export type ProbeEffect = "READ_ONLY" | "REVERSIBLE_WRITE" | "IRREVERSIBLE";
export type Authority = "NONE" | "OPERATOR" | "OWNER";

export interface ProbeUnknown {
  readonly id: string;
  readonly blocking: boolean;
}

export interface ProbeDefinition {
  readonly id: string;
  readonly resolves: readonly string[];
  readonly effect: ProbeEffect;
  readonly cost: number;
  readonly requiredAuthority: Authority;
  readonly rollback?: string;
}

export interface ProbePlanningProblem {
  readonly unknowns: readonly ProbeUnknown[];
  readonly probes: readonly ProbeDefinition[];
  readonly availableAuthorities: readonly Exclude<Authority, "NONE">[];
  readonly maxTotalCost?: number;
}

export interface RejectedProbe {
  readonly probeId: string;
  readonly reason: "IRREVERSIBLE_EFFECT" | "MISSING_ROLLBACK" | "MISSING_AUTHORITY" | "NO_BLOCKING_GAIN";
}

export interface ProbePlanResult {
  readonly status: "READY" | "PROBE" | "BLOCKED" | "FREEZE";
  readonly selectedProbeIds: readonly string[];
  readonly totalCost: number;
  readonly minimumCost: number | null;
  readonly uncoveredUnknownIds: readonly string[];
  readonly rejectedProbes: readonly RejectedProbe[];
  readonly coverageWitness: Readonly<Record<string, readonly string[]>>;
  readonly reasons: readonly string[];
  readonly fingerprint: string;
}

const MAX_SEARCH_CANDIDATES = 24;
const EFFECTS: readonly ProbeEffect[] = ["READ_ONLY", "REVERSIBLE_WRITE", "IRREVERSIBLE"];
const AUTHORITIES: readonly Authority[] = ["NONE", "OPERATOR", "OWNER"];

function authorityLevel(authority: Authority): number {
  return authority === "NONE" ? 0 : authority === "OPERATOR" ? 1 : 2;
}

function highestAuthority(authorities: readonly Exclude<Authority, "NONE">[]): number {
  return authorities.reduce((maximum, authority) => Math.max(maximum, authorityLevel(authority)), 0);
}

function compareCandidate(a: readonly ProbeDefinition[], b: readonly ProbeDefinition[]): number {
  const costA = a.reduce((sum, probe) => sum + probe.cost, 0);
  const costB = b.reduce((sum, probe) => sum + probe.cost, 0);
  if (costA !== costB) return costA - costB;
  if (a.length !== b.length) return a.length - b.length;
  const idsA = a.map((probe) => probe.id).sort(compareText);
  const idsB = b.map((probe) => probe.id).sort(compareText);
  for (let index = 0; index < idsA.length; index += 1) {
    const comparison = compareText(idsA[index]!, idsB[index]!);
    if (comparison !== 0) return comparison;
  }
  return 0;
}

export function planReversibleProbes(problem: ProbePlanningProblem): ProbePlanResult {
  const blockingIds = problem.unknowns.filter((unknown) => unknown.blocking).map((unknown) => unknown.id).sort(compareText);
  const allUnknownIds = problem.unknowns.map((unknown) => unknown.id).sort(compareText);
  const reasons: string[] = [];

  if (allUnknownIds.some((id) => !isNonBlank(id))) reasons.push("BLANK_UNKNOWN_ID");
  if (hasDuplicates(allUnknownIds)) reasons.push("DUPLICATE_UNKNOWN_ID");
  const probeIds = problem.probes.map((probe) => probe.id);
  if (probeIds.some((id) => !isNonBlank(id))) reasons.push("BLANK_PROBE_ID");
  if (hasDuplicates(probeIds)) reasons.push("DUPLICATE_PROBE_ID");
  if (problem.probes.some((probe) => !Number.isInteger(probe.cost) || probe.cost <= 0)) reasons.push("INVALID_PROBE_COST");
  if (problem.probes.some((probe) => !EFFECTS.includes(probe.effect))) reasons.push("INVALID_PROBE_EFFECT");
  if (problem.probes.some((probe) => !AUTHORITIES.includes(probe.requiredAuthority))) reasons.push("INVALID_PROBE_AUTHORITY");
  if (problem.probes.some((probe) => hasDuplicates(probe.resolves) || probe.resolves.some((id) => !isNonBlank(id)))) {
    reasons.push("INVALID_PROBE_RESOLUTION_SET");
  }
  const unknownIdSet = new Set(allUnknownIds);
  if (problem.probes.some((probe) => probe.resolves.some((id) => !unknownIdSet.has(id)))) reasons.push("PROBE_REFERENCES_UNKNOWN_ID");
  if (problem.maxTotalCost !== undefined && (!Number.isInteger(problem.maxTotalCost) || problem.maxTotalCost < 0)) {
    reasons.push("INVALID_MAX_TOTAL_COST");
  }
  const knownAvailable = new Set<Authority>(["NONE", ...problem.availableAuthorities]);
  if (problem.availableAuthorities.some((authority) => authority !== "OPERATOR" && authority !== "OWNER")) {
    reasons.push("INVALID_AVAILABLE_AUTHORITY");
  }

  const normalizedProbes = problem.probes
    .map((probe) => ({ ...probe, resolves: sortedUnique(probe.resolves) }))
    .sort((a, b) => compareText(a.id, b.id));

  const rejectedProbes: RejectedProbe[] = [];
  const safeCandidates: ProbeDefinition[] = [];
  const blockingSet = new Set(blockingIds);
  const availableLevel = highestAuthority(problem.availableAuthorities);

  for (const probe of normalizedProbes) {
    if (probe.effect === "IRREVERSIBLE") {
      rejectedProbes.push({ probeId: probe.id, reason: "IRREVERSIBLE_EFFECT" });
      continue;
    }
    if (probe.effect === "REVERSIBLE_WRITE" && (probe.rollback === undefined || !isNonBlank(probe.rollback))) {
      rejectedProbes.push({ probeId: probe.id, reason: "MISSING_ROLLBACK" });
      continue;
    }
    if (!knownAvailable.has(probe.requiredAuthority) && authorityLevel(probe.requiredAuthority) > availableLevel) {
      rejectedProbes.push({ probeId: probe.id, reason: "MISSING_AUTHORITY" });
      continue;
    }
    if (authorityLevel(probe.requiredAuthority) > availableLevel) {
      rejectedProbes.push({ probeId: probe.id, reason: "MISSING_AUTHORITY" });
      continue;
    }
    if (!probe.resolves.some((id) => blockingSet.has(id))) {
      rejectedProbes.push({ probeId: probe.id, reason: "NO_BLOCKING_GAIN" });
      continue;
    }
    safeCandidates.push(probe);
  }
  rejectedProbes.sort((a, b) => compareText(a.probeId, b.probeId) || compareText(a.reason, b.reason));

  if (reasons.length > 0) {
    const sortedReasons = sortedUnique(reasons);
    const identity: CanonicalValue = { status: "FREEZE", blockingIds, reasons: sortedReasons };
    return {
      status: "FREEZE",
      selectedProbeIds: [],
      totalCost: 0,
      minimumCost: null,
      uncoveredUnknownIds: blockingIds,
      rejectedProbes,
      coverageWitness: {},
      reasons: sortedReasons,
      fingerprint: fingerprint64(identity),
    };
  }

  if (blockingIds.length === 0) {
    const identity: CanonicalValue = { status: "READY", blockingIds: [], selectedProbeIds: [] };
    return {
      status: "READY",
      selectedProbeIds: [],
      totalCost: 0,
      minimumCost: 0,
      uncoveredUnknownIds: [],
      rejectedProbes,
      coverageWitness: {},
      reasons: [],
      fingerprint: fingerprint64(identity),
    };
  }

  if (safeCandidates.length > MAX_SEARCH_CANDIDATES) {
    const resultReasons = ["SEARCH_BOUND_EXCEEDED"];
    const identity: CanonicalValue = { status: "BLOCKED", blockingIds, reasons: resultReasons };
    return {
      status: "BLOCKED",
      selectedProbeIds: [],
      totalCost: 0,
      minimumCost: null,
      uncoveredUnknownIds: blockingIds,
      rejectedProbes,
      coverageWitness: {},
      reasons: resultReasons,
      fingerprint: fingerprint64(identity),
    };
  }

  const coverable = new Set<string>();
  for (const probe of safeCandidates) for (const id of probe.resolves) if (blockingSet.has(id)) coverable.add(id);
  const impossible = blockingIds.filter((id) => !coverable.has(id));
  if (impossible.length > 0) {
    const resultReasons = impossible.map((id) => `NO_SAFE_PROBE:${id}`);
    const identity: CanonicalValue = { status: "BLOCKED", blockingIds, impossible, reasons: resultReasons };
    return {
      status: "BLOCKED",
      selectedProbeIds: [],
      totalCost: 0,
      minimumCost: null,
      uncoveredUnknownIds: impossible,
      rejectedProbes,
      coverageWitness: {},
      reasons: resultReasons,
      fingerprint: fingerprint64(identity),
    };
  }

  let best: ProbeDefinition[] | null = null;
  const selected: ProbeDefinition[] = [];
  const covered = new Set<string>();

  const search = (index: number): void => {
    if (covered.size === blockingSet.size) {
      const candidate = [...selected];
      if (best === null || compareCandidate(candidate, best) < 0) best = candidate;
      return;
    }
    if (index >= safeCandidates.length) return;
    if (best !== null) {
      const currentCost = selected.reduce((sum, probe) => sum + probe.cost, 0);
      const bestCost = best.reduce((sum, probe) => sum + probe.cost, 0);
      if (currentCost > bestCost) return;
    }

    const remainingCoverage = new Set(covered);
    for (let cursor = index; cursor < safeCandidates.length; cursor += 1) {
      for (const id of safeCandidates[cursor]!.resolves) if (blockingSet.has(id)) remainingCoverage.add(id);
    }
    if (remainingCoverage.size !== blockingSet.size) return;

    const probe = safeCandidates[index]!;
    const newlyCovered: string[] = [];
    for (const id of probe.resolves) {
      if (blockingSet.has(id) && !covered.has(id)) {
        covered.add(id);
        newlyCovered.push(id);
      }
    }
    selected.push(probe);
    search(index + 1);
    selected.pop();
    for (const id of newlyCovered) covered.delete(id);

    search(index + 1);
  };

  search(0);
  if (best === null) {
    const resultReasons = ["NO_COMPLETE_SAFE_COVER"];
    const identity: CanonicalValue = { status: "BLOCKED", blockingIds, reasons: resultReasons };
    return {
      status: "BLOCKED",
      selectedProbeIds: [],
      totalCost: 0,
      minimumCost: null,
      uncoveredUnknownIds: blockingIds,
      rejectedProbes,
      coverageWitness: {},
      reasons: resultReasons,
      fingerprint: fingerprint64(identity),
    };
  }

  const winning: ProbeDefinition[] = best;
  const minimumCost = winning.reduce((sum: number, probe: ProbeDefinition) => sum + probe.cost, 0);
  if (problem.maxTotalCost !== undefined && minimumCost > problem.maxTotalCost) {
    const resultReasons = ["COST_BUDGET_EXCEEDED"];
    const identity: CanonicalValue = { status: "BLOCKED", blockingIds, minimumCost, maxTotalCost: problem.maxTotalCost };
    return {
      status: "BLOCKED",
      selectedProbeIds: winning.map((probe: ProbeDefinition) => probe.id).sort(compareText),
      totalCost: minimumCost,
      minimumCost,
      uncoveredUnknownIds: [],
      rejectedProbes,
      coverageWitness: {},
      reasons: resultReasons,
      fingerprint: fingerprint64(identity),
    };
  }

  const selectedProbeIds = winning.map((probe: ProbeDefinition) => probe.id).sort(compareText);
  const coverageWitness: Record<string, string[]> = {};
  for (const id of blockingIds) {
    coverageWitness[id] = winning.filter((probe: ProbeDefinition) => probe.resolves.includes(id)).map((probe: ProbeDefinition) => probe.id).sort(compareText);
  }
  const identity: CanonicalValue = {
    status: "PROBE",
    blockingIds,
    selectedProbeIds,
    totalCost: minimumCost,
    coverageWitness,
  };
  return {
    status: "PROBE",
    selectedProbeIds,
    totalCost: minimumCost,
    minimumCost,
    uncoveredUnknownIds: [],
    rejectedProbes,
    coverageWitness,
    reasons: [],
    fingerprint: fingerprint64(identity),
  };
}
